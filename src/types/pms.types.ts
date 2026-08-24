// TypeScript Types for Hotel PMS Multi-Tenant SaaS

export type SystemRole =
  | 'SUPER_ADMIN'
  | 'CHAIN_OWNER'
  | 'BRANCH_MANAGER'
  | 'RECEPTIONIST'
  | 'HOUSEKEEPING'
  | 'MAINTENANCE'
  | 'ACCOUNTANT';

export type RoomStatus =
  | 'AVAILABLE'
  | 'OCCUPIED'
  | 'CLEANING_IN_PROGRESS'
  | 'DIRTY_PENDING_CLEANING'
  | 'INSPECTION_PENDING'
  | 'MAINTENANCE_BLOCKED';

export type ReservationStatus =
  | 'CONFIRMED'
  | 'CHECKED_IN'
  | 'CHECKED_OUT'
  | 'CANCELLED'
  | 'NO_SHOW';

export type PaymentMethod =
  | 'CASH'
  | 'CREDIT_CARD_POS'
  | 'DEBIT_CARD_POS'
  | 'YAPE'
  | 'PLIN'
  | 'BANK_TRANSFER'
  | 'POINTS_REDEEM';

export type ModuleKey =
  | 'core_frontdesk'
  | 'housekeeping'
  | 'dynamic_pricing'
  | 'points_crm'
  | 'electronic_invoicing'
  | 'pos_room_charge'
  | 'whatsapp_bot';

export interface ModuleDefinition {
  key: ModuleKey;
  name: string;
  description: string;
  icon: string;
  isCore: boolean; // if true, cannot be disabled
}

export interface Organization {
  id: string;
  name: string;
  legalName?: string;
  taxId?: string; // RUC
  branches: Branch[];
  enabledModules: ModuleKey[];
}

export interface Branch {
  id: string;
  organizationId: string;
  name: string;
  code: string;
  city: string;
  address?: string;
  roomsCount: number;
  enabledModulesOverride?: ModuleKey[];
}

export interface RoomType {
  id: string;
  branchId: string;
  name: string;
  code: string;
  baseCapacity: number;
  basePrice: number;
  amenities: string[];
}

export interface Room {
  id: string;
  branchId: string;
  roomTypeId: string;
  roomTypeName: string;
  roomNumber: string;
  floorNumber: number;
  currentStatus: RoomStatus;
  isOperational: boolean;
  notes?: string;
  assignedHousekeeper?: string;
  cleaningMinutesSpent?: number;
}

export interface Guest {
  id: string;
  organizationId: string;
  firstName: string;
  lastName: string;
  documentType: 'DNI' | 'PASAPORTE' | 'CE';
  documentNumber: string;
  nationality: string;
  email: string;
  phone: string;
  loyaltyTier: 'BRONZE' | 'SILVER' | 'GOLD' | 'PLATINUM';
  pointsBalance: number;
  totalSpent: number;
  totalNightsStayed: number;
  isBlacklisted: boolean;
  blacklistReason?: string;
  preferences?: Record<string, string>;
}

export interface Reservation {
  id: string;
  branchId: string;
  guestId: string;
  guestName: string;
  guestDoc: string;
  roomId?: string;
  roomNumber?: string;
  roomTypeId: string;
  roomTypeName: string;
  code: string;
  checkInDate: string; // YYYY-MM-DD
  checkOutDate: string; // YYYY-MM-DD
  status: ReservationStatus;
  adultsCount: number;
  childrenCount: number;
  totalPrice: number;
  bookingSource: 'DIRECT_DESK' | 'DIRECT_WEB' | 'WHATSAPP' | 'BOOKING' | 'AIRBNB';
}

export interface CashShift {
  id: string;
  branchId: string;
  userName: string;
  shiftName: string;
  openedAt: string;
  closedAt?: string;
  initialCash: number;
  isClosed: boolean;
  systemCash: number;
  systemPos: number;
  systemYapePlin: number;
  systemTransfers: number;
  declaredCash?: number;
  declaredPos?: number;
  declaredYapePlin?: number;
  declaredTransfers?: number;
  cashDifference?: number;
}

export interface MaintenanceTicket {
  id: string;
  branchId: string;
  roomNumber: string;
  title: string;
  description: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'EMERGENCY';
  photoUrl?: string;
  isResolved: boolean;
  reportedBy: string;
  reportedAt: string;
}
