-- =================================================================
-- Echo — Database Schema
-- Supabase PostgreSQL + pgvector
-- =================================================================

-- Enable extensions
create extension if not exists vector;
create extension if not exists pg_trgm;  -- For fuzzy text search

-- -----------------------------------------------------------------
-- PROFILES (extends Supabase auth.users)
-- -----------------------------------------------------------------
create table if not exists profiles (
  id          uuid primary key references auth.users(id) on delete cascade,
  email       text unique not null,
  full_name   text not null,
  avatar_url  text,
  organization text default '',
  role        text default 'viewer'
                check (role in ('admin', 'editor', 'viewer')),
  created_at  timestamptz default now(),
  updated_at  timestamptz default now()
);

-- Auto-create profile on signup
create or replace function handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email, full_name)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1))
  );
  return new;
end;
$$ language plpgsql security definer;

create or replace trigger on_auth_user_created
  after insert on auth.users
  for each row execute function handle_new_user();

-- -----------------------------------------------------------------
-- DOCUMENTS
-- -----------------------------------------------------------------
create table if not exists documents (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid references profiles(id) on delete cascade not null,
  title           text not null,
  file_type       text not null,
  file_url        text,
  file_path       text,
  file_size       bigint default 0,
  page_count      integer default 0,
  category        text,
  status          text default 'uploading'
                    check (status in ('uploading','processing','ocr','embedding','indexed','failed')),
  summary         text,
  equipment_tags  text[] default '{}',
  tags            text[] default '{}',
  metadata        jsonb default '{}',
  error_message   text,
  created_at      timestamptz default now(),
  updated_at      timestamptz default now()
);

create index idx_documents_user_id on documents(user_id);
create index idx_documents_status on documents(status);
create index idx_documents_category on documents(category);
create index idx_documents_title_trgm on documents using gin (title gin_trgm_ops);

-- -----------------------------------------------------------------
-- DOCUMENT CHUNKS (with pgvector embeddings)
-- -----------------------------------------------------------------
create table if not exists document_chunks (
  id            uuid primary key default gen_random_uuid(),
  document_id   uuid references documents(id) on delete cascade not null,
  user_id       uuid not null,
  chunk_index   integer not null,
  content       text not null,
  page_number   integer,
  token_count   integer default 0,
  embedding     vector(1536),
  metadata      jsonb default '{}',
  created_at    timestamptz default now()
);

create index idx_chunks_document_id on document_chunks(document_id);
create index idx_chunks_user_id on document_chunks(user_id);
create index idx_chunks_embedding on document_chunks
  using ivfflat (embedding vector_cosine_ops) with (lists = 100);

-- -----------------------------------------------------------------
-- EQUIPMENT
-- -----------------------------------------------------------------
create table if not exists equipment (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid references profiles(id) on delete cascade not null,
  name            text not null,
  type            text not null,
  model           text,
  manufacturer    text,
  serial_number   text,
  location        text,
  status          text default 'operational'
                    check (status in ('operational','maintenance','warning','critical','offline')),
  health_score    integer default 100
                    check (health_score >= 0 and health_score <= 100),
  specifications  jsonb default '{}',
  installed_date  date,
  last_inspection date,
  next_inspection date,
  created_at      timestamptz default now(),
  updated_at      timestamptz default now()
);

create index idx_equipment_user_id on equipment(user_id);
create index idx_equipment_status on equipment(status);

-- -----------------------------------------------------------------
-- MAINTENANCE EVENTS
-- -----------------------------------------------------------------
create table if not exists maintenance_events (
  id            uuid primary key default gen_random_uuid(),
  equipment_id  uuid references equipment(id) on delete cascade not null,
  event_type    text not null,
  description   text not null,
  technician    text,
  status        text default 'scheduled'
                  check (status in ('scheduled','in_progress','completed','cancelled')),
  event_date    date not null,
  created_at    timestamptz default now()
);

create index idx_maintenance_equipment_id on maintenance_events(equipment_id);

-- -----------------------------------------------------------------
-- CONVERSATIONS
-- -----------------------------------------------------------------
create table if not exists conversations (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid references profiles(id) on delete cascade not null,
  title         text default 'New Conversation',
  last_message  text,
  message_count integer default 0,
  created_at    timestamptz default now(),
  updated_at    timestamptz default now()
);

create index idx_conversations_user_id on conversations(user_id);

-- -----------------------------------------------------------------
-- MESSAGES
-- -----------------------------------------------------------------
create table if not exists messages (
  id                uuid primary key default gen_random_uuid(),
  conversation_id   uuid references conversations(id) on delete cascade not null,
  role              text not null check (role in ('user','assistant','system')),
  content           text not null,
  sources           jsonb default '[]',
  confidence        float,
  metadata          jsonb default '{}',
  created_at        timestamptz default now()
);

create index idx_messages_conversation_id on messages(conversation_id);

-- -----------------------------------------------------------------
-- KNOWLEDGE GRAPH EDGES
-- -----------------------------------------------------------------
create table if not exists knowledge_edges (
  id            uuid primary key default gen_random_uuid(),
  source_id     text not null,
  source_type   text not null
                  check (source_type in ('document','equipment','topic','person')),
  target_id     text not null,
  target_type   text not null
                  check (target_type in ('document','equipment','topic','person')),
  relationship  text not null,
  label         text not null,
  weight        float default 1.0,
  metadata      jsonb default '{}',
  user_id       uuid references profiles(id) on delete cascade not null,
  created_at    timestamptz default now()
);

