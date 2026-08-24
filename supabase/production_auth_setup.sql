-- Add production-grade RLS and User creation triggers

-- 1. Trigger to automatically create a user_profile when a user is created in auth.users
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.user_profiles (id, full_name, email, system_role)
  VALUES (
    new.id, 
    COALESCE(new.raw_user_meta_data->>'full_name', 'Nuevo Usuario'),
    new.email,
    'SUPER_ADMIN' -- Giving SUPER_ADMIN to the first users for setup
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if trigger exists and drop it before creating to avoid errors
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- 2. Policies for organizations (Allow authenticated users to create and view their orgs)
-- Users can see orgs they belong to
CREATE POLICY org_select_policy ON organizations
    FOR SELECT USING (
        id = get_user_organization_id() 
        OR get_user_organization_id() IS NULL -- Allow seeing if they don't have an org yet (for setup)
    );

-- Allow authenticated users to create an organization (they will become the owner implicitly)
CREATE POLICY org_insert_policy ON organizations
    FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);

-- 3. Policies for branches
CREATE POLICY branch_insert_policy ON branches
    FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);
    
-- 4. Enable RLS on everything just to be absolutely sure
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE branches ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
-- Allow users to update their own profile
CREATE POLICY user_profile_update_policy ON user_profiles
    FOR UPDATE USING (id = auth.uid());
