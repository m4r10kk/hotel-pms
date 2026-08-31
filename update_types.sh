sed -i '' '/total_amount: number/a\
  stay_type?: string\
  duration_hours?: number\
  check_in_time?: string\
  check_out_time?: string\
' src/lib/types.ts
