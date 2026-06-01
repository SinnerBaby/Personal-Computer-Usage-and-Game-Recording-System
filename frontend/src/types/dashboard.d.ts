export interface DashboardOverview {
  total_duration: number
  active_duration: number
  idle_duration: number
  game_duration: number
  app_count: number
  game_count: number
  vs_yesterday: {
    total_change: number
    total_change_pct: number
    game_change: number
    game_change_pct: number
  }
  most_used_app: { name: string; duration: number } | null
  most_played_game: { name: string; duration: number } | null
}

export interface TrendData {
  labels: string[]
  series: {
    total_duration: number[]
    active_duration: number[]
    game_duration: number[]
  }
  summary: {
    avg_daily_total: number
    avg_daily_game: number
    max_day: string
    max_duration: number
  }
}
