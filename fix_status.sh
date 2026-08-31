#!/bin/bash
sed -i '' 's/r\.status/r\.current_status/g' src/app/dashboard/page.tsx
sed -i '' 's/rm\.status/rm\.current_status/g' src/app/dashboard/page.tsx
sed -i '' 's/r\.current_status \!==/r\.current_status \!==/g' src/app/dashboard/page.tsx
