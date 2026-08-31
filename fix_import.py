with open('src/app/dashboard/TourGuide.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "import Joyride, { Step, CallBackProps, STATUS } from 'react-joyride'",
    "import { Joyride, Step, CallBackProps, STATUS } from 'react-joyride'"
)

with open('src/app/dashboard/TourGuide.tsx', 'w') as f:
    f.write(content)
