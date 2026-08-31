with open('src/app/dashboard/TourGuide.tsx', 'r') as f:
    content = f.read()

content = content.replace("<Joyride\n", "{/* @ts-ignore */}\n      <Joyride\n")

with open('src/app/dashboard/TourGuide.tsx', 'w') as f:
    f.write(content)
