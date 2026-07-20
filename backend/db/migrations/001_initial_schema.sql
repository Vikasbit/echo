-- ══════════════════════════════════════════════════════════════════
-- INDUS AI — Initial Database Schema
-- PostgreSQL + pgvector on Supabase
-- ══════════════════════════════════════════════════════════════════

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ── Profiles ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS profiles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT NOT NULL UNIQUE,
    full_name       TEXT NOT NULL,
    avatar_url      TEXT,
    role            TEXT NOT NULL DEFAULT 'viewer',
    organization    TEXT NOT NULL DEFAULT '',
    password_hash   TEXT,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- ── Documents ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS documents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    title           TEXT NOT NULL,
    file_type       TEXT NOT NULL,
    file_url        TEXT NOT NULL DEFAULT '',
    file_size       BIGINT NOT NULL DEFAULT 0,
    page_count      INTEGER DEFAULT 0,
    category        TEXT DEFAULT 'Uncategorized',
    status          TEXT NOT NULL DEFAULT 'uploading',
    summary         TEXT,
    equipment_tags  TEXT[] DEFAULT '{}',
    tags            TEXT[] DEFAULT '{}',
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- ── Document Chunks ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS document_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id     UUID REFERENCES documents(id) ON DELETE CASCADE NOT NULL,
    chunk_index     INTEGER NOT NULL,
    content         TEXT NOT NULL,
    page_number     INTEGER,
    token_count     INTEGER,
    embedding       vector(1536),
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ── Equipment ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS equipment (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    name            TEXT NOT NULL,
    type            TEXT NOT NULL,
    model           TEXT,
    manufacturer    TEXT,
    serial_number   TEXT,
    location        TEXT,
    status          TEXT NOT NULL DEFAULT 'operational',
    health_score    INTEGER DEFAULT 100 CHECK (health_score >= 0 AND health_score <= 100),
    specifications  JSONB DEFAULT '{}',
    installed_date  DATE,
    last_inspection DATE,
    next_inspection DATE,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- ── Maintenance Events ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS maintenance_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    equipment_id    UUID REFERENCES equipment(id) ON DELETE CASCADE NOT NULL,
    event_type      TEXT NOT NULL,
    description     TEXT NOT NULL,
    technician      TEXT,
    status          TEXT NOT NULL DEFAULT 'scheduled',
    event_date      TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ── Conversations ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    title           TEXT NOT NULL DEFAULT 'New Conversation',
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- ── Messages ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE NOT NULL,
    role            TEXT NOT NULL,
    content         TEXT NOT NULL,
    sources         JSONB DEFAULT '[]',
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ── Knowledge Graph Edges ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS knowledge_edges (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id       UUID NOT NULL,
    source_type     TEXT NOT NULL,
    target_id       UUID NOT NULL,
    target_type     TEXT NOT NULL,
    relationship    TEXT NOT NULL,
    weight          FLOAT DEFAULT 1.0,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ══════════════════════════════════════════════════════════════════
-- INDEXES
-- ══════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_documents_user ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
CREATE INDEX IF NOT EXISTS idx_documents_created ON documents(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_chunks_document ON document_chunks(document_id);

CREATE INDEX IF NOT EXISTS idx_equipment_user ON equipment(user_id);
CREATE INDEX IF NOT EXISTS idx_equipment_status ON equipment(status);
CREATE INDEX IF NOT EXISTS idx_equipment_type ON equipment(type);

CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_updated ON conversations(updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at ASC);

CREATE INDEX IF NOT EXISTS idx_knowledge_edges_source ON knowledge_edges(source_id, source_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_edges_target ON knowledge_edges(target_id, target_type);

-- ══════════════════════════════════════════════════════════════════
-- pgvector IVFFlat INDEX (run after inserting initial data)
-- ══════════════════════════════════════════════════════════════════

-- CREATE INDEX IF NOT EXISTS idx_chunks_embedding
--     ON document_chunks USING ivfflat (embedding vector_cosine_ops)
--     WITH (lists = 100);

-- ══════════════════════════════════════════════════════════════════
-- FUNCTIONS
-- ══════════════════════════════════════════════════════════════════

-- Vector similarity search function for pgvector
CREATE OR REPLACE FUNCTION match_chunks(
    query_embedding vector(1536),
    match_count INT DEFAULT 8,
    filter_user_id UUID DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    document_id UUID,
    chunk_index INT,
    content TEXT,
    page_number INT,
    token_count INT,
    metadata JSONB,
    similarity FLOAT,
    document_title TEXT,
    category TEXT,
    file_type TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        dc.id,
        dc.document_id,
        dc.chunk_index,
        dc.content,
        dc.page_number,
        dc.token_count,
        dc.metadata,
        1 - (dc.embedding <=> query_embedding) AS similarity,
        d.title AS document_title,
        d.category,
        d.file_type
    FROM document_chunks dc
    JOIN documents d ON dc.document_id = d.id
    WHERE
        d.status = 'indexed'
        AND (filter_user_id IS NULL OR d.user_id = filter_user_id)
    ORDER BY dc.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_equipment_updated_at
    BEFORE UPDATE ON equipment
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
