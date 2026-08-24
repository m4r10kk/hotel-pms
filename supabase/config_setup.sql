-- Allow selecting and inserting room_types
CREATE POLICY org_isolation_policy_room_types ON room_types
    FOR ALL USING (
        branch_id IN (SELECT id FROM branches WHERE organization_id = get_user_organization_id())
    );

-- Allow seeing user profiles for the same organization
CREATE POLICY org_isolation_policy_user_profiles ON user_profiles
    FOR SELECT USING (
        organization_id = get_user_organization_id()
    );

-- Allow super admins to invite/insert users (This assumes we use a backend or allow direct inserts if auth.users could be bypassed. But since auth.users handles login, users must be created via Supabase Auth Admin API. For now, we will just allow them to update roles of existing profiles)
CREATE POLICY admin_update_user_profiles ON user_profiles
    FOR UPDATE USING (
        organization_id = get_user_organization_id() AND
        (SELECT system_role FROM user_profiles WHERE id = auth.uid()) = 'SUPER_ADMIN'
    );
