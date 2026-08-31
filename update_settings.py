import os

code = """'use client'
import { useState, useEffect, useCallback } from 'react'
import { createClient } from '@/lib/supabase'

export default function SettingsView({ 
  activeOrgId, activeBranchId, roomTypes, onRefreshOrg, onBranchCreated, onRefresh 
}: { 
  activeOrgId: string
  activeBranchId: string
  roomTypes: any[]
  onRefreshOrg: () => void
  onBranchCreated: (id: string) => void
  onRefresh: () => void
}) {
  const supabase = createClient()
  const [loading, setLoading] = useState(false)
  
  // Data
  const [branches, setBranches] = useState<any[]>([])
  const [rooms, setRooms] = useState<any[]>([])

  // Edit states
  const [editingBranch, setEditingBranch] = useState<any>(null)
  const [editingRoomType, setEditingRoomType] = useState<any>(null)
  const [editingRoom, setEditingRoom] = useState<any>(null)
  
  // Forms
  const [bName, setBName] = useState('')
  const [bCity, setBCity] = useState('')
  
  const [rtName, setRtName] = useState('')
  const [rtCode, setRtCode] = useState('')
  const [rtPrice, setRtPrice] = useState('')
  const [rtHourly, setRtHourly] = useState('')
  
  const [rNumber, setRNumber] = useState('')
  const [rFloor, setRFloor] = useState('1')
  const [rTypeId, setRTypeId] = useState('')

  const [msg, setMsg] = useState({ b: '', rt: '', r: '' })

  const loadData = useCallback(async () => {
    if (activeOrgId) {
      const { data: bData } = await supabase.from('branches').select('*').eq('organization_id', activeOrgId).order('created_at', { ascending: true })
      if (bData) setBranches(bData)
    }
    if (activeBranchId) {
      const { data: rData } = await supabase.from('rooms').select('*').eq('branch_id', activeBranchId).order('room_number', { ascending: true })
      if (rData) setRooms(rData)
    }
  }, [activeOrgId, activeBranchId, supabase])

  useEffect(() => { loadData() }, [loadData])

  const showMsg = (key: 'b' | 'rt' | 'r', text: string) => {
    setMsg(prev => ({ ...prev, [key]: text }))
    setTimeout(() => setMsg(prev => ({ ...prev, [key]: '' })), 4000)
  }

  // --- BRANCHES ---
  async function handleSaveBranch(e: React.FormEvent) {
    e.preventDefault()
    if (!activeOrgId) { showMsg('b', '⚠️ Selecciona una empresa primero.'); return }
    setLoading(true)
    const branchCode = bCity.toUpperCase().replace(/\\s+/g, '_').slice(0, 20)
    
    if (editingBranch) {
      const { error } = await supabase.from('branches').update({ name: bName, city: bCity, code: branchCode }).eq('id', editingBranch.id)
      if (error) { showMsg('b', `❌ ${error.message}`) } else { showMsg('b', '✅ Sucursal actualizada.'); setEditingBranch(null); setBName(''); setBCity(''); loadData(); onRefreshOrg() }
    } else {
      const { data, error } = await supabase.from('branches').insert({ organization_id: activeOrgId, name: bName, code: branchCode, city: bCity }).select('id').single()
      if (error) { showMsg('b', `❌ ${error.message}`) } else { showMsg('b', '✅ Sucursal creada.'); setBName(''); setBCity(''); if (data) onBranchCreated(data.id); loadData(); onRefreshOrg() }
    }
    setLoading(false)
  }

  async function deleteBranch(id: string) {
    if (!confirm('¿Eliminar sucursal? Se borrarán sus habitaciones y reservas.')) return
    setLoading(true)
    const { error } = await supabase.from('branches').delete().eq('id', id)
    if (error) showMsg('b', `❌ ${error.message}`)
    else { showMsg('b', '✅ Eliminada.'); loadData(); onRefreshOrg() }
    setLoading(false)
  }

  function editBranch(b: any) {
    setEditingBranch(b); setBName(b.name); setBCity(b.city)
  }

  // --- ROOM TYPES ---
  async function handleSaveRoomType(e: React.FormEvent) {
    e.preventDefault()
    if (!activeBranchId) { showMsg('rt', '⚠️ Selecciona sucursal primero.'); return }
    setLoading(true)
    const payload = { branch_id: activeBranchId, name: rtName, code: rtCode, base_price: parseFloat(rtPrice), hourly_rate: rtHourly ? parseFloat(rtHourly) : null }
    
    if (editingRoomType) {
      const { error } = await supabase.from('room_types').update(payload).eq('id', editingRoomType.id)
      if (error) showMsg('rt', `❌ ${error.message}`)
      else { showMsg('rt', '✅ Actualizado.'); setEditingRoomType(null); setRtName(''); setRtCode(''); setRtPrice(''); setRtHourly(''); onRefresh() }
    } else {
      const { error } = await supabase.from('room_types').insert(payload)
      if (error) showMsg('rt', `❌ ${error.message}`)
      else { showMsg('rt', '✅ Creado.'); setRtName(''); setRtCode(''); setRtPrice(''); setRtHourly(''); onRefresh() }
    }
    setLoading(false)
  }

  async function deleteRoomType(id: string) {
    if (!confirm('¿Eliminar tipo? Solo si no tiene habitaciones.')) return
    setLoading(true)
    const { error } = await supabase.from('room_types').delete().eq('id', id)
    if (error) showMsg('rt', `❌ ${error.message}`)
    else { showMsg('rt', '✅ Eliminado.'); onRefresh() }
    setLoading(false)
  }

  function editRoomType(rt: any) {
    setEditingRoomType(rt); setRtName(rt.name); setRtCode(rt.code); setRtPrice(rt.base_price); setRtHourly(rt.hourly_rate || '')
  }

  // --- ROOMS ---
  async function handleSaveRoom(e: React.FormEvent) {
    e.preventDefault()
    if (!activeBranchId || !rTypeId) { showMsg('r', '⚠️ Faltan datos.'); return }
    setLoading(true)
    const payload = { branch_id: activeBranchId, room_type_id: rTypeId, room_number: rNumber, floor_number: parseInt(rFloor) }
    
    if (editingRoom) {
      const { error } = await supabase.from('rooms').update(payload).eq('id', editingRoom.id)
      if (error) showMsg('r', `❌ ${error.message}`)
      else { showMsg('r', '✅ Actualizada.'); setEditingRoom(null); setRNumber(''); setRFloor('1'); setRTypeId(''); loadData(); onRefresh() }
    } else {
      const { error } = await supabase.from('rooms').insert(payload)
      if (error) showMsg('r', `❌ ${error.message}`)
      else { showMsg('r', '✅ Creada.'); setRNumber(''); setRFloor('1'); setRTypeId(''); loadData(); onRefresh() }
    }
    setLoading(false)
  }

  async function deleteRoom(id: string) {
    if (!confirm('¿Eliminar habitación? Se borrarán sus reservas.')) return
    setLoading(true)
    const { error } = await supabase.from('rooms').delete().eq('id', id)
    if (error) showMsg('r', `❌ ${error.message}`)
    else { showMsg('r', '✅ Eliminada.'); loadData(); onRefresh() }
    setLoading(false)
  }

  function editRoom(r: any) {
    setEditingRoom(r); setRNumber(r.room_number); setRFloor(r.floor_number); setRTypeId(r.room_type_id)
  }

  const card = { background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }
  const fieldLabel = { display: 'block', fontSize: '10px', fontWeight: '800' as const, color: 'var(--text-300)', marginBottom: '6px' }
  const msgStyle = (m: string) => ({ padding: '8px 12px', borderRadius: '8px', fontSize: '12px', marginTop: '10px', background: m.startsWith('✅') ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)', color: m.startsWith('✅') ? '#34d399' : '#fca5a5' })

  return (
    <div className="animate-fadeUp tour-settings" style={{ display: 'grid', gap: '24px' }}>
      {/* SUCURSALES */}
      <div style={card}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '6px' }}>1. Sucursales</h2>
        <form onSubmit={handleSaveBranch} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap', marginBottom: '16px' }}>
          <div><label style={fieldLabel}>NOMBRE SUCURSAL</label><input type="text" className="form-input" value={bName} onChange={e => setBName(e.target.value)} required /></div>
          <div><label style={fieldLabel}>CIUDAD</label><input type="text" className="form-input" value={bCity} onChange={e => setBCity(e.target.value)} required /></div>
          <button type="submit" disabled={loading} style={{ background: editingBranch ? 'var(--orange)' : 'var(--emerald)', color: '#fff', padding: '10px 16px', borderRadius: '8px', border: 'none', cursor: 'pointer', fontWeight: 700 }}>{editingBranch ? 'Guardar Cambios' : 'Crear Sucursal'}</button>
          {editingBranch && <button type="button" onClick={() => {setEditingBranch(null); setBName(''); setBCity('')}} style={{ background: 'var(--bg-600)', color: '#fff', padding: '10px 16px', borderRadius: '8px', border: 'none', cursor: 'pointer' }}>Cancelar</button>}
        </form>
        {msg.b && <div style={msgStyle(msg.b)}>{msg.b}</div>}
        
        {branches.length > 0 && (
          <table style={{ width: '100%', fontSize: '12px', borderCollapse: 'collapse', marginTop: '12px' }}>
            <thead><tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-500)', textAlign: 'left' }}><th>Nombre</th><th>Ciudad</th><th>Código</th><th>Acciones</th></tr></thead>
            <tbody>{branches.map(b => (
              <tr key={b.id} style={{ borderBottom: '1px dotted var(--border-subtle)' }}>
                <td style={{ padding: '8px 0' }}>{b.name} {activeBranchId === b.id && <span className="pill pill-emerald" style={{marginLeft:'5px'}}>Activa</span>}</td>
                <td>{b.city}</td><td>{b.code}</td>
                <td>
                  <button onClick={() => editBranch(b)} style={{ background: 'none', border: 'none', color: 'var(--text-300)', cursor: 'pointer', marginRight: '8px' }}>✏️</button>
                  <button onClick={() => deleteBranch(b.id)} style={{ background: 'none', border: 'none', color: 'var(--text-300)', cursor: 'pointer' }}>🗑️</button>
                </td>
              </tr>
            ))}</tbody>
          </table>
        )}
      </div>

      {/* TIPOS */}
      <div style={card}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '6px' }}>2. Tipos de Habitación</h2>
        <form onSubmit={handleSaveRoomType} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap', marginBottom: '16px' }}>
          <div><label style={fieldLabel}>NOMBRE</label><input type="text" className="form-input" value={rtName} onChange={e => setRtName(e.target.value)} required /></div>
          <div><label style={fieldLabel}>CÓDIGO</label><input type="text" className="form-input" style={{width:'80px'}} value={rtCode} onChange={e => setRtCode(e.target.value)} required /></div>
          <div><label style={fieldLabel}>PRECIO / NOCHE</label><input type="number" step="0.01" className="form-input" style={{width:'100px'}} value={rtPrice} onChange={e => setRtPrice(e.target.value)} required /></div>
          <div><label style={fieldLabel}>TARIFA / HORA</label><input type="number" step="0.01" className="form-input" style={{width:'100px'}} value={rtHourly} onChange={e => setRtHourly(e.target.value)} /></div>
          <button type="submit" disabled={loading} style={{ background: editingRoomType ? 'var(--orange)' : 'var(--emerald)', color: '#fff', padding: '10px 16px', borderRadius: '8px', border: 'none', cursor: 'pointer', fontWeight: 700 }}>{editingRoomType ? 'Guardar' : 'Crear Tipo'}</button>
          {editingRoomType && <button type="button" onClick={() => {setEditingRoomType(null); setRtName(''); setRtCode(''); setRtPrice(''); setRtHourly('')}} style={{ background: 'var(--bg-600)', color: '#fff', padding: '10px 16px', borderRadius: '8px', border: 'none', cursor: 'pointer' }}>Cancelar</button>}
        </form>
        {msg.rt && <div style={msgStyle(msg.rt)}>{msg.rt}</div>}

        {roomTypes.length > 0 && (
          <table style={{ width: '100%', fontSize: '12px', borderCollapse: 'collapse', marginTop: '12px' }}>
            <thead><tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-500)', textAlign: 'left' }}><th>Nombre</th><th>Código</th><th>Noche</th><th>Hora</th><th>Acciones</th></tr></thead>
            <tbody>{roomTypes.map(rt => (
              <tr key={rt.id} style={{ borderBottom: '1px dotted var(--border-subtle)' }}>
                <td style={{ padding: '8px 0' }}>{rt.name}</td><td>{rt.code}</td>
                <td>S/. {rt.base_price}</td><td>{rt.hourly_rate ? `S/. ${rt.hourly_rate}` : '—'}</td>
                <td>
                  <button onClick={() => editRoomType(rt)} style={{ background: 'none', border: 'none', color: 'var(--text-300)', cursor: 'pointer', marginRight: '8px' }}>✏️</button>
                  <button onClick={() => deleteRoomType(rt.id)} style={{ background: 'none', border: 'none', color: 'var(--text-300)', cursor: 'pointer' }}>🗑️</button>
                </td>
              </tr>
            ))}</tbody>
          </table>
        )}
      </div>

      {/* HABITACIONES */}
      <div style={card}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '6px' }}>3. Habitaciones</h2>
        <form onSubmit={handleSaveRoom} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap', marginBottom: '16px' }}>
          <div><label style={fieldLabel}>TIPO</label>
            <select className="form-input" value={rTypeId} onChange={e => setRTypeId(e.target.value)} required>
              <option value="" disabled>-- Selecciona --</option>
              {roomTypes.map(rt => <option key={rt.id} value={rt.id}>{rt.name}</option>)}
            </select>
          </div>
          <div><label style={fieldLabel}>Nº HABITACIÓN</label><input type="text" className="form-input" style={{width:'100px'}} value={rNumber} onChange={e => setRNumber(e.target.value)} required /></div>
          <div><label style={fieldLabel}>PISO</label><input type="number" className="form-input" style={{width:'80px'}} value={rFloor} onChange={e => setRFloor(e.target.value)} required /></div>
          <button type="submit" disabled={loading} style={{ background: editingRoom ? 'var(--orange)' : 'var(--emerald)', color: '#fff', padding: '10px 16px', borderRadius: '8px', border: 'none', cursor: 'pointer', fontWeight: 700 }}>{editingRoom ? 'Guardar' : 'Crear Habitación'}</button>
          {editingRoom && <button type="button" onClick={() => {setEditingRoom(null); setRNumber(''); setRFloor('1'); setRTypeId('')}} style={{ background: 'var(--bg-600)', color: '#fff', padding: '10px 16px', borderRadius: '8px', border: 'none', cursor: 'pointer' }}>Cancelar</button>}
        </form>
        {msg.r && <div style={msgStyle(msg.r)}>{msg.r}</div>}

        {rooms.length > 0 && (
          <table style={{ width: '100%', fontSize: '12px', borderCollapse: 'collapse', marginTop: '12px' }}>
            <thead><tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-500)', textAlign: 'left' }}><th>Habitación</th><th>Piso</th><th>Tipo</th><th>Acciones</th></tr></thead>
            <tbody>{rooms.map(r => {
              const rt = roomTypes.find(t => t.id === r.room_type_id)
              return (
                <tr key={r.id} style={{ borderBottom: '1px dotted var(--border-subtle)' }}>
                  <td style={{ padding: '8px 0', fontWeight: 'bold' }}>{r.room_number}</td>
                  <td>{r.floor_number}</td>
                  <td>{rt?.name || r.room_type}</td>
                  <td>
                    <button onClick={() => editRoom(r)} style={{ background: 'none', border: 'none', color: 'var(--text-300)', cursor: 'pointer', marginRight: '8px' }}>✏️</button>
                    <button onClick={() => deleteRoom(r.id)} style={{ background: 'none', border: 'none', color: 'var(--text-300)', cursor: 'pointer' }}>🗑️</button>
                  </td>
                </tr>
              )
            })}</tbody>
          </table>
        )}
      </div>
    </div>
  )
}
"""

with open('/Users/marlok/Desktop/California/src/app/dashboard/SettingsView.tsx', 'w') as f:
    f.write(code)
