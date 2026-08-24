-- ==============================================================================
-- HOTEL PMS SAAS - MULTI-TENANT & MULTI-BRANCH SCHEMA
-- PostgreSQL Schema with Row-Level Security (RLS), Triggers, & Realtime Support
-- ==============================================================================

-- 1. ENUMS
CREATE TYPE user_system_role AS ENUM (
    'SUPER_ADMIN',
    'CHAIN_OWNER',
    'BRANCH_MANAGER',
    'RECEPTIONIST',
    'HOUSEKEEPING',
    'MAINTENANCE',
    'ACCOUNTANT'
);

CREATE TYPE room_status AS ENUM (
    'AVAILABLE',
    'OCCUPIED',
    'CLEANING_IN_PROGRESS',
    'DIRTY_PENDING_CLEANING',
    'INSPECTION_PENDING',
    'MAINTENANCE_BLOCKED'
);

CREATE TYPE reservation_status AS ENUM (
    'CONFIRMED',
    'CHECKED_IN',
    'CHECKED_OUT',
    'CANCELLED',
    'NO_SHOW'
);

CREATE TYPE payment_method AS ENUM (
    'CASH',
    'CREDIT_CARD_POS',
    'DEBIT_CARD_POS',
    'YAPE',
    'PLIN',
    'BANK_TRANSFER',
    'POINTS_REDEEM'
);

CREATE TYPE invoice_type AS ENUM (
    'BOLETA',
    'FACTURA',
    'NOTA_CREDITO',
    'TICKET_INTERNO'
);

CREATE TYPE maintenance_priority AS ENUM (
    'LOW',
    'MEDIUM',
    'HIGH',
    'EMERGENCY'
);

-- ==============================================================================
-- 2. TENANT HIERARCHY & SUBSCRIPTIONS
-- ==============================================================================

-- Organizations (Empresas / Cadenas Hoteleras)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    legal_name VARCHAR(255),
    tax_id VARCHAR(50), -- RUC en Perú
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Branches (Hoteles / Sedes físicas)
CREATE TABLE branches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL, -- ej. 'MIRAFLORES', 'CUSCO'
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Peru',
    phone VARCHAR(50),
    check_in_time TIME DEFAULT '14:00:00',
    check_out_time TIME DEFAULT '12:00:00',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(organization_id, code)
);

-- Organization Feature Flags (Módulos Opcionales por Empresa/Sede)
CREATE TABLE organization_modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    branch_id UUID REFERENCES branches(id) ON DELETE CASCADE, -- Si es null aplica a toda la org
    module_key VARCHAR(100) NOT NULL, 
    -- 'core_frontdesk', 'housekeeping', 'dynamic_pricing', 'points_crm', 'electronic_invoicing', 'pos_room_charge', 'whatsapp_bot'
    is_enabled BOOLEAN DEFAULT FALSE,
    config JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(organization_id, branch_id, module_key)
);

-- Users (Perfiles vinculados a Supabase Auth)
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY, -- Maps to auth.users.id
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    system_role user_system_role NOT NULL DEFAULT 'RECEPTIONIST',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Asignación de Usuarios a Sucursales Específicas
CREATE TABLE user_branch_access (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    role_in_branch user_system_role NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, branch_id)
);

-- ==============================================================================
-- 3. HABITACIONES, CATEGORÍAS & TARIFAS
-- ==============================================================================

CREATE TABLE room_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL, -- ej. 'Simple', 'Matrimonial King', 'Suite Familiar'
    code VARCHAR(20) NOT NULL,
    description TEXT,
    base_capacity INT NOT NULL DEFAULT 2,
    max_capacity INT NOT NULL DEFAULT 2,
    base_price NUMERIC(10, 2) NOT NULL,
    amenities JSONB DEFAULT '[]'::jsonb, -- ['A/C', 'Jacuzzi', 'Vista al Mar', 'Smart TV']
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(branch_id, code)
);

CREATE TABLE rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    room_type_id UUID NOT NULL REFERENCES room_types(id) ON DELETE RESTRICT,
    room_number VARCHAR(20) NOT NULL,
    floor_number INT NOT NULL DEFAULT 1,
    current_status room_status NOT NULL DEFAULT 'AVAILABLE',
    is_operational BOOLEAN DEFAULT TRUE,
    notes TEXT,
    last_cleaned_at TIMESTAMPTZ,
    last_cleaned_by UUID REFERENCES user_profiles(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(branch_id, room_number)
);

