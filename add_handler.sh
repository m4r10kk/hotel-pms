#!/bin/bash
cat << 'INNER_EOF' > /Users/marlok/Desktop/California/handler.txt

  async function handleCreateEmployee(e: React.FormEvent) {
    e.preventDefault()
    if (!activeOrgId) return alert('Selecciona una empresa primero')
    
    // We need the admin's UUID
    const { data: { session } } = await supabase.auth.getSession()
    if (!session?.user?.id) return alert('No hay sesión de administrador activa')

    setEmpLoading(true)
    const result = await createEmployee(
      activeOrgId,
      session.user.id,
      empName,
      empEmail,
      empPass,
      empRole
    )
    setEmpLoading(false)

    if (result.error) {
      alert(result.error)
    } else {
      alert('Empleado creado exitosamente.')
      setEmpName('')
      setEmpEmail('')
      setEmpPass('')
      setEmpRole('FRONT_DESK')
      loadUsers(activeOrgId)
    }
  }

INNER_EOF

# Insert right before return (
sed -i '' '/return (/e cat \/Users\/marlok\/Desktop\/California\/handler.txt' src/app/dashboard/page.tsx

