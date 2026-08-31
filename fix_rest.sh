#!/bin/bash
set -e

awk '/{..Habitación., .Estado Actual., .Acción.}.map\(h => \(/ {print; getline; print; getline; print; getline; print; exit}' src/app/dashboard/page.tsx > p1.txt

cat << 'INNER_EOF' > p2.txt
                      <tbody>
                        {rooms.filter(r => r.status.includes('DIRTY') || r.status.includes('CLEANING')).map(rm => (
                          <tr key={rm.id}>
                            <td style={{ padding: '12px 14px', fontWeight: '800' }}>Hab. {rm.room_number}</td>
                            <td style={{ padding: '12px 14px' }}><span className="pill pill-amber">{rm.status}</span></td>
                            <td style={{ padding: '12px 14px' }}><button style={{ background: 'var(--emerald)', color: '#fff', border: 'none', padding: '5px 10px', borderRadius: '6px', fontSize: '11px', cursor: 'pointer' }}>Marcar Limpia</button></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* ══ CASH SHIFT ══ */}
              {activeView === 'cashshift' && (
INNER_EOF

awk '
  /== CASH SHIFT ==/ { flag = 1; getline; next }
  /{..Turno ID., .Caja Declarada., .Sistema., .Diferencia., .Estado.}.map\(h => \(/ {
    if(flag) { print; getline; print; getline; print; getline; print; flag = 0; exit }
  }
  flag { print }
' src/app/dashboard/page.tsx > p3.txt

cat << 'INNER_EOF' > p4.txt
                      <tbody>
                        {/* Fake cash shift data for now since we do not fetch it */}
                        <tr><td colSpan={5} style={{ padding: '12px 14px', color: 'var(--text-500)' }}>No hay turnos registrados</td></tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* ══ CRM ══ */}
              {activeView === 'crm' && (
INNER_EOF

awk '
  /== CRM ==/ { flag = 1; getline; next }
  /{..Huésped., .Documento., .Nivel., .Puntos., .Contacto.}.map\(h => \(/ {
    if (flag) { print; getline; print; getline; print; getline; print; flag = 0; exit }
  }
  flag { print }
' src/app/dashboard/page.tsx > p5.txt

cat << 'INNER_EOF' > p6.txt
                      <tbody>
                        {guests.map(g => (
                          <tr key={g.id}>
                            <td style={{ padding: '12px 14px', fontWeight: '800' }}>{g.first_name} {g.last_name}</td>
                            <td style={{ padding: '12px 14px', color: 'var(--text-300)' }}>{g.document_type} {g.document_number}</td>
                            <td style={{ padding: '12px 14px' }}><span className="pill pill-emerald">{g.loyalty_tier}</span></td>
                            <td style={{ padding: '12px 14px', color: 'var(--orange)', fontWeight: '700' }}>{g.loyalty_points} pts</td>
                            <td style={{ padding: '12px 14px', color: 'var(--text-500)', fontSize: '11px' }}>{g.email || g.phone || '—'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* ══ USERS ══ */}
INNER_EOF

awk '
  /== USERS ==/ { flag = 1 }
  flag { print }
' src/app/dashboard/page.tsx > p7.txt

cat p1.txt p2.txt p3.txt p4.txt p5.txt p6.txt p7.txt > page_fixed2.tsx
mv page_fixed2.tsx src/app/dashboard/page.tsx
