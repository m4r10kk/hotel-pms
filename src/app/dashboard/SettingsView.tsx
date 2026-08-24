import { useState } from 'react'
import { createClient } from '@/lib/supabase'

export default function SettingsView({ 
  activeOrgId, activeBranchId, roomTypes, onRefreshOrg, onRefresh 
}: { 
  activeOrgId: string, activeBranchId: string, roomTypes: any[], onRefreshOrg: () => void, onRefresh: () => void 
}) {
  const supabase = createClient()
  const [loading, setLoading] = useState(false)
  
  // Room Type Form
  const [rtName, setRtName] = useState('')
  const [rtCode, setRtCode] = useState('')
  const [rtPrice, setRtPrice] = useState('')

  // Room Form
  const [rNumber, setRNumber] = useState('')
  const [rFloor, setRFloor] = useState('1')
  const [rTypeId, setRTypeId] = useState('')

  // Branch Form
  const [bName, setBName] = useState('')
  const [bCity, setBCity] = useState('')

  async function handleSaveRoomType(e: React.FormEvent) {
    e.preventDefault()
    if (!activeBranchId) return alert('Selecciona una sucursal primero')
    setLoading(true)
    const { error } = await supabase.from('room_types').insert({
      branch_id: activeBranchId,
      name: rtName,
      code: rtCode,
      base_price: parseFloat(rtPrice)
    })
    setLoading(false)
    if (error) alert(`Error: ${error.message}`)
    else {
      setRtName(''); setRtCode(''); setRtPrice(''); onRefresh()
    }
  }

  async function handleSaveRoom(e: React.FormEvent) {
    e.preventDefault()
    if (!activeBranchId) return alert('Selecciona una sucursal primero')
    if (!rTypeId) return alert('Selecciona un tipo de habitación')
    setLoading(true)
    const { error } = await supabase.from('rooms').insert({
      branch_id: activeBranchId,
      room_type_id: rTypeId,
      room_number: rNumber,
      floor_number: parseInt(rFloor)
    })
    setLoading(false)
    if (error) alert(`Error: ${error.message}`)
    else {
      setRNumber(''); setRFloor('1'); setRTypeId(''); onRefresh()
    }
  }

  async function handleSaveBranch(e: React.FormEvent) {
    e.preventDefault()
    if (!activeOrgId) return alert('Selecciona una empresa primero')
    setLoading(true)
    const branchCode = bCity.toUpperCase().replace(/\s+/g, '_').slice(0, 20)
    const { error } = await supabase.from('branches').insert({
      organization_id: activeOrgId,
      name: bName,
      code: branchCode,
      city: bCity
    })
    setLoading(false)
    if (error) alert(`Error: ${error.message}`)
    else {
      setBName(''); setBCity(''); onRefreshOrg()
    }
  }

  return (
    <div className="animate-fadeUp" style={{ display: 'grid', gap: '24px' }}>
      
      {/* ══ SUCURSALES ══ */}
      <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '16px' }}>Sucursales</h2>
        <form onSubmit={handleSaveBranch} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div>
            <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>NOMBRE SUCURSAL</label>
            <input type="text" className="form-input" placeholder="Ej: Hotel Central" value={bName} onChange={e => setBName(e.target.value)} required />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>CIUDAD</label>
            <input type="text" className="form-input" placeholder="Ej: Lima" value={bCity} onChange={e => setBCity(e.target.value)} required />
          </div>
          <button type="submit" disabled={loading} style={{ background: 'var(--emerald)', color: '#fff', padding: '10px 16px', borderRadius: '8px', fontSize: '12px', fontWeight: '700', border: 'none', cursor: 'pointer' }}>Guardar Sucursal</button>
        </form>
      </div>

      {/* ══ TIPOS DE HABITACIÓN ══ */}
      <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '16px' }}>Tipos de Habitación (Para sucursal activa)</h2>
        <form onSubmit={handleSaveRoomType} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div>
            <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>NOMBRE</label>
            <input type="text" className="form-input" placeholder="Ej: Matrimonial King" value={rtName} onChange={e => setRtName(e.target.value)} required />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>CÓDIGO</label>
            <input type="text" className="form-input" placeholder="Ej: MAT-KING" value={rtCode} onChange={e => setRtCode(e.target.value)} required />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>PRECIO BASE</label>
            <input type="number" step="0.01" className="form-input" placeholder="Ej: 150.00" value={rtPrice} onChange={e => setRtPrice(e.target.value)} required />
          </div>
          <button type="submit" disabled={loading} style={{ background: 'var(--orange)', color: '#fff', padding: '10px 16px', borderRadius: '8px', fontSize: '12px', fontWeight: '700', border: 'none', cursor: 'pointer' }}>Guardar Tipo</button>
        </form>
      </div>

      {/* ══ HABITACIONES ══ */}
      <div style={{ background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)', padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '16px' }}>Habitaciones</h2>
        <form onSubmit={handleSaveRoom} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div>
            <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>TIPO DE HABITACIÓN</label>
            <select className="form-input" value={rTypeId} onChange={e => setRTypeId(e.target.value)} required>
              <option value="" disabled>-- Selecciona --</option>
              {roomTypes.map(rt => (
                <option key={rt.id} value={rt.id}>{rt.name} ({rt.code})</option>
              ))}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>Nº HABITACIÓN</label>
            <input type="text" className="form-input" placeholder="Ej: 101" value={rNumber} onChange={e => setRNumber(e.target.value)} required />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }}>PISO</label>
            <input type="number" className="form-input" placeholder="Ej: 1" value={rFloor} onChange={e => setRFloor(e.target.value)} required />
          </div>
          <button type="submit" disabled={loading} style={{ background: 'var(--emerald)', color: '#fff', padding: '10px 16px', borderRadius: '8px', fontSize: '12px', fontWeight: '700', border: 'none', cursor: 'pointer' }}>Guardar Habitación</button>
        </form>
      </div>
    </div>
  )
}