create index idx_edges_user_id on knowledge_edges(user_id);
create index idx_edges_source on knowledge_edges(source_id, source_type);
create index idx_edges_target on knowledge_edges(target_id, target_type);

-- -----------------------------------------------------------------
-- ACTIVITY LOG
-- -----------------------------------------------------------------
create table if not exists activity_log (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid references profiles(id) on delete cascade not null,
  type        text not null
                check (type in ('upload','query','alert','maintenance','login')),
  title       text not null,
  description text default '',
  severity    text default 'info'
                check (severity in ('info','warning','critical')),
  metadata    jsonb default '{}',
  created_at  timestamptz default now()
);

create index idx_activity_user_id on activity_log(user_id);
create index idx_activity_type on activity_log(type);

-- -----------------------------------------------------------------
-- RPC: Vector Similarity Search
-- -----------------------------------------------------------------
create or replace function match_chunks(
  query_embedding vector(1536),
  match_count int default 8,
  filter_user_id uuid default null
)
returns table (
  id            uuid,
  document_id   uuid,
  content       text,
  page_number   integer,
  chunk_index   integer,
  similarity    float
)
language plpgsql
as $$
begin
  return query
  select
    dc.id,
    dc.document_id,
    dc.content,
    dc.page_number,
    dc.chunk_index,
    1 - (dc.embedding <=> query_embedding) as similarity
  from document_chunks dc
  where dc.user_id = filter_user_id
    and dc.embedding is not null
  order by dc.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- -----------------------------------------------------------------
-- RPC: Unified Search
-- -----------------------------------------------------------------
create or replace function unified_search(
  search_query text,
  filter_user_id uuid,
  result_limit int default 10
)
returns table (
  result_id     text,
  result_type   text,
  title         text,
  excerpt       text,
  relevance     float
)
language plpgsql
as $$
begin
  return query
  -- Search documents
  select
    d.id::text as result_id,
    'document' as result_type,
    d.title,
    coalesce(d.summary, left(d.title, 200)) as excerpt,
    similarity(d.title, search_query) as relevance
  from documents d
  where d.user_id = filter_user_id
    and (d.title ilike '%' || search_query || '%'
      or d.summary ilike '%' || search_query || '%')

  union all

  -- Search equipment
  select
    e.id::text,
    'equipment',
    e.name,
    coalesce(e.manufacturer, '') || ' ' || coalesce(e.model, ''),
    similarity(e.name, search_query)
  from equipment e
  where e.user_id = filter_user_id
    and (e.name ilike '%' || search_query || '%'
      or e.manufacturer ilike '%' || search_query || '%')

  union all

  -- Search conversations
  select
    c.id::text,
    'conversation',
    c.title,
    coalesce(c.last_message, ''),
    similarity(c.title, search_query)
  from conversations c
  where c.user_id = filter_user_id
    and c.title ilike '%' || search_query || '%'

  order by relevance desc
  limit result_limit;
end;
$$;

-- -----------------------------------------------------------------
-- TRIGGERS: Auto-update updated_at
-- -----------------------------------------------------------------
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger profiles_updated_at
  before update on profiles for each row execute function update_updated_at();
create trigger documents_updated_at
  before update on documents for each row execute function update_updated_at();
create trigger equipment_updated_at
  before update on equipment for each row execute function update_updated_at();
create trigger conversations_updated_at
  before update on conversations for each row execute function update_updated_at();

-- -----------------------------------------------------------------
-- ROW LEVEL SECURITY
-- -----------------------------------------------------------------
alter table profiles enable row level security;
alter table documents enable row level security;
alter table document_chunks enable row level security;
alter table equipment enable row level security;
alter table conversations enable row level security;
alter table messages enable row level security;
alter table maintenance_events enable row level security;
alter table knowledge_edges enable row level security;
alter table activity_log enable row level security;

-- Profiles
create policy "Users read own profile"
  on profiles for select using (auth.uid() = id);
create policy "Users update own profile"
  on profiles for update using (auth.uid() = id);

-- Documents
create policy "Users manage own documents"
  on documents for all using (auth.uid() = user_id);

-- Document Chunks
create policy "Users manage own chunks"
  on document_chunks for all using (auth.uid() = user_id);

-- Equipment
create policy "Users manage own equipment"
  on equipment for all using (auth.uid() = user_id);

-- Conversations
create policy "Users manage own conversations"
  on conversations for all using (auth.uid() = user_id);

-- Messages (via conversation ownership)
create policy "Users manage own messages"
  on messages for all using (
    conversation_id in (
      select id from conversations where user_id = auth.uid()
    )
  );

-- Maintenance Events (via equipment ownership)
create policy "Users manage own maintenance"
  on maintenance_events for all using (
    equipment_id in (
      select id from equipment where user_id = auth.uid()
    )
  );

-- Knowledge Edges
create policy "Users manage own graph"
  on knowledge_edges for all using (auth.uid() = user_id);

-- Activity Log
create policy "Users read own activity"
  on activity_log for all using (auth.uid() = user_id);
