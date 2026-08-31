import re

# 1. Fix TourGuide.tsx to use createPortal
with open('src/app/dashboard/TourGuide.tsx', 'r') as f:
    tour_content = f.read()

tour_content = tour_content.replace("import { useState, useEffect } from 'react'", "import { useState, useEffect } from 'react'\nimport { createPortal } from 'react-dom'")
tour_content = tour_content.replace(
    "  return (\n    <>\n      <div style={{ position: 'fixed',",
    "  const tourOverlay = (\n    <>\n      <div style={{ position: 'fixed',"
)
tour_content = tour_content.replace(
    "        </div>\n      </div>\n    </>\n  )\n}",
    "        </div>\n      </div>\n    </>\n  )\n\n  return createPortal(tourOverlay, document.body)\n}"
)
with open('src/app/dashboard/TourGuide.tsx', 'w') as f:
    f.write(tour_content)


# 2. Fix Room Select in page.tsx
with open('src/app/dashboard/page.tsx', 'r') as f:
    page_content = f.read()

# Replace rooms.filter(...) with just rooms.map
old_select = """                  {rooms.filter(r => r.status === 'AVAILABLE').map(r => {
                    const rt = roomTypes.find(t => t.id === (r as any).room_type_id)
                    const rate = resStayType === 'HORAS' && rt?.hourly_rate ? `S/. ${rt.hourly_rate}/hr` : rt ? `S/. ${rt.base_price}/noche` : ''
                    return <option key={r.id} value={r.id}>Hab. {r.room_number} — {rt?.name ?? r.room_type} {rate ? `(${rate})` : ''}</option>
                  })}"""

new_select = """                  {rooms.map(r => {
                    const rt = roomTypes.find(t => t.id === (r as any).room_type_id)
                    const rate = resStayType === 'HORAS' && rt?.hourly_rate ? `S/. ${rt.hourly_rate}/hr` : rt ? `S/. ${rt.base_price}/noche` : ''
                    return <option key={r.id} value={r.id} disabled={r.status !== 'AVAILABLE'}>Hab. {r.room_number} — {rt?.name ?? r.room_type} {rate ? `(${rate})` : ''} {r.status !== 'AVAILABLE' ? '(Ocupada/Sucia)' : ''}</option>
                  })}"""

page_content = page_content.replace(old_select, new_select)

with open('src/app/dashboard/page.tsx', 'w') as f:
    f.write(page_content)

