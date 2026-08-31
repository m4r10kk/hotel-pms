'use server'

import { createClient } from '@supabase/supabase-js'

export async function createEmployee(
  activeOrgId: string,
  adminUserId: string,
  fullName: string,
  email: string,
  passwordTemp: string,
  role: string
) {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY

  if (!supabaseUrl || !serviceRoleKey) {
    return { error: 'Faltan credenciales del servidor (SUPABASE_SERVICE_ROLE_KEY).' }
  }

  const supabaseAdmin = createClient(supabaseUrl, serviceRoleKey, {
    auth: { autoRefreshToken: false, persistSession: false }
  })

  // 1. Verify that the adminUserId is actually a SUPER_ADMIN of the activeOrgId
  const { data: adminProfile, error: adminErr } = await supabaseAdmin
    .from('user_profiles')
    .select('system_role, organization_id')
    .eq('id', adminUserId)
    .single()

  if (adminErr || !adminProfile) {
    return { error: 'No se pudo verificar tu identidad de administrador.' }
  }

  if (adminProfile.system_role !== 'SUPER_ADMIN') {
    return { error: 'Solo un Administrador puede crear empleados.' }
  }

  // Also verify the organization exists
  const { data: orgData } = await supabaseAdmin
    .from('organizations')
    .select('id')
    .eq('id', activeOrgId)
    .single()

  if (!orgData) {
    return { error: 'La empresa seleccionada no existe.' }
  }

  // 2. Create the user in Auth
  const { data: authData, error: authErr } = await supabaseAdmin.auth.admin.createUser({
    email,
    password: passwordTemp,
    email_confirm: true,
    user_metadata: { full_name: fullName }
  })

  if (authErr) {
    return { error: `Error de Auth: ${authErr.message}` }
  }

  const newUserId = authData.user.id

  // 3. Update the user_profiles table (which was created by the DB trigger)
  const { error: profileErr } = await supabaseAdmin
    .from('user_profiles')
    .update({
      system_role: role,
      organization_id: activeOrgId
    })
    .eq('id', newUserId)

  if (profileErr) {
    return { error: `Error actualizando perfil: ${profileErr.message}` }
  }

  return { success: true }
}
