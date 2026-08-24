#!/bin/bash
# 1. Add state for users
sed -i '' 's/const \[guests, setGuests\] = useState<Guest\[\]>(\[\])/const [guests, setGuests] = useState<Guest[]>([])\n  const [users, setUsers] = useState<any[]>([])/g' src/app/dashboard/page.tsx

# 2. Add loadUsers function
sed -i '' 's/const loadGuests = useCallback(async (orgId: string) => {/const loadUsers = useCallback(async (orgId: string) => {\n    const { data } = await supabase.from('"'"'user_profiles'"'"').select('"'"'*'"'"').eq('"'"'organization_id'"'"', orgId)\n    if (data) setUsers(data)\n  }, [supabase])\n\n  const loadGuests = useCallback(async (orgId: string) => {/g' src/app/dashboard/page.tsx

# 3. Call loadUsers in useEffect for activeOrgId
sed -i '' 's/loadBranches(activeOrgId)\n      loadGuests(activeOrgId)/loadBranches(activeOrgId)\n      loadGuests(activeOrgId)\n      loadUsers(activeOrgId)/g' src/app/dashboard/page.tsx

# 4. Add to dependency array
sed -i '' 's/}, \[activeOrgId, loadBranches, loadGuests\])/}, [activeOrgId, loadBranches, loadGuests, loadUsers])/g' src/app/dashboard/page.tsx

