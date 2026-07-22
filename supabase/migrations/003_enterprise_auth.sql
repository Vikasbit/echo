-- Migration 003: Enterprise Authentication & Workspaces

-- 1. Create Workspaces Table
CREATE TABLE IF NOT EXISTS public.workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    industry TEXT,
    subscription TEXT DEFAULT 'free' CHECK (subscription IN ('free', 'pro', 'enterprise')),
    owner_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 2. Create Companies Table
CREATE TABLE IF NOT EXISTS public.companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES public.workspaces(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    industry TEXT,
    employees TEXT,
    country TEXT,
    logo TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 3. Update Profiles Table
ALTER TABLE public.profiles
ADD COLUMN workspace_id UUID REFERENCES public.workspaces(id) ON DELETE CASCADE,
ADD COLUMN company_id UUID REFERENCES public.companies(id) ON DELETE CASCADE,
ADD COLUMN role TEXT DEFAULT 'Viewer' CHECK (role IN ('Owner', 'Admin', 'Engineer', 'Technician', 'Operator', 'Viewer')),
ADD COLUMN department TEXT;

-- Remove existing handle_new_user trigger to replace it
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- 4. Unified handle_new_user function for multi-step onboarding
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
DECLARE
    new_workspace_id UUID;
    new_company_id UUID;
    is_owner BOOLEAN := false;
BEGIN
    -- Only create a workspace if company_name is provided (which implies Owner signup)
    IF new.raw_user_meta_data->>'company_name' IS NOT NULL THEN
        -- Create workspace
        INSERT INTO public.workspaces (company_name, industry, owner_id)
        VALUES (
            new.raw_user_meta_data->>'company_name',
            new.raw_user_meta_data->>'industry',
            new.id
        ) RETURNING id INTO new_workspace_id;

        -- Create company
        INSERT INTO public.companies (workspace_id, name, industry, employees)
        VALUES (
            new_workspace_id,
            new.raw_user_meta_data->>'company_name',
            new.raw_user_meta_data->>'industry',
            new.raw_user_meta_data->>'company_size'
        ) RETURNING id INTO new_company_id;

        is_owner := true;
    ELSE
        -- For invited users, the frontend should pass workspace_id and role
        -- We will just use what they pass (or null if not provided, though that's an error state)
        new_workspace_id := (new.raw_user_meta_data->>'workspace_id')::UUID;
        new_company_id := (new.raw_user_meta_data->>'company_id')::UUID;
    END IF;

    -- Create profile
    INSERT INTO public.profiles (
        id, 
        email, 
        full_name, 
        company_name, 
        workspace_id, 
        company_id, 
        role
    )
    VALUES (
        new.id,
        new.email,
        new.raw_user_meta_data->>'full_name',
        new.raw_user_meta_data->>'company_name',
        new_workspace_id,
        new_company_id,
        CASE WHEN is_owner THEN 'Owner' ELSE coalesce(new.raw_user_meta_data->>'role', 'Viewer') END
    );

    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Re-attach trigger
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 5. Update Documents Table
ALTER TABLE public.documents
ADD COLUMN workspace_id UUID REFERENCES public.workspaces(id) ON DELETE CASCADE,
ADD COLUMN company_id UUID REFERENCES public.companies(id) ON DELETE CASCADE,
ADD COLUMN uploaded_by UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
ADD COLUMN department TEXT,
ADD COLUMN equipment TEXT,
ADD COLUMN version TEXT DEFAULT '1.0',
ADD COLUMN uploaded_at TIMESTAMPTZ DEFAULT NOW();

-- 6. Enable RLS on new tables
ALTER TABLE public.workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.companies ENABLE ROW LEVEL SECURITY;

-- 7. RLS Policies
-- Workspaces: Users can view their own workspace
CREATE POLICY "Users can view their workspace" ON public.workspaces
    FOR SELECT USING (id IN (SELECT workspace_id FROM public.profiles WHERE profiles.id = auth.uid()));

-- Companies: Users can view companies in their workspace
CREATE POLICY "Users can view companies in their workspace" ON public.companies
    FOR SELECT USING (workspace_id IN (SELECT workspace_id FROM public.profiles WHERE profiles.id = auth.uid()));

-- Documents: Drop old policy and add workspace-based policy
DROP POLICY IF EXISTS "Users manage own documents" ON public.documents;
CREATE POLICY "Users view workspace documents" ON public.documents
    FOR SELECT USING (workspace_id IN (SELECT workspace_id FROM public.profiles WHERE profiles.id = auth.uid()));
CREATE POLICY "Users insert workspace documents" ON public.documents
    FOR INSERT WITH CHECK (workspace_id IN (SELECT workspace_id FROM public.profiles WHERE profiles.id = auth.uid()));
CREATE POLICY "Users update workspace documents" ON public.documents
    FOR UPDATE USING (workspace_id IN (SELECT workspace_id FROM public.profiles WHERE profiles.id = auth.uid()));
CREATE POLICY "Users delete workspace documents" ON public.documents
    FOR DELETE USING (workspace_id IN (SELECT workspace_id FROM public.profiles WHERE profiles.id = auth.uid()));

-- Profiles: Update policy so users can view all profiles in their workspace
DROP POLICY IF EXISTS "Users can view own profile" ON public.profiles;
CREATE POLICY "Users can view profiles in their workspace" ON public.profiles
    FOR SELECT USING (
        id = auth.uid() OR 
        workspace_id IN (SELECT workspace_id FROM public.profiles p WHERE p.id = auth.uid())
    );
