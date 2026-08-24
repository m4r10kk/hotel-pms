#!/bin/bash
# Updating useEffect for loadRoomTypes
sed -i '' 's/loadRooms(activeBranchId)/loadRoomTypes(activeBranchId)\n      loadRooms(activeBranchId)/g' src/app/dashboard/page.tsx
