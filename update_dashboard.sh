#!/bin/bash
# Adding room_types state
sed -i '' 's/const \[rooms, setRooms\] = useState<Room\[\]>(\[\])/const [roomTypes, setRoomTypes] = useState<any[]>([])\n  const [rooms, setRooms] = useState<Room[]>([])/g' src/app/dashboard/page.tsx
