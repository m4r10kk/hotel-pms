#!/bin/bash

# Define the new view logic
cat << 'INNER_EOF' > /Users/marlok/Desktop/California/users_view.txt
          {/* ══ USERS ══ */}
          {activeView === 'users' && (
            <div className="animate-fadeUp" style={{ display: 'grid', gap: '24px' }}>
              <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
                <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '16px' }}>Crear Nuevo Empleado</h2>
                <form onSubmit={handleCreateEmployee} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>NOMBRE</label>
                    <input type="text" className="form-input" placeholder="Ej: Juan Perez" value={empName} onChange={e => setEmpName(e.target.value)} required />
                  </div>
                  <div>
                    <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>CORREO</label>
                    <input type="email" className="form-input" placeholder="juan@hotel.com" value={empEmail} onChange={e => setEmpEmail(e.target.value)} required />
                  </div>
                  <div>
                    <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>CONTRASEÑA TEMPORAL</label>
                    <input type="text" className="form-input" placeholder="Ej: temporal123" value={empPass} onChange={e => setEmpPass(e.target.value)} required />
                  </div>
                  <div>
                    <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>ROL</label>
                    <select className="form-input" value={empRole} onChange={e => setEmpRole(e.target.value)} required>
                      <option value="FRONT_DESK">Recepción (Front Desk)</option>
                      <option value="HOUSEKEEPING">Limpieza (Housekeeping)</option>
                      <option value="SUPER_ADMIN">Administrador</option>
                    </select>
                  </div>
                  <button type="submit" disabled={empLoading} style={{ background: 'var(--orange)', color: '#fff', padding: '10px 16px', borderRadius: '8px', fontSize: '12px', fontWeight: '700', border: 'none', cursor: 'pointer' }}>
                    {empLoading ? 'Creando...' : 'Crear Empleado'}
                  </button>
                </form>
              </div>

              <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
                <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '16px' }}>Personal de la Empresa</h2>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ background: 'var(--bg-700)' }}>
                      {['Usuario', 'Rol', 'Empresa', 'Estado'].map(h => (
                        <th key={h} style={{ padding: '10px 14px', fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-500)', textAlign: 'left', borderBottom: '1px solid var(--border-subtle)' }}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {users.map(u => (
                      <tr key={u.id}>
                        <td style={{ padding: '12px 14px', fontWeight: '800' }}>{u.full_name} <br/><span style={{fontSize:'10px', color:'var(--text-500)', fontWeight:400}}>{u.email}</span></td>
                        <td style={{ padding: '12px 14px' }}><span className="pill pill-orange">{u.system_role}</span></td>
                        <td style={{ padding: '12px 14px', color: 'var(--text-300)', fontSize: '12.5px' }}>{orgs.find(o => o.id === u.organization_id)?.name}</td>
                        <td style={{ padding: '12px 14px' }}><span className="pill pill-emerald">{u.is_active ? 'Activo' : 'Inactivo'}</span></td>
                      </tr>
                    ))}
                    {users.length === 0 && (
                      <tr><td colSpan={4} style={{ padding: '12px 14px', color: 'var(--text-500)' }}>No hay usuarios</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
INNER_EOF

# Add the import for createEmployee
sed -i '' 's/import SettingsView from '"'"'.\/SettingsView'"'"'/import SettingsView from '"'"'.\/SettingsView'"'"'\nimport { createEmployee } from '"'"'@\/app\/actions\/users'"'"'/g' src/app/dashboard/page.tsx

# Add state variables for the employee form
sed -i '' 's/const \[users, setUsers\] = useState<any\[\]>(\[\])/const [users, setUsers] = useState<any[]>([])\n\n  const [empName, setEmpName] = useState('"'"''"'"')\n  const [empEmail, setEmpEmail] = useState('"'"''"'"')\n  const [empPass, setEmpPass] = useState('"'"''"'"')\n  const [empRole, setEmpRole] = useState('"'"'FRONT_DESK'"'"')\n  const [empLoading, setEmpLoading] = useState(false)/g' src/app/dashboard/page.tsx

