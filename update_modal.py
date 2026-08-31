import re

with open('src/app/dashboard/page.tsx', 'r') as f:
    content = f.read()

# 1. Add state variables for new guest fields
# We need: resDocType, resDocNum, resFirstName, resLastName, resEmail, resPhone
states = """  const [resStayType, setResStayType] = useState<'NOCHE' | 'HORAS'>('NOCHE')
  const [resCheckInTime, setResCheckInTime] = useState('')
  const [resCheckOutTime, setResCheckOutTime] = useState('')
  const [resTotalPrice, setResTotalPrice] = useState(0)
  
  const [resDocType, setResDocType] = useState('DNI')
  const [resDocNum, setResDocNum] = useState('')
  const [resFirstName, setResFirstName] = useState('')
  const [resLastName, setResLastName] = useState('')"""

content = re.sub(
    r"  const \[resStayType, setResStayType\] = useState\<'NOCHE' \| 'HORAS'\>\('NOCHE'\)\n  const \[resCheckInTime, setResCheckInTime\] = useState\(''\)\n  const \[resCheckOutTime, setResCheckOutTime\] = useState\(''\)\n  const \[resTotalPrice, setResTotalPrice\] = useState\(0\)",
    states,
    content
)

# 2. Update saveNewReservation to use the new fields and search by doc num
old_guest_logic = """    // Create guest on the fly
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
    }"""

new_guest_logic = """    // Check if guest exists by document number
    let guestId = null
    const { data: existingGuest } = await supabase.from('guests').select('id').eq('organization_id', activeOrgId).eq('document_number', resDocNum.trim()).single()
    
    if (existingGuest) {
      guestId = existingGuest.id
    } else {
      // Create new guest
      const { data: guestData, error: guestErr } = await supabase.from('guests').insert({
        organization_id: activeOrgId,
        first_name: resFirstName.trim() || 'Huésped',
        last_name: resLastName.trim() || '-',
        document_type: resDocType,
        document_number: resDocNum.trim() || `TEMP-${Date.now()}`,
      }).select('id').single()

      if (guestErr || !guestData) {
        setResError(`Error al registrar huésped: ${guestErr?.message}`)
        setResSaving(false); return
      }
      guestId = guestData.id
    }"""

content = content.replace(old_guest_logic, new_guest_logic)

# Replace guest validation
content = content.replace(
    "if (!resGuestName.trim()) { setResError('Ingresa el nombre del huésped.'); setResSaving(false); return }",
    "if (!resDocNum.trim() || !resFirstName.trim()) { setResError('Ingresa documento y nombres del huésped.'); setResSaving(false); return }"
)

# Replace guest_id usage
content = content.replace("guest_id: guestData.id,", "guest_id: guestId,")

# Replace form reset
content = content.replace(
    "setResRoomId(''); setResCheckIn(''); setResCheckOut(''); setResGuestName('')",
    "setResRoomId(''); setResCheckIn(''); setResCheckOut(''); setResDocNum(''); setResFirstName(''); setResLastName('')"
)

# 3. Update the form UI to include these fields
old_guest_form = """              {/* Guest name */}
              <div style={{ marginBottom: '13px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-500)', marginBottom: '6px' }}>Nombre del Huésped</label>
                <input type="text" className="form-input" placeholder="Ej: Juan García" value={resGuestName} onChange={e => setResGuestName(e.target.value)} required />
              </div>"""

new_guest_form = """              {/* Guest Details */}
              <div style={{ marginBottom: '13px', display: 'flex', gap: '10px' }}>
                <div style={{ width: '90px' }}>
                  <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-500)', marginBottom: '6px' }}>Tipo</label>
                  <select className="form-input" value={resDocType} onChange={e => setResDocType(e.target.value)} required>
                    <option value="DNI">DNI</option>
                    <option value="PASAPORTE">PAS</option>
                    <option value="CE">CE</option>
                  </select>
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-500)', marginBottom: '6px' }}>Nº Documento</label>
                  <input type="text" className="form-input" placeholder="Ej: 7283..." value={resDocNum} onChange={e => setResDocNum(e.target.value)} required />
                </div>
              </div>
              <div style={{ marginBottom: '13px', display: 'flex', gap: '10px' }}>
                <div style={{ flex: 1 }}>
                  <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-500)', marginBottom: '6px' }}>Nombres</label>
                  <input type="text" className="form-input" placeholder="Ej: Juan" value={resFirstName} onChange={e => setResFirstName(e.target.value)} required />
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-500)', marginBottom: '6px' }}>Apellidos</label>
                  <input type="text" className="form-input" placeholder="Ej: Pérez" value={resLastName} onChange={e => setResLastName(e.target.value)} required />
                </div>
              </div>"""

content = content.replace(old_guest_form, new_guest_form)

# Write back
with open('src/app/dashboard/page.tsx', 'w') as f:
    f.write(content)

