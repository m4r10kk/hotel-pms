import { ModuleDefinition, ModuleKey, Organization, Branch } from '@/types/pms.types';

export const AVAILABLE_MODULES: ModuleDefinition[] = [
  {
    key: 'core_frontdesk',
    name: 'Front Desk & Calendario',
    description: 'Tape Chart interactivo, motor de reservas, check-in express y folios maestros.',
    icon: 'LayoutDashboard',
    isCore: true,
  },
  {
    key: 'housekeeping',
    name: 'Housekeeping & Mantenimiento Móvil',
    description: 'App para camareras con tiempos de limpieza, fotos de averías y control de minibar.',
    icon: 'Sparkles',
    isCore: false,
  },
  {
    key: 'dynamic_pricing',
    name: 'Tarifas Dinámicas & Temporadas',
    description: 'Precios por temporada, días laborables vs fines de semana y blindaje de descuentos.',
    icon: 'TrendingUp',
    isCore: false,
  },
  {
    key: 'points_crm',
    name: 'CRM de Huéspedes & Programa de Puntos',
    description: 'Ficha única, acumulación y canje de puntos, niveles VIP y lista de alertas.',
    icon: 'Award',
    isCore: false,
  },
  {
    key: 'pos_room_charge',
    name: 'Punto de Venta & Room Charge',
    description: 'Carga de consumos de restaurante, cafetería o minibar a la cuenta del cuarto.',
    icon: 'UtensilsCrossed',
    isCore: false,
  },
  {
    key: 'electronic_invoicing',
    name: 'Facturación Electrónica SUNAT',
    description: 'Emisión directa de Boletas, Facturas y Notas de Crédito con 1 clic.',
    icon: 'Receipt',
    isCore: false,
  },
  {
    key: 'whatsapp_bot',
    name: 'Automatización por WhatsApp',
    description: 'Confirmaciones automáticas con GPS, clave WiFi y pre-checkin web.',
    icon: 'MessageSquare',
    isCore: false,
  },
];

/**
 * Checks if a specific module is active for an organization / branch
 */
export function isModuleEnabled(
  moduleKey: ModuleKey,
  org: Organization,
  branch?: Branch
): boolean {
  if (moduleKey === 'core_frontdesk') return true; // Core is always active

  // Check branch level override first if present
  if (branch?.enabledModulesOverride && branch.enabledModulesOverride.length > 0) {
    return branch.enabledModulesOverride.includes(moduleKey);
  }

  // Fallback to organization level enabled modules
  return org.enabledModules.includes(moduleKey);
}
