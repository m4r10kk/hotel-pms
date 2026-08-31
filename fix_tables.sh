#!/bin/bash
set -e

# Extract up to Rooms Table thead
awk '/{..Habitación., .Tipo., .Piso., .Estado., .Tarifa Base., .Acción.}.map\(h => \(/ {print; getline; print; getline; print; getline; print; exit}' src/app/dashboard/page.tsx > p1.txt

# Create Rooms Table tbody
cat << 'INNER_EOF' > p2.txt
                      <tbody>
                        {rooms.map(rm => (
                          <tr key={rm.id}>
                            <td style={{ padding: '12px 14px', fontWeight: '800' }}>Hab. {rm.room_number}</td>
                            <td style={{ padding: '12px 14px', color: 'var(--text-300)' }}>{rm.room_type}</td>
                            <td style={{ padding: '12px 14px' }}>{rm.floor}</td>
                            <td style={{ padding: '12px 14px' }}><span className={`pill pill-${rm.status === 'AVAILABLE' ? 'emerald' : rm.status === 'OCCUPIED' ? 'orange' : 'amber'}`}>{rm.status}</span></td>
                            <td style={{ padding: '12px 14px' }}>S/. {rm.base_rate}</td>
                            <td style={{ padding: '12px 14px' }}>
                              {rm.status === 'AVAILABLE' && (
                                <button onClick={() => { setResRoomId(rm.id); setShowReservationModal(true) }} style={{ background: 'var(--bg-600)', border: '1px solid var(--border-subtle)', color: 'var(--text-300)', padding: '5px 10px', borderRadius: '6px', fontSize: '11px', cursor: 'pointer' }}>Reservar</button>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Reservations */}
              {reservations.length > 0 && (
                <div style={{ ...card, padding: 0, overflow: 'hidden', marginTop: '16px' }}>
                  <div style={{ padding: '16px 18px', borderBottom: '1px solid var(--border-subtle)' }}>
                    <h2 style={{ fontSize: '14px', fontWeight: '800' }}>Reservas Activas</h2>
                  </div>
                  <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: '560px' }}>
                      <thead>
                        <tr style={{ background: 'var(--bg-700)' }}>
                          {['Huésped', 'Habitación', 'Check-in', 'Check-out', 'Total', 'Estado'].map(h => (
                            <th key={h} style={{ padding: '11px 14px', fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-500)', textAlign: 'left', borderBottom: '1px solid var(--border-subtle)' }}>{h}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {reservations.map(res => {
                          const rm = rooms.find(r => r.id === res.room_id)
                          return (
                            <tr key={res.id}>
                              <td style={{ padding: '12px 14px', fontWeight: '800' }}>
                                {res.guests?.first_name} {res.guests?.last_name}
                                {res.stay_type === 'HORAS' && <span className="pill pill-amber" style={{marginLeft: '6px'}}>HORAS</span>}
                              </td>
                              <td style={{ padding: '12px 14px' }}>Hab. {rm?.room_number}</td>
                              <td style={{ padding: '12px 14px' }}>{res.stay_type === 'HORAS' ? res.check_in_time : res.check_in_date}</td>
                              <td style={{ padding: '12px 14px' }}>{res.stay_type === 'HORAS' ? res.check_out_time : res.check_out_date}</td>
                              <td style={{ padding: '12px 14px', color: 'var(--orange)', fontWeight: '700' }}>S/. {res.total_amount || res.total_price || 0}</td>
                              <td style={{ padding: '12px 14px' }}><span className="pill pill-emerald">{res.status}</span></td>
                            </tr>
                          )
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ══ HOUSEKEEPING ══ */}
          {activeView === 'housekeeping' && (
INNER_EOF

# Extract from Housekeeping onwards
awk '
  /== HOUSEKEEPING ==/ { flag = 1 }
  flag { print }
' src/app/dashboard/page.tsx > p3.txt

cat p1.txt p2.txt p3.txt > page_fixed1.tsx
mv page_fixed1.tsx src/app/dashboard/page.tsx

