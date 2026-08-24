#!/bin/bash
# Adding loadRoomTypes function
sed -i '' 's/const loadRooms = useCallback(async (branchId: string) => {/const loadRoomTypes = useCallback(async (branchId: string) => {\n    const { data } = await supabase.from('"'"'room_types'"'"').select('"'"'*'"'"').eq('"'"'branch_id'"'"', branchId)\n    if (data) setRoomTypes(data)\n  }, [supabase])\n\n  const loadRooms = useCallback(async (branchId: string) => {/g' src/app/dashboard/page.tsx
