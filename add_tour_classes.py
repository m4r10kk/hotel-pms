import re

with open('src/app/dashboard/page.tsx', 'r') as f:
    content = f.read()

# Add import
content = content.replace(
    "import SettingsView from './SettingsView'",
    "import SettingsView from './SettingsView'\nimport TourGuide from './TourGuide'"
)

# Add component at the end of the Dashboard return
content = content.replace(
    "    </div>\n  )\n}",
    "      <TourGuide view={activeView} />\n    </div>\n  )\n}"
)

# 1. Tapechart classes
content = content.replace(
    "<div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px', marginBottom: '24px' }}>",
    "<div className=\"tour-tapechart-metrics\" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px', marginBottom: '24px' }}>",
    1
)
content = content.replace(
    "{/* Rooms Table */}\n              {rooms.length === 0 ? (",
    "{/* Rooms Table */}\n              <div className=\"tour-tapechart-rooms\">\n              {rooms.length === 0 ? (",
    1
)
content = content.replace(
    "              {/* Reservations */}",
    "              </div>\n              {/* Reservations */}",
    1
)
content = content.replace(
    "{/* Reservations */}\n              {reservations.length > 0 && (",
    "{/* Reservations */}\n              <div className=\"tour-tapechart-res\">\n              {reservations.length > 0 && (",
    1
)

# Fix the end of tapechart
def replace_nth(string, old, new, n):
    parts = string.split(old)
    if len(parts) <= n:
        return string
    return old.join(parts[:n]) + new + old.join(parts[n:])

content = replace_nth(content, "            </div>\n          )}", "              </div>\n            </div>\n          )}", 2)


# 2. Housekeeping classes
content = content.replace(
    "<div style={{ overflowX: 'auto' }}>\n                    <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: '400px' }}>\n                      <thead>\n                        <tr style={{ background: 'var(--bg-700)' }}>\n                          {['Habitación', 'Estado Actual', 'Acción'].map",
    "<div className=\"tour-housekeeping-list\" style={{ overflowX: 'auto' }}>\n                    <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: '400px' }}>\n                      <thead>\n                        <tr style={{ background: 'var(--bg-700)' }}>\n                          {['Habitación', 'Estado Actual', 'Acción'].map",
    1
)

# 3. Cash Shift classes
content = content.replace(
    "            <div className=\"animate-fadeUp\" style={{ display: 'grid', gap: '24px' }}>\n              <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>\n                <h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>Arqueo de Caja (Turnos)</h2>",
    "            <div className=\"animate-fadeUp\" style={{ display: 'grid', gap: '24px' }}>\n              <div className=\"tour-cash-form\" style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>\n                <h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>Arqueo de Caja (Turnos)</h2>",
    1
)

# 4. CRM classes
content = content.replace(
    "            <div className=\"animate-fadeUp\" style={{ display: 'grid', gap: '24px' }}>\n              <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>\n                <h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>CRM & Lealtad</h2>",
    "            <div className=\"animate-fadeUp tour-crm-list\" style={{ display: 'grid', gap: '24px' }}>\n              <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>\n                <h2 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '4px' }}>CRM & Lealtad</h2>",
    1
)

# 5. Users classes
content = content.replace(
    "          {activeView === 'users' && (\n            <div className=\"animate-fadeUp\" style={{ display: 'grid', gap: '24px' }}>\n              <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>",
    "          {activeView === 'users' && (\n            <div className=\"animate-fadeUp tour-users-form\" style={{ display: 'grid', gap: '24px' }}>\n              <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>",
    1
)

with open('src/app/dashboard/page.tsx', 'w') as f:
    f.write(content)
