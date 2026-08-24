#!/bin/bash
# Insert import
sed -i '' 's/import { Guest } from '"'"'@\/lib\/types'"'"'/import { Guest } from '"'"'@\/lib\/types'"'"'\nimport SettingsView from '"'"'.\/SettingsView'"'"'/g' src/app/dashboard/page.tsx

# Inject View
sed -i '' 's/          {activeView === '"'"'users'"'"' && (/          {activeView === '"'"'settings'"'"' \&\& <SettingsView activeBranchId={activeBranchId} roomTypes={roomTypes} onRefresh={() => { loadRoomTypes(activeBranchId); loadRooms(activeBranchId); }} \/>}\n\n          {activeView === '"'"'users'"'"' \&\& (/g' src/app/dashboard/page.tsx