-- Tarifario Dinámico y Temporadas
CREATE TABLE rate_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    room_type_id UUID REFERENCES room_types(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL, -- 'Temporada Alta Verano', 'Tarifa Corporativa'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    day_of_week INT[] DEFAULT '{0,1,2,3,4,5,6}', -- 0=Domingo, 6=Sábado
    multiplier NUMERIC(4, 2) DEFAULT 1.0, -- ej. 1.25 para +25%
    override_price NUMERIC(10, 2),
    extra_person_fee NUMERIC(10, 2) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 4. CRM DE HUÉSPEDES & PROGRAMA DE PUNTOS
-- ==============================================================================

CREATE TABLE guests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    document_type VARCHAR(20) DEFAULT 'DNI', -- 'DNI', 'PASAPORTE', 'CE'
    document_number VARCHAR(50) NOT NULL,
    nationality VARCHAR(100) DEFAULT 'Peruana',
    email VARCHAR(255),
    phone VARCHAR(50),
    is_blacklisted BOOLEAN DEFAULT FALSE,
    blacklist_reason TEXT,
    loyalty_tier VARCHAR(50) DEFAULT 'BRONZE', -- 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM'
    points_balance INT DEFAULT 0,
    total_spent NUMERIC(12, 2) DEFAULT 0.0,
    total_nights_stayed INT DEFAULT 0,
    preferences JSONB DEFAULT '{}'::jsonb, -- {'pillow_type': 'plumas', 'floor': 'alto'}
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(organization_id, document_number)
);

