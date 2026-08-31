-- Fix Branches RLS
CREATE POLICY branch_select_policy ON branches
    FOR SELECT USING (
        organization_id = get_user_organization_id()
        OR get_user_organization_id() IS NULL
    );

CREATE POLICY branch_update_policy ON branches
    FOR UPDATE USING (
        organization_id = get_user_organization_id()
    );

-- Fix Room Types RLS for insert
CREATE POLICY room_types_insert_policy ON room_types
    FOR INSERT WITH CHECK (
        branch_id IN (SELECT id FROM branches WHERE organization_id = get_user_organization_id())
    );

-- Fix Rooms RLS for insert
CREATE POLICY rooms_insert_policy ON rooms
    FOR INSERT WITH CHECK (
        branch_id IN (SELECT id FROM branches WHERE organization_id = get_user_organization_id())
    );

-- Fix Reservations RLS for insert
CREATE POLICY reservations_insert_policy ON reservations
    FOR INSERT WITH CHECK (
        branch_id IN (SELECT id FROM branches WHERE organization_id = get_user_organization_id())
    );

-- Fix Guests RLS for insert
CREATE POLICY guests_insert_policy ON guests
    FOR INSERT WITH CHECK (
        organization_id = get_user_organization_id()
    );
