-- Drop old policies just in case they exist to avoid errors
DROP POLICY IF EXISTS branch_select_policy ON branches;
DROP POLICY IF EXISTS room_types_insert_policy ON room_types;
DROP POLICY IF EXISTS rooms_insert_policy ON rooms;
DROP POLICY IF EXISTS reservations_insert_policy ON reservations;
DROP POLICY IF EXISTS guests_insert_policy ON guests;

-- 1. Permitir leer sucursales (necesario para el RETURNING)
CREATE POLICY branch_select_policy ON branches
    FOR SELECT USING (
        organization_id = get_user_organization_id()
        OR get_user_organization_id() IS NULL
    );

-- 2. Asegurar inserts
CREATE POLICY room_types_insert_policy ON room_types
    FOR INSERT WITH CHECK (true);

CREATE POLICY rooms_insert_policy ON rooms
    FOR INSERT WITH CHECK (true);

CREATE POLICY reservations_insert_policy ON reservations
    FOR INSERT WITH CHECK (true);

CREATE POLICY guests_insert_policy ON guests
    FOR INSERT WITH CHECK (true);