CREATE TABLE loyalty_points_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id UUID NOT NULL REFERENCES guests(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    points_change INT NOT NULL, -- positivo para acumulación, negativo para canje
    action_type VARCHAR(50) NOT NULL, -- 'NIGHT_ACCRUAL', 'MINIBAR_ACCRUAL', 'REDEMPTION_DISCOUNT'
    reference_id UUID, -- reference to reservation_id or payment_id
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 5. RESERVAS, CHECK-IN & FOLIOS
-- ==============================================================================

CREATE TABLE reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    guest_id UUID NOT NULL REFERENCES guests(id) ON DELETE RESTRICT,
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,
    room_type_id UUID NOT NULL REFERENCES room_types(id) ON DELETE RESTRICT,
    code VARCHAR(50) NOT NULL UNIQUE,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    actual_check_in_at TIMESTAMPTZ,
    actual_check_out_at TIMESTAMPTZ,
    status reservation_status NOT NULL DEFAULT 'CONFIRMED',
    adults_count INT DEFAULT 2,
    children_count INT DEFAULT 0,
    total_price NUMERIC(10, 2) NOT NULL,
    booking_source VARCHAR(50) DEFAULT 'DIRECT_DESK', -- 'DIRECT_DESK', 'DIRECT_WEB', 'WHATSAPP', 'BOOKING', 'AIRBNB'
    created_by UUID REFERENCES user_profiles(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Acompañantes en la reserva
CREATE TABLE reservation_guests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id UUID NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(20) DEFAULT 'DNI',
    document_number VARCHAR(50) NOT NULL,
    nationality VARCHAR(100),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Folios de Cuenta (Cuenta maestra de la habitación)
CREATE TABLE folios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id UUID NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    total_charges NUMERIC(10, 2) DEFAULT 0.0,
    total_payments NUMERIC(10, 2) DEFAULT 0.0,
    balance NUMERIC(10, 2) DEFAULT 0.0, -- total_charges - total_payments
    is_closed BOOLEAN DEFAULT FALSE,
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ítems de Cobro en Folio (Habitación, Minibar, Restaurante, Lavandería)
CREATE TABLE folio_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    folio_id UUID NOT NULL REFERENCES folios(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL, -- 'ROOM_RATE', 'MINIBAR', 'RESTAURANT', 'EARLY_CHECKIN', 'LATE_CHECKOUT', 'DAMAGE_FEE'
    description VARCHAR(255) NOT NULL,
    quantity INT DEFAULT 1,
    unit_price NUMERIC(10, 2) NOT NULL,
    total_price NUMERIC(10, 2) NOT NULL,
    created_by UUID REFERENCES user_profiles(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 6. CAJA, TURNOS, PAGOS & FACTURACIÓN SUNAT
-- ==============================================================================

-- Arqueo Ciego de Turnos de Caja
CREATE TABLE cash_shifts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES user_profiles(id),
    shift_name VARCHAR(50) NOT NULL, -- 'TURNO_MANANA', 'TURNO_TARDE', 'TURNO_NOCHE'
    opened_at TIMESTAMPTZ DEFAULT NOW(),
    closed_at TIMESTAMPTZ,
    initial_cash NUMERIC(10, 2) DEFAULT 0.0,
    -- Declaraciones Ciegas al Cierre
    declared_cash NUMERIC(10, 2),
    declared_pos NUMERIC(10, 2),
    declared_yape_plin NUMERIC(10, 2),
    declared_transfers NUMERIC(10, 2),
    -- Totales Calculados por Sistema
    system_cash NUMERIC(10, 2) DEFAULT 0.0,
    system_pos NUMERIC(10, 2) DEFAULT 0.0,
    system_yape_plin NUMERIC(10, 2) DEFAULT 0.0,
    system_transfers NUMERIC(10, 2) DEFAULT 0.0,
    cash_difference NUMERIC(10, 2) DEFAULT 0.0,
    is_closed BOOLEAN DEFAULT FALSE,
    supervisor_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Pagos Registrados
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    folio_id UUID NOT NULL REFERENCES folios(id) ON DELETE RESTRICT,
    cash_shift_id UUID REFERENCES cash_shifts(id),
    amount NUMERIC(10, 2) NOT NULL,
    method payment_method NOT NULL,
    operation_reference VARCHAR(100), -- Código de voucher o transferencia Yape
    invoice_type invoice_type DEFAULT 'BOLETA',
    invoice_series VARCHAR(10), -- ej. 'B001', 'F001'
    invoice_number VARCHAR(20),
    sunat_status VARCHAR(50) DEFAULT 'PENDING', -- 'PENDING', 'ACCEPTED', 'REJECTED'
    sunat_response_message TEXT,
    created_by UUID REFERENCES user_profiles(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 7. HOUSEKEEPING & MANTENIMIENTO
-- ==============================================================================

CREATE TABLE housekeeping_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    housekeeper_id UUID NOT NULL REFERENCES user_profiles(id),
    started_at TIMESTAMPTZ DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    duration_minutes INT,
    status_before room_status,
    status_after room_status,
    inspected_by UUID REFERENCES user_profiles(id),
    notes TEXT
);

CREATE TABLE maintenance_tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    reported_by UUID NOT NULL REFERENCES user_profiles(id),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority maintenance_priority DEFAULT 'MEDIUM',
    photo_urls JSONB DEFAULT '[]'::jsonb,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMPTZ,
    resolved_by UUID REFERENCES user_profiles(id),
    resolution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 8. AUDITORÍA INMUTABLE (AUDIT LOGS)
-- ==============================================================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    branch_id UUID REFERENCES branches(id) ON DELETE CASCADE,
    user_id UUID REFERENCES user_profiles(id),
    action VARCHAR(100) NOT NULL, -- 'DISCOUNT_APPLIED', 'PRICE_OVERRIDE', 'RESERVATION_CANCELLED', 'MANUAL_STATUS_CHANGE'
    entity_table VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,
    old_data JSONB,
    new_data JSONB,
    ip_address VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 9. ROW-LEVEL SECURITY (RLS) POLICIES
-- ==============================================================================

ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE branches ENABLE ROW LEVEL SECURITY;
ALTER TABLE organization_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE room_types ENABLE ROW LEVEL SECURITY;
ALTER TABLE reservations ENABLE ROW LEVEL SECURITY;
ALTER TABLE folios ENABLE ROW LEVEL SECURITY;
ALTER TABLE folio_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE cash_shifts ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE guests ENABLE ROW LEVEL SECURITY;
ALTER TABLE housekeeping_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE maintenance_tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Helper function to get current user organization
CREATE OR REPLACE FUNCTION get_user_organization_id()
RETURNS UUID AS $$
BEGIN
    RETURN (SELECT organization_id FROM user_profiles WHERE id = auth.uid());
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- RLS Policy: Users can only see data belonging to their organization
CREATE POLICY org_isolation_policy_rooms ON rooms
    FOR ALL USING (
        branch_id IN (SELECT id FROM branches WHERE organization_id = get_user_organization_id())
    );

CREATE POLICY org_isolation_policy_reservations ON reservations
    FOR ALL USING (
        branch_id IN (SELECT id FROM branches WHERE organization_id = get_user_organization_id())
    );

CREATE POLICY org_isolation_policy_guests ON guests
    FOR ALL USING (
        organization_id = get_user_organization_id()
    );

CREATE POLICY org_isolation_policy_cash_shifts ON cash_shifts
    FOR ALL USING (
        branch_id IN (SELECT id FROM branches WHERE organization_id = get_user_organization_id())
    );
