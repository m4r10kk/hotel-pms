import re

with open('src/app/dashboard/page.tsx', 'r') as f:
    content = f.read()

# 1. Add states
states = """  const [resSaving, setResSaving] = useState(false)
  const [resError, setResError] = useState('')
  const [resStayType, setResStayType] = useState<'NOCHE' | 'HORAS'>('NOCHE')
  const [resCheckInTime, setResCheckInTime] = useState('')
  const [resCheckOutTime, setResCheckOutTime] = useState('')
  const [resTotalPrice, setResTotalPrice] = useState(0)"""
content = re.sub(r"  const \[resSaving, setResSaving\] = useState\(false\)\n  const \[resError, setResError\] = useState\(''\)", states, content)

# 2. Update SettingsView tag
content = content.replace(
    "<SettingsView activeOrgId={activeOrgId} activeBranchId={activeBranchId} roomTypes={roomTypes} onRefreshOrg={() => loadBranches(activeOrgId)} onRefresh={() => { loadRoomTypes(activeBranchId); loadRooms(activeBranchId); }} />",
    "<SettingsView activeOrgId={activeOrgId} activeBranchId={activeBranchId} roomTypes={roomTypes} onRefreshOrg={() => loadBranches(activeOrgId)} onBranchCreated={(id) => { setActiveBranchId(id); loadBranches(activeOrgId); }} onRefresh={() => { loadRoomTypes(activeBranchId); loadRooms(activeBranchId); }} />"
)

# 3. Update saveNewReservation
old_func = """  async function saveNewReservation(e: React.FormEvent) {
    e.preventDefault()
    setResSaving(true)
    setResError('')

    if (!resRoomId || !resCheckIn || !resCheckOut) {
      setResError('Completa todos los campos.')
      setResSaving(false)
      return
    }

    const { error } = await supabase.from('reservations').insert({
      branch_id: activeBranchId,
      room_id: resRoomId,
      check_in_date: resCheckIn,
      check_out_date: resCheckOut,
      status: 'CONFIRMED',
      total_amount: 0,
    })

    if (error) {
      setResError('Error al guardar. Verifica que la habitación esté disponible.')
      setResSaving(false)
    } else {
      setResRoomId('')
      setResCheckIn('')
      setResCheckOut('')
      setResGuestName('')
      setResSaving(false)
      setShowReservationModal(false)
    }
  }"""

new_func = """  async function saveNewReservation(e: React.FormEvent) {
    e.preventDefault()
    setResSaving(true)
    setResError('')

    if (!resRoomId) { setResError('Selecciona una habitación.'); setResSaving(false); return }
    if (!resGuestName.trim()) { setResError('Ingresa el nombre del huésped.'); setResSaving(false); return }

    if (resStayType === 'HORAS' && (!resCheckInTime || !resCheckOutTime)) {
      setResError('Ingresa la hora de entrada y salida.'); setResSaving(false); return
    }
    if (resStayType === 'NOCHE' && (!resCheckIn || !resCheckOut)) {
      setResError('Ingresa las fechas de check-in y check-out.'); setResSaving(false); return
    }

    // Create guest on the fly
    const nameParts = resGuestName.trim().split(' ')
    const { data: guestData, error: guestErr } = await supabase.from('guests').insert({
      organization_id: activeOrgId,
      first_name: nameParts[0],
      last_name: nameParts.slice(1).join(' ') || '-',
      document_type: 'DNI',
      document_number: `TEMP-${Date.now()}`,
      loyalty_points: 0,
      loyalty_tier: 'BRONZE'
    }).select('id').single()

    if (guestErr || !guestData) {
      setResError(`Error al registrar huésped: ${guestErr?.message}`)
      setResSaving(false); return
    }

    const today = new Date().toISOString().split('T')[0]
    const checkInDate = resStayType === 'NOCHE' ? resCheckIn : today
    const checkOutDate = resStayType === 'NOCHE' ? resCheckOut : today

    let durationHours: number | null = null
    if (resStayType === 'HORAS' && resCheckInTime && resCheckOutTime) {
      const [h1, m1] = resCheckInTime.split(':').map(Number)
      const [h2, m2] = resCheckOutTime.split(':').map(Number)
      durationHours = Math.max(1, Math.round(((h2 * 60 + m2) - (h1 * 60 + m1)) / 60))
    }

    const selectedRoom = rooms.find(r => r.id === resRoomId)
    const selectedRoomType = roomTypes.find(rt => rt.id === (selectedRoom as any)?.room_type_id)

    let total = resTotalPrice
    if (total === 0) {
      if (resStayType === 'HORAS' && selectedRoomType?.hourly_rate && durationHours) {
        total = selectedRoomType.hourly_rate * durationHours
      } else if (resStayType === 'NOCHE' && selectedRoomType?.base_price) {
        const nights = Math.max(1, Math.round((new Date(checkOutDate).getTime() - new Date(checkInDate).getTime()) / 86400000))
        total = selectedRoomType.base_price * nights
      }
    }

    const resCode = `RES-${Date.now().toString().slice(-8)}`

    const payload: Record<string, any> = {
      branch_id: activeBranchId,
      guest_id: guestData.id,
      room_id: resRoomId,
      room_type_id: (selectedRoom as any)?.room_type_id || selectedRoomType?.id,
      code: resCode,
      check_in_date: checkInDate,
      check_out_date: checkOutDate,
      status: 'CONFIRMED',
      total_price: total,
      stay_type: resStayType,
      adults_count: 1,
    }

    if (resStayType === 'HORAS') {
      payload.duration_hours = durationHours
      payload.check_in_time = resCheckInTime
      payload.check_out_time = resCheckOutTime
    }

    const { error } = await supabase.from('reservations').insert(payload)

    if (error) {
      setResError(`Error: ${error.message}`)
      setResSaving(false)
    } else {
      setResRoomId(''); setResCheckIn(''); setResCheckOut(''); setResGuestName('')
      setResCheckInTime(''); setResCheckOutTime(''); setResTotalPrice(0); setResStayType('NOCHE')
      setResSaving(false)
      setShowReservationModal(false)
      loadReservations(activeBranchId)
    }
  }"""
