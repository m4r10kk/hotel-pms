import re

with open('src/app/dashboard/page.tsx', 'r') as f:
    content = f.read()

# Replace descriptions
content = content.replace("                    <p style={{ fontSize: '11px', color: 'var(--text-500)', marginTop: '4px' }}>Aquí puedes ver el estado actual de todas las habitaciones de la sucursal seleccionada. Usa el botón 'Reservar' para registrar ingresos (walk-ins) o reservas anticipadas por noche o por horas.</p>\n", "")
content = content.replace("                  <p style={{ fontSize: '11px', color: 'var(--text-500)', marginTop: '4px' }}>Gestiona el estado de limpieza de las habitaciones. El personal de limpieza puede marcar las habitaciones sucias como 'Limpias' para que estén disponibles nuevamente en recepción.</p>\n", "")
content = content.replace("              <p style={{ fontSize: '11px', color: 'var(--text-500)', marginBottom: '16px' }}>Control de caja y turnos. Al finalizar su turno, el recepcionista declara el efectivo y pagos electrónicos cobrados. El sistema calcula si hay descuadres (Arqueo Ciego).</p>\n", "")
content = content.replace("              <p style={{ fontSize: '11px', color: 'var(--text-500)', marginBottom: '16px' }}>Base de datos de todos los huéspedes de la cadena. Aquí se acumulan los puntos de lealtad y se define el nivel (Bronce, Plata, Oro, Platino) de los clientes frecuentes.</p>\n", "")
content = content.replace("              <p style={{ fontSize: '11px', color: 'var(--text-500)', marginBottom: '16px' }}>Administración del personal. Crea cuentas de acceso para tus empleados (recepcionistas, gerentes, limpieza) asignándoles roles que restringirán a qué partes del sistema pueden acceder.</p>\n", "")

# We need to find every <tbody>...</tbody> in the main sections.
# There are 5 tables that were corrupted by the early users.map sed command:
# 1. Tape chart rooms table
# 2. Tape chart reservations table
# 3. Housekeeping table
# 4. Cash shift table
# 5. CRM table
# (Users table is the 6th and that one is correct)

# Let's replace them carefully using regex by matching the preceding headers.

# 1. Tape chart rooms
content = re.sub(
    r"(\{\['Habitación', 'Tipo', 'Piso', 'Estado', 'Tarifa Base', 'Acción'\].map[^{]*?</thead>\s*)<tbody>.*?</tbody>",
    r"\1<tbody>\n"
    r"                        {rooms.map(rm => {\n"
    r"                          const rt = roomTypes.find(t => t.id === (rm as any).room_type_id)\n"
    r"                          return (\n"
    r"                            <tr key={rm.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.2s', cursor: 'default' }} onMouseEnter={e => e.currentTarget.style.background='var(--bg-700)'} onMouseLeave={e => e.currentTarget.style.background='transparent'}>\n"
    r"                              <td style={{ padding: '14px 16px', fontWeight: '800', color: 'var(--text-100)' }}>Hab. {rm.room_number}</td>\n"
    r"                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{rt?.name ?? rm.room_type}</td>\n"
    r"                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{rm.floor_number}</td>\n"
    r"                              <td style={{ padding: '14px 16px' }}><span className={`pill pill-${rm.status === 'AVAILABLE' ? 'emerald' : rm.status === 'OCCUPIED' ? 'orange' : 'amber'}`}>{rm.status}</span></td>\n"
    r"                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>S/. {rt?.base_price ?? rm.base_rate}</td>\n"
    r"                              <td style={{ padding: '14px 16px' }}>\n"
    r"                                {rm.status === 'AVAILABLE' && (\n"
    r"                                  <button onClick={() => { setResRoomId(rm.id); setShowReservationModal(true) }} style={{ background: 'rgba(255,107,0,0.15)', border: '1px solid rgba(255,107,0,0.3)', color: 'var(--orange)', padding: '6px 14px', borderRadius: '8px', fontSize: '11px', fontWeight: 800, cursor: 'pointer', transition: 'all 0.2s' }}>Reservar</button>\n"
    r"                                )}\n"
    r"                              </td>\n"
    r"                            </tr>\n"
    r"                          )\n"
    r"                        })}\n"
    r"                      </tbody>",
    content,
    flags=re.DOTALL
)

