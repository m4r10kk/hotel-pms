with open('src/app/dashboard/page.tsx', 'r') as f:
    content = f.read()

bad_tbody = """                <tbody>
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
                </tbody>"""

import re
# We can find them based on the text before them.
def replace_after(content, search_text, new_tbody):
    idx = content.find(search_text)
    if idx == -1: return content
    
    start_tbody = content.find("<tbody>", idx)
    end_tbody = content.find("</tbody>", start_tbody) + len("</tbody>")
    
    if start_tbody == -1 or end_tbody == -1: return content
    
    return content[:start_tbody] + new_tbody + content[end_tbody:]

# 1. Tape chart rooms
content = replace_after(content, "Habitaciones — Estado en Tiempo Real", """<tbody>
                        {rooms.map(rm => {
                          const rt = roomTypes.find(t => t.id === (rm as any).room_type_id)
                          return (
                            <tr key={rm.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.2s', cursor: 'default' }} onMouseEnter={e => e.currentTarget.style.background='var(--bg-700)'} onMouseLeave={e => e.currentTarget.style.background='transparent'}>
                              <td style={{ padding: '14px 16px', fontWeight: '800', color: 'var(--text-100)' }}>Hab. {rm.room_number}</td>
                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{rt?.name ?? rm.room_type}</td>
                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{rm.floor_number}</td>
                              <td style={{ padding: '14px 16px' }}><span className={`pill pill-${rm.current_status === 'AVAILABLE' ? 'emerald' : rm.current_status === 'OCCUPIED' ? 'orange' : 'amber'}`}>{rm.current_status}</span></td>
                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>S/. {rt?.base_price ?? rm.base_rate}</td>
                              <td style={{ padding: '14px 16px' }}>
                                {rm.current_status === 'AVAILABLE' && (
                                  <button onClick={() => { setResRoomId(rm.id); setShowReservationModal(true) }} style={{ background: 'rgba(255,107,0,0.15)', border: '1px solid rgba(255,107,0,0.3)', color: 'var(--orange)', padding: '6px 14px', borderRadius: '8px', fontSize: '11px', fontWeight: 800, cursor: 'pointer', transition: 'all 0.2s' }}>Reservar</button>
                                )}
                              </td>
                            </tr>
                          )
                        })}
                      </tbody>""")

# 2. Tape chart reservations
content = replace_after(content, "Reservas en Curso", """<tbody>
                        {reservations.map(res => {
                          const rm = rooms.find(r => r.id === res.room_id)
                          return (
                            <tr key={res.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.2s' }} onMouseEnter={e => e.currentTarget.style.background='var(--bg-700)'} onMouseLeave={e => e.currentTarget.style.background='transparent'}>
                              <td style={{ padding: '14px 16px', fontWeight: '800', color: 'var(--text-100)' }}>
                                {(res as any).guests?.first_name} {(res as any).guests?.last_name}
                                {res.stay_type === 'HORAS' && <span className="pill pill-amber" style={{marginLeft: '6px'}}>HORAS</span>}
                              </td>
                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>Hab. {rm?.room_number}</td>
                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{res.stay_type === 'HORAS' ? (res as any).check_in_time : res.check_in_date}</td>
                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{res.stay_type === 'HORAS' ? (res as any).check_out_time : res.check_out_date}</td>
                              <td style={{ padding: '14px 16px', color: 'var(--orange)', fontWeight: '700' }}>S/. {res.total_amount || (res as any).total_price || 0}</td>
                              <td style={{ padding: '14px 16px' }}><span className="pill pill-emerald">{res.status}</span></td>
                            </tr>
                          )
                        })}
                      </tbody>""")

# 3. Housekeeping
content = replace_after(content, "Estado de Limpieza", """<tbody>
                        {rooms.filter(r => r.current_status.includes('DIRTY') || r.current_status.includes('CLEANING')).map(rm => (
                          <tr key={rm.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.2s' }}>
                            <td style={{ padding: '14px 16px', fontWeight: '800', color: 'var(--text-100)' }}>Hab. {rm.room_number}</td>
                            <td style={{ padding: '14px 16px' }}><span className="pill pill-amber">{rm.current_status}</span></td>
                            <td style={{ padding: '14px 16px' }}><button style={{ background: 'var(--emerald)', color: '#fff', border: 'none', padding: '6px 14px', borderRadius: '8px', fontSize: '11px', fontWeight: 800, cursor: 'pointer', transition: 'all 0.2s' }}>Marcar Limpia</button></td>
                          </tr>
                        ))}
                        {rooms.filter(r => r.current_status.includes('DIRTY') || r.current_status.includes('CLEANING')).length === 0 && (
                          <tr><td colSpan={3} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-500)', fontSize: '13px' }}>Todo limpio ✨</td></tr>
                        )}
                      </tbody>""")

# 4. Cash Shift
content = replace_after(content, "Arqueo de Caja (Turnos)", """<tbody>
                        <tr><td colSpan={5} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-500)', fontSize: '13px' }}>No hay turnos registrados.</td></tr>
                      </tbody>""")

# 5. CRM
content = replace_after(content, "CRM & Lealtad", """<tbody>
                        {guests.map(g => (
                          <tr key={g.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.2s' }} onMouseEnter={e => e.currentTarget.style.background='var(--bg-700)'} onMouseLeave={e => e.currentTarget.style.background='transparent'}>
                            <td style={{ padding: '14px 16px', fontWeight: '800', color: 'var(--text-100)' }}>{g.first_name} {g.last_name}</td>
                            <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{g.document_type} {g.document_number}</td>
                            <td style={{ padding: '14px 16px' }}><span className="pill pill-emerald">{g.loyalty_tier}</span></td>
                            <td style={{ padding: '14px 16px', color: 'var(--orange)', fontWeight: '700' }}>{g.loyalty_points} pts</td>
                            <td style={{ padding: '14px 16px', color: 'var(--text-400)', fontSize: '12px' }}>{g.email || g.phone || '—'}</td>
                          </tr>
                        ))}
                      </tbody>""")

with open('src/app/dashboard/page.tsx', 'w') as f:
    f.write(content)

print("Tables fixed.")
