import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

async function run() {
  const { data, error } = await supabase.from('rooms').select('room_number, status')
  if (error) console.error(error)
  else console.log(data)
}
run()
