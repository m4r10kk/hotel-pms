with open('src/app/dashboard/TourGuide.tsx', 'r') as f:
    content = f.read()

content = content.replace("showProgress={true}\n", "")
content = content.replace("showSkipButton={true}\n", "")

with open('src/app/dashboard/TourGuide.tsx', 'w') as f:
    f.write(content)
