#!/bin/bash
sed -i '' 's/() => loadRoomTypes(activeBranchId)\n      loadRooms(activeBranchId)/() => { loadRoomTypes(activeBranchId); loadRooms(activeBranchId); }/g' src/app/dashboard/page.tsx
