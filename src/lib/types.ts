export type RoomStatus =
  | 'AVAILABLE'
  | 'OCCUPIED'
  | 'CLEANING_IN_PROGRESS'
  | 'DIRTY_PENDING_CLEANING'
  | 'INSPECTION_PENDING'
  | 'MAINTENANCE_BLOCKED'

export type ReservationStatus =
  | 'CONFIRMED'
  | 'CHECKED_IN'
  | 'CHECKED_OUT'
  | 'CANCELLED'
  | 'NO_SHOW'

export interface Organization {
  id: string
  name: string
  legal_name: string | null
  tax_id: string | null
  contact_email: string | null
  contact_phone: string | null
  is_active: boolean
  created_at: string
}

export interface Branch {
  id: string
  organization_id: string
  name: string
  code: string
  address: string | null
  city: string | null
  country: string
  is_active: boolean
  created_at: string
}

export interface Room {
  id: string
  branch_id: string
  room_number: string
  room_type: string
  floor: number | null
  capacity: number
  status: RoomStatus
  is_clean: boolean
  base_rate: number
  created_at: string
}

export interface Reservation {
  id: string
  branch_id: string
  room_id: string
  guest_id: string
  status: ReservationStatus
  check_in_date: string
  check_out_date: string
  total_amount: number
  created_at: string
  guests?: Guest
  rooms?: Room
}

export interface Guest {
  id: string
  organization_id: string
  first_name: string
  last_name: string
  document_type: string
  document_number: string
  email: string | null
  phone: string | null
  loyalty_points: number
  loyalty_tier: string
  created_at: string
}

export interface CashShift {
  id: string
  branch_id: string
  shift_code: string
  status: string
  declared_cash: number
  system_cash: number
  difference_amount: number
  created_at: string
}
