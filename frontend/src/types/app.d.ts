export interface AppUsage {
  id: number
  app_name: string
  window_title: string | null
  process_name: string
  category: AppCategory | null
  start_time: string
  end_time: string | null
  duration: number
  is_idle: boolean
  date: string
}

export interface AppCategory {
  id: number
  name: string
  icon: string | null
  color: string | null
  sort_order: number
}
