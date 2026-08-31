import re
with open('src/app/dashboard/TourGuide.tsx', 'r') as f:
    content = f.read()

content = content.replace("styles={{ ...{} } as any}", "styles={({")
content = content.replace("buttonSkip: { color: '#9ca3af' }\n        }}", "buttonSkip: { color: '#9ca3af' }\n        }) as any}")

with open('src/app/dashboard/TourGuide.tsx', 'w') as f:
    f.write(content)
