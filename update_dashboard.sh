#!/bin/bash
set -e

echo "Adding states..."
# Add state variables right after resSaving
sed -i '' '/const \[resError/a\
  const [resStayType, setResStayType] = useState<'"'"'NOCHE'"'"' | '"'"'HORAS'"'"'>('"'"'NOCHE'"'"')\
  const [resCheckInTime, setResCheckInTime] = useState('"'"''"'"')\
  const [resCheckOutTime, setResCheckOutTime] = useState('"'"''"'"')\
  const [resTotalPrice, setResTotalPrice] = useState(0)\
' src/app/dashboard/page.tsx

echo "Updating SettingsView tag..."
# Replace SettingsView call
sed -i '' 's/<SettingsView activeOrgId={activeOrgId} activeBranchId={activeBranchId} roomTypes={roomTypes} onRefreshOrg={() => loadBranches(activeOrgId)} onRefresh={() => { loadRoomTypes(activeBranchId); loadRooms(activeBranchId); }} \/>/<SettingsView activeOrgId={activeOrgId} activeBranchId={activeBranchId} roomTypes={roomTypes} onRefreshOrg={() => loadBranches(activeOrgId)} onBranchCreated={(id) => { setActiveBranchId(id); loadBranches(activeOrgId); }} onRefresh={() => { loadRoomTypes(activeBranchId); loadRooms(activeBranchId); }} \/>/g' src/app/dashboard/page.tsx

