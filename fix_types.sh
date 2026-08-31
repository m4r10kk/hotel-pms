#!/bin/bash
sed -i '' 's/status: RoomStatus/current_status: RoomStatus/g' src/lib/types.ts
