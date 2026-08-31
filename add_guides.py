import re

with open('src/app/dashboard/page.tsx', 'r') as f:
    content = f.read()

# Tape Chart guide
content = content.replace(
    "<h2 style={{ fontSize: '14px', fontWeight: '800' }}>Habitaciones — Estado en Tiempo Real</h2>",
    "<h2 style={{ fontSize: '14px', fontWeight: '800' }}>Habitaciones — Estado en Tiempo Real</h2>\n                    <p style={{ fontSize: '11px', color: 'var(--text-500)', marginTop: '4px' }}>Aquí puedes ver el estado actual de todas las habitaciones de la sucursal seleccionada. Usa el botón 'Reservar' para registrar ingresos (walk-ins) o reservas anticipadas por noche o por horas.</p>"
)

# Housekeeping guide
content = content.replace(
    "<h2 style={{ fontSize: '14px', fontWeight: '800' }}>Housekeeping — Pisos</h2>",
    "<h2 style={{ fontSize: '14px', fontWeight: '800' }}>Housekeeping — Pisos</h2>\n                  <p style={{ fontSize: '11px', color: 'var(--text-500)', marginTop: '4px' }}>Gestiona el estado de limpieza de las habitaciones. El personal de limpieza puede marcar las habitaciones sucias como 'Limpias' para que estén disponibles nuevamente en recepción.</p>"
)

# Cash Shift guide
content = content.replace(
    "<h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>Arqueo de Caja (Turnos)</h2>",
    "<h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>Arqueo de Caja (Turnos)</h2>\n              <p style={{ fontSize: '11px', color: 'var(--text-500)', marginBottom: '16px' }}>Control de caja y turnos. Al finalizar su turno, el recepcionista declara el efectivo y pagos electrónicos cobrados. El sistema calcula si hay descuadres (Arqueo Ciego).</p>"
)

# CRM guide
content = content.replace(
    "<h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>CRM & Lealtad</h2>",
    "<h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>CRM & Lealtad</h2>\n              <p style={{ fontSize: '11px', color: 'var(--text-500)', marginBottom: '16px' }}>Base de datos de todos los huéspedes de la cadena. Aquí se acumulan los puntos de lealtad y se define el nivel (Bronce, Plata, Oro, Platino) de los clientes frecuentes.</p>"
)

# Users guide
content = content.replace(
    "<h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>Usuarios & Roles (RBAC)</h2>",
    "<h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>Usuarios & Roles (RBAC)</h2>\n              <p style={{ fontSize: '11px', color: 'var(--text-500)', marginBottom: '16px' }}>Administración del personal. Crea cuentas de acceso para tus empleados (recepcionistas, gerentes, limpieza) asignándoles roles que restringirán a qué partes del sistema pueden acceder.</p>"
)

with open('src/app/dashboard/page.tsx', 'w') as f:
    f.write(content)

