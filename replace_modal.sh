#!/bin/bash
# Extract everything before <form onSubmit={saveNewReservation}>
awk '/<form onSubmit={saveNewReservation}>/{exit} {print}' src/app/dashboard/page.tsx > page_part1.txt

# Extract everything after </form> after the new reservation form
# The new reservation form is the FIRST form inside showReservationModal
awk '
  /<form onSubmit={saveNewReservation}>/ { flag = 1; count=1 }
  flag && /<\/form>/ { count--; if(count==0) { flag = 0; next } }
  flag && /<form/ { count++ }
  !flag { print }
' src/app/dashboard/page.tsx > temp_after.txt

cat << 'INNER_EOF' > new_form.txt
            <form onSubmit={saveNewReservation}>
              {/* Guest name */}
              <div style={{ marginBottom: '13px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Nombre del Huésped</label>
                <input type="text" className="form-input" placeholder="Ej: Juan García" value={resGuestName} onChange={e => setResGuestName(e.target.value)} required />
              </div>

              {/* Stay type toggle */}
              <div style={{ marginBottom: '13px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '8px' }}>Tipo de Estadía</label>
                <div style={{ display: 'flex', gap: '8px' }}>
                  {(['NOCHE', 'HORAS'] as const).map(type => (
                    <button key={type} type="button" onClick={() => setResStayType(type)} style={{
                      flex: 1, padding: '9px', borderRadius: '9px', fontSize: '12px', fontWeight: '700',
                      cursor: 'pointer', border: '1px solid',
                      background: resStayType === type ? 'rgba(255,107,0,0.2)' : 'var(--bg-700)',
                      borderColor: resStayType === type ? 'rgba(255,107,0,0.5)' : 'var(--border-subtle)',
                      color: resStayType === type ? 'var(--orange)' : 'var(--text-500)',
                    }}>
                      {type === 'NOCHE' ? '🌙 Por Noche' : '⏰ Por Horas'}
                    </button>
                  ))}
                </div>
              </div>

              {/* Room selector */}
              <div style={{ marginBottom: '13px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Habitación</label>
                <select className="form-input" value={resRoomId} onChange={e => setResRoomId(e.target.value)} required style={{ cursor: 'pointer' }}>
                  <option value="">— Selecciona habitación —</option>
                  {rooms.filter(r => r.status === 'AVAILABLE').map(r => {
                    const rt = roomTypes.find(t => t.id === (r as any).room_type_id)
                    const rate = resStayType === 'HORAS' && rt?.hourly_rate ? `S/. ${rt.hourly_rate}/hr` : rt ? `S/. ${rt.base_price}/noche` : ''
                    return <option key={r.id} value={r.id}>Hab. {r.room_number} — {rt?.name ?? r.room_type} {rate ? `(${rate})` : ''}</option>
                  })}
                </select>
              </div>

              {/* Date/time fields depending on stay type */}
              {resStayType === 'NOCHE' ? (
                <>
                  <div style={{ marginBottom: '13px' }}>
                    <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Check-in</label>
                    <input type="date" className="form-input" value={resCheckIn} onChange={e => setResCheckIn(e.target.value)} required={resStayType === 'NOCHE'} />
                  </div>
                  <div style={{ marginBottom: '18px' }}>
                    <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Check-out</label>
                    <input type="date" className="form-input" value={resCheckOut} onChange={e => setResCheckOut(e.target.value)} required={resStayType === 'NOCHE'} />
                  </div>
                </>
              ) : (
                <>
                  <div style={{ display: 'flex', gap: '12px', marginBottom: '13px' }}>
                    <div style={{ flex: 1 }}>
                      <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Hora de Entrada</label>
                      <input type="time" className="form-input" value={resCheckInTime} onChange={e => setResCheckInTime(e.target.value)} required={resStayType === 'HORAS'} />
                    </div>
                    <div style={{ flex: 1 }}>
                      <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Hora de Salida</label>
                      <input type="time" className="form-input" value={resCheckOutTime} onChange={e => setResCheckOutTime(e.target.value)} required={resStayType === 'HORAS'} />
                    </div>
                  </div>
                  {resCheckInTime && resCheckOutTime && resRoomId && (() => {
                    const [h1, m1] = resCheckInTime.split(':').map(Number)
                    const [h2, m2] = resCheckOutTime.split(':').map(Number)
                    const hrs = Math.max(0, Math.round(((h2 * 60 + m2) - (h1 * 60 + m1)) / 60))
                    const rt = roomTypes.find(t => t.id === (rooms.find(r => r.id === resRoomId) as any)?.room_type_id)
                    const total = rt?.hourly_rate ? rt.hourly_rate * hrs : 0
                    return hrs > 0 ? (
                      <div style={{ background: 'rgba(255,107,0,0.1)', border: '1px solid rgba(255,107,0,0.3)', borderRadius: '10px', padding: '12px 14px', marginBottom: '14px', fontSize: '13px' }}>
                        <span style={{ color: 'var(--text-500)' }}>{hrs} hora{hrs !== 1 ? 's' : ''} × S/. {rt?.hourly_rate ?? 0}/hr = </span>
                        <strong style={{ color: 'var(--orange)', fontSize: '16px' }}>S/. {total.toFixed(2)}</strong>
                      </div>
                    ) : null
                  })()}
                </>
              )}

              <div style={{ display: 'flex', gap: '10px' }}>
                <button type="button" onClick={() => setShowReservationModal(false)} style={{ flex: 1, justifyContent: 'center', background: 'var(--bg-700)', border: '1px solid var(--border-subtle)', color: 'var(--text-300)', padding: '10px', borderRadius: '9px', cursor: 'pointer', fontFamily: 'inherit', fontWeight: '700', fontSize: '13px', display: 'flex', alignItems: 'center' }}>Cancelar</button>
                <button type="submit" disabled={resSaving} style={{ flex: 1, justifyContent: 'center', background: 'linear-gradient(135deg, var(--orange) 0%, #ea580c 100%)', color: '#fff', padding: '10px', borderRadius: '9px', border: 'none', cursor: 'pointer', fontFamily: 'inherit', fontWeight: '700', fontSize: '13px', display: 'flex', alignItems: 'center', opacity: resSaving ? 0.7 : 1 }}>
                  {resSaving ? 'Guardando...' : 'Guardar Reserva'}
                </button>
              </div>
            </form>
INNER_EOF

cat page_part1.txt new_form.txt temp_after.txt > src/app/dashboard/page.tsx
