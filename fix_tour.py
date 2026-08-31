with open('src/app/dashboard/TourGuide.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { Joyride, Step, CallBackProps, STATUS } from 'react-joyride'", "import { Joyride, STATUS } from 'react-joyride'")
content = content.replace("const steps: Record<string, Step[]> =", "const steps: Record<string, any[]> =")
content = content.replace("const handleJoyrideCallback = (data: CallBackProps) => {", "const handleJoyrideCallback = (data: any) => {")

with open('src/app/dashboard/TourGuide.tsx', 'w') as f:
    f.write(content)