# 2. Tape chart reservations
content = re.sub(
    r"(\{\['Huésped', 'Habitación', 'Check-in', 'Check-out', 'Total', 'Estado'\].map[^{]*?</thead>\s*)<tbody>.*?</tbody>",
    r"\1<tbody>\n"
    r"                        {reservations.map(res => {\n"
    r"                          const rm = rooms.find(r => r.id === res.room_id)\n"
    r"                          return (\n"
    r"                            <tr key={res.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.2s' }} onMouseEnter={e => e.currentTarget.style.background='var(--bg-700)'} onMouseLeave={e => e.currentTarget.style.background='transparent'}>\n"
    r"                              <td style={{ padding: '14px 16px', fontWeight: '800', color: 'var(--text-100)' }}>\n"
    r"                                {(res as any).guests?.first_name} {(res as any).guests?.last_name}\n"
    r"                                {res.stay_type === 'HORAS' && <span className=\"pill pill-amber\" style={{marginLeft: '6px'}}>HORAS</span>}\n"
    r"                              </td>\n"
    r"                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>Hab. {rm?.room_number}</td>\n"
    r"                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{res.stay_type === 'HORAS' ? (res as any).check_in_time : res.check_in_date}</td>\n"
    r"                              <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{res.stay_type === 'HORAS' ? (res as any).check_out_time : res.check_out_date}</td>\n"
    r"                              <td style={{ padding: '14px 16px', color: 'var(--orange)', fontWeight: '700' }}>S/. {res.total_amount || (res as any).total_price || 0}</td>\n"
    r"                              <td style={{ padding: '14px 16px' }}><span className=\"pill pill-emerald\">{res.status}</span></td>\n"
    r"                            </tr>\n"
    r"                          )\n"
    r"                        })}\n"
    r"                      </tbody>",
    content,
    flags=re.DOTALL
)

# 3. Housekeeping
content = re.sub(
    r"(\{\['Habitación', 'Estado Actual', 'Acción'\].map[^{]*?</thead>\s*)<tbody>.*?</tbody>",
    r"\1<tbody>\n"
    r"                        {rooms.filter(r => r.status.includes('DIRTY') || r.status.includes('CLEANING')).map(rm => (\n"
    r"                          <tr key={rm.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.2s' }}>\n"
    r"                            <td style={{ padding: '14px 16px', fontWeight: '800', color: 'var(--text-100)' }}>Hab. {rm.room_number}</td>\n"
    r"                            <td style={{ padding: '14px 16px' }}><span className=\"pill pill-amber\">{rm.status}</span></td>\n"
    r"                            <td style={{ padding: '14px 16px' }}><button style={{ background: 'var(--emerald)', color: '#fff', border: 'none', padding: '6px 14px', borderRadius: '8px', fontSize: '11px', fontWeight: 800, cursor: 'pointer', transition: 'all 0.2s' }}>Marcar Limpia</button></td>\n"
    r"                          </tr>\n"
    r"                        ))}\n"
    r"                        {rooms.filter(r => r.status.includes('DIRTY') || r.status.includes('CLEANING')).length === 0 && (\n"
    r"                          <tr><td colSpan={3} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-500)', fontSize: '13px' }}>Todo limpio ✨</td></tr>\n"
    r"                        )}\n"
    r"                      </tbody>",
    content,
    flags=re.DOTALL
)

# 4. Cash Shift
content = re.sub(
    r"(\{\['Turno ID', 'Caja Declarada', 'Sistema', 'Diferencia', 'Estado'\].map[^{]*?</thead>\s*)<tbody>.*?</tbody>",
    r"\1<tbody>\n"
    r"                        <tr><td colSpan={5} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-500)', fontSize: '13px' }}>No hay turnos registrados.</td></tr>\n"
    r"                      </tbody>",
    content,
    flags=re.DOTALL
)

# 5. CRM
content = re.sub(
    r"(\{\['Huésped', 'Documento', 'Nivel', 'Puntos', 'Contacto'\].map[^{]*?</thead>\s*)<tbody>.*?</tbody>",
    r"\1<tbody>\n"
    r"                        {guests.map(g => (\n"
    r"                          <tr key={g.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.2s' }} onMouseEnter={e => e.currentTarget.style.background='var(--bg-700)'} onMouseLeave={e => e.currentTarget.style.background='transparent'}>\n"
    r"                            <td style={{ padding: '14px 16px', fontWeight: '800', color: 'var(--text-100)' }}>{g.first_name} {g.last_name}</td>\n"
    r"                            <td style={{ padding: '14px 16px', color: 'var(--text-300)' }}>{g.document_type} {g.document_number}</td>\n"
    r"                            <td style={{ padding: '14px 16px' }}><span className=\"pill pill-emerald\">{g.loyalty_tier}</span></td>\n"
    r"                            <td style={{ padding: '14px 16px', color: 'var(--orange)', fontWeight: '700' }}>{g.loyalty_points} pts</td>\n"
    r"                            <td style={{ padding: '14px 16px', color: 'var(--text-400)', fontSize: '12px' }}>{g.email || g.phone || '—'}</td>\n"
    r"                          </tr>\n"
    r"                        ))}\n"
    r"                      </tbody>",
    content,
    flags=re.DOTALL
)


with open('src/app/dashboard/page.tsx', 'w') as f:
    f.write(content)

