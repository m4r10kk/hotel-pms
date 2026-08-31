#!/bin/bash
set -e

echo "Updating SettingsView.tsx..."
cat << 'INNER_EOF' > /Users/marlok/Desktop/California/src/app/dashboard/SettingsView.tsx
'use client'
import { useState } from 'react'
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
  
  // Branch form
  const [bName, setBName] = useState('')
  const [bCity, setBCity] = useState('')
  const [bMsg, setBMsg] = useState('')

  // Room Type form
  const [rtName, setRtName] = useState('')
  const [rtCode, setRtCode] = useState('')
  const [rtPrice, setRtPrice] = useState('')
  const [rtHourly, setRtHourly] = useState('')
  const [rtMsg, setRtMsg] = useState('')

  // Room form
  const [rNumber, setRNumber] = useState('')
  const [rFloor, setRFloor] = useState('1')
  const [rTypeId, setRTypeId] = useState('')
  const [rMsg, setRMsg] = useState('')

  const card: React.CSSProperties = {
    background: 'rgba(13,21,39,0.75)', backdropFilter: 'blur(16px)',
    padding: '24px', borderRadius: '14px', border: '1px solid var(--border-subtle)'
  }

  async function handleSaveBranch(e: React.FormEvent) {
    e.preventDefault()
    if (!activeOrgId) { setBMsg('⚠️ Selecciona una empresa primero.'); return }
    setLoading(true)
    setBMsg('')
    const branchCode = bCity.toUpperCase().replace(/\s+/g, '_').slice(0, 20)
    const { data, error } = await supabase.from('branches').insert({
      organization_id: activeOrgId,
      name: bName,
      code: branchCode,
      city: bCity
    }).select('id').single()
    setLoading(false)
    if (error) { setBMsg(`❌ ${error.message}`); return }
    setBName(''); setBCity('')
    setBMsg('✅ Sucursal creada y seleccionada.')
    if (data) onBranchCreated(data.id)
    onRefreshOrg()
  }

  async function handleSaveRoomType(e: React.FormEvent) {
    e.preventDefault()
    if (!activeBranchId) { setRtMsg('⚠️ Selecciona una sucursal en el sidebar antes de continuar.'); return }
    setLoading(true); setRtMsg('')
    const { error } = await supabase.from('room_types').insert({
      branch_id: activeBranchId,
      name: rtName,
      code: rtCode,
      base_price: parseFloat(rtPrice),
      ...(rtHourly ? { hourly_rate: parseFloat(rtHourly) } : {})
    })
    setLoading(false)
    if (error) { setRtMsg(`❌ ${error.message}`); return }
    setRtName(''); setRtCode(''); setRtPrice(''); setRtHourly('')
    setRtMsg('✅ Tipo guardado.')
    onRefresh()
  }

  async function handleSaveRoom(e: React.FormEvent) {
    e.preventDefault()
    if (!activeBranchId) { setRMsg('⚠️ Selecciona una sucursal en el sidebar antes de continuar.'); return }
    if (!rTypeId) { setRMsg('⚠️ Selecciona el tipo de habitación.'); return }
    setLoading(true); setRMsg('')
    const { error } = await supabase.from('rooms').insert({
      branch_id: activeBranchId,
      room_type_id: rTypeId,
      room_number: rNumber,
      floor_number: parseInt(rFloor)
    })
    setLoading(false)
    if (error) { setRMsg(`❌ ${error.message}`); return }
    setRNumber(''); setRFloor('1'); setRTypeId('')
    setRMsg('✅ Habitación creada.')
    onRefresh()
  }

  const fieldLabel: React.CSSProperties = { display: 'block', fontSize: '10px', fontWeight: '800', color: 'var(--text-300)', marginBottom: '6px' }
  const msgStyle = (msg: string): React.CSSProperties => ({
    marginTop: '10px', padding: '8px 12px', borderRadius: '8px', fontSize: '12px',
    background: msg.startsWith('✅') ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)',
    color: msg.startsWith('✅') ? '#34d399' : '#fca5a5',
    border: `1px solid ${msg.startsWith('✅') ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)'}`
  })

  return (
    <div className="animate-fadeUp" style={{ display: 'grid', gap: '24px' }}>

      {/* Sucursales */}
      <div style={card}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '6px' }}>Sucursales</h2>
        <p style={{ fontSize: '12px', color: 'var(--text-500)', marginBottom: '16px' }}>Crea una sucursal para luego agregar habitaciones. Al crear, se auto-seleccionará.</p>
        <form onSubmit={handleSaveBranch} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div>
            <label style={fieldLabel}>NOMBRE SUCURSAL</label>
            <input type="text" className="form-input" placeholder="Ej: Hotel Central" value={bName} onChange={e => setBName(e.target.value)} required />
          </div>
          <div>
            <label style={fieldLabel}>CIUDAD</label>
            <input type="text" className="form-input" placeholder="Ej: Lima" value={bCity} onChange={e => setBCity(e.target.value)} required />
          </div>
          <button type="submit" disabled={loading} style={{ background: 'var(--emerald)', color: '#fff', padding: '10px 16px', borderRadius: '8px', fontSize: '12px', fontWeight: '700', border: 'none', cursor: 'pointer' }}>Guardar Sucursal</button>
        </form>
        {bMsg && <div style={msgStyle(bMsg)}>{bMsg}</div>}
      </div>

      {/* Tipos de Habitación */}
      <div style={card}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '6px' }}>Tipos de Habitación</h2>
        <p style={{ fontSize: '12px', color: 'var(--text-500)', marginBottom: '16px' }}>Se asignan a la sucursal activa. La tarifa por hora es opcional (para el modo de cobro por horas).</p>
        <form onSubmit={handleSaveRoomType} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div>
            <label style={fieldLabel}>NOMBRE</label>
            <input type="text" className="form-input" placeholder="Ej: Matrimonial King" value={rtName} onChange={e => setRtName(e.target.value)} required />
          </div>
          <div>
            <label style={fieldLabel}>CÓDIGO</label>
            <input type="text" className="form-input" placeholder="Ej: MAT-KING" value={rtCode} onChange={e => setRtCode(e.target.value)} required />
          </div>
          <div>
            <label style={fieldLabel}>PRECIO / NOCHE</label>
            <input type="number" step="0.01" className="form-input" placeholder="Ej: 150.00" value={rtPrice} onChange={e => setRtPrice(e.target.value)} required />
          </div>
          <div>
            <label style={fieldLabel}>TARIFA / HORA (opcional)</label>
            <input type="number" step="0.01" className="form-input" placeholder="Ej: 25.00" value={rtHourly} onChange={e => setRtHourly(e.target.value)} />
          </div>
          <button type="submit" disabled={loading} style={{ background: 'var(--orange)', color: '#fff', padding: '10px 16px', borderRadius: '8px', fontSize: '12px', fontWeight: '700', border: 'none', cursor: 'pointer' }}>Guardar Tipo</button>
        </form>
        {rtMsg && <div style={msgStyle(rtMsg)}>{rtMsg}</div>}
      </div>

      {/* Habitaciones */}
      <div style={card}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', marginBottom: '6px' }}>Habitaciones</h2>
        <p style={{ fontSize: '12px', color: 'var(--text-500)', marginBottom: '16px' }}>Asigna un tipo de habitación creado arriba a un número de cuarto.</p>
        <form onSubmit={handleSaveRoom} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div>
            <label style={fieldLabel}>TIPO DE HABITACIÓN</label>
            <select className="form-input" value={rTypeId} onChange={e => setRTypeId(e.target.value)} required>
              <option value="" disabled>-- Selecciona --</option>
              {roomTypes.map(rt => (
                <option key={rt.id} value={rt.id}>{rt.name} — S/. {rt.base_price}/noche{rt.hourly_rate ? ` · S/. ${rt.hourly_rate}/hora` : ''}</option>
              ))}
            </select>
          </div>
          <div>
            <label style={fieldLabel}>Nº HABITACIÓN</label>
            <input type="text" className="form-input" placeholder="Ej: 101" value={rNumber} onChange={e => setRNumber(e.target.value)} required />
          </div>
          <div>
            <label style={fieldLabel}>PISO</label>
            <input type="number" className="form-input" placeholder="1" value={rFloor} onChange={e => setRFloor(e.target.value)} required />
          </div>
          <button type="submit" disabled={loading} style={{ background: 'var(--emerald)', color: '#fff', padding: '10px 16px', borderRadius: '8px', fontSize: '12px', fontWeight: '700', border: 'none', cursor: 'pointer' }}>Guardar Habitación</button>
        </form>
        {rMsg && <div style={msgStyle(rMsg)}>{rMsg}</div>}
      </div>
    </div>
  )
}
INNER_EOF

