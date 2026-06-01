export interface Game {
  id: number
  name: string
  developer: string | null
  publisher: string | null
  platform: string | null
  purchase_price: number | null
  purchase_date: string | null
  cover_image: string | null
  rating: number | null
  notes: string | null
  total_duration: number
  session_count: number
  last_played_at: string | null
  tags: GameTag[]
  created_at: string
  updated_at: string
}

export interface GameTag {
  id: number
  name: string
  color: string | null
}

export interface GameSession {
  id: number
  game_id: number
  start_time: string
  end_time: string | null
  duration: number
  date: string
}