content = content.replace(old_func, new_func)

# 4. Update reservation form
old_form = """            <form onSubmit={saveNewReservation}>
              <div style={{ marginBottom: '13px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Habitación</label>
                <select className="form-input" value={resRoomId} onChange={e => setResRoomId(e.target.value)} required style={{ cursor: 'pointer' }}>
                  <option value="">— Selecciona habitación —</option>
                  {rooms.filter(r => r.status === 'AVAILABLE').map(r => (
                    <option key={r.id} value={r.id}>Hab. {r.room_number} — {r.room_type} (S/. {r.base_rate})</option>
                  ))}
                </select>
              </div>
              <div style={{ marginBottom: '13px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Check-in</label>
                <input type="date" className="form-input" value={resCheckIn} onChange={e => setResCheckIn(e.target.value)} required />
              </div>
              <div style={{ marginBottom: '18px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Check-out</label>
                <input type="date" className="form-input" value={resCheckOut} onChange={e => setResCheckOut(e.target.value)} required />
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button type="button" onClick={() => setShowReservationModal(false)} style={{ ...btnGhost, flex: 1, justifyContent: 'center' }}>Cancelar</button>
                <button type="submit" disabled={resSaving} style={{ ...btnPrimary, flex: 1, justifyContent: 'center' }}>
                  {resSaving ? 'Guardando...' : 'Guardar Reserva'}
                </button>
              </div>
            </form>"""

new_form = """            <form onSubmit={saveNewReservation}>
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
            </form>"""
content = content.replace(old_form, new_form)

# 5. Fix tables - just find the `<tbody>...</tbody>` that were ruined by earlier scripts.
# Wait, I reverted to git. So the tables are NOT broken in this run. 
# They are exactly as they were. I just need to update the tape chart to show the new fields!

# Let's replace the Rooms Table row to show reserve modal
old_rooms_row = """                        {rooms.map(rm => (
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
                        ))}"""
new_rooms_row = """                        {rooms.map(rm => {
                          const rt = roomTypes.find(t => t.id === (rm as any).room_type_id)
                          return (
                            <tr key={rm.id}>
                              <td style={{ padding: '12px 14px', fontWeight: '800' }}>Hab. {rm.room_number}</td>
                              <td style={{ padding: '12px 14px', color: 'var(--text-300)' }}>{rt?.name ?? rm.room_type}</td>
                              <td style={{ padding: '12px 14px' }}>{rm.floor}</td>
                              <td style={{ padding: '12px 14px' }}><span className={`pill pill-${rm.status === 'AVAILABLE' ? 'emerald' : rm.status === 'OCCUPIED' ? 'orange' : 'amber'}`}>{rm.status}</span></td>
                              <td style={{ padding: '12px 14px' }}>S/. {rt?.base_price ?? rm.base_rate}</td>
                              <td style={{ padding: '12px 14px' }}>
                                {rm.status === 'AVAILABLE' && (
                                  <button onClick={() => { setResRoomId(rm.id); setShowReservationModal(true) }} style={{ background: 'var(--bg-600)', border: '1px solid var(--border-subtle)', color: 'var(--text-300)', padding: '5px 10px', borderRadius: '6px', fontSize: '11px', cursor: 'pointer' }}>Reservar</button>
                                )}
                              </td>
                            </tr>
                          )
                        })}"""
content = content.replace(old_rooms_row, new_rooms_row)

old_res_table = """                      <tbody>
                        {reservations.map(res => {
                          const rm = rooms.find(r => r.id === res.room_id)
                          return (
                            <tr key={res.id}>
                              <td style={{ padding: '12px 14px', fontWeight: '800' }}>{res.guests?.first_name} {res.guests?.last_name}</td>
                              <td style={{ padding: '12px 14px' }}>Hab. {rm?.room_number}</td>
                              <td style={{ padding: '12px 14px' }}>{res.check_in_date}</td>
                              <td style={{ padding: '12px 14px' }}>{res.check_out_date}</td>
                              <td style={{ padding: '12px 14px', color: 'var(--orange)', fontWeight: '700' }}>S/. {res.total_amount || 0}</td>
                              <td style={{ padding: '12px 14px' }}><span className="pill pill-emerald">{res.status}</span></td>
                            </tr>
                          )
                        })}
                      </tbody>"""
new_res_table = """                      <tbody>
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
                              <td style={{ padding: '12px 14px', color: 'var(--orange)', fontWeight: '700' }}>S/. {res.total_amount || (res as any).total_price || 0}</td>
                              <td style={{ padding: '12px 14px' }}><span className="pill pill-emerald">{res.status}</span></td>
                            </tr>
                          )
                        })}
                      </tbody>"""
content = content.replace(old_res_table, new_res_table)

with open('src/app/dashboard/page.tsx', 'w') as f:
    f.write(content)

