import request from './index'

export function getDashboardOverview(): Promise<any> {
  return request.get('/dashboard/overview')
}

export function getTrendData(days: number = 7): Promise<any> {
  return request.get('/dashboard/trend', { params: { days } })
}

export function getRecentApps(limit: number = 10): Promise<any> {
  return request.get('/dashboard/recent-apps', { params: { limit } })
}

export function getRecentGames(limit: number = 5): Promise<any> {
  return request.get('/dashboard/recent-games', { params: { limit } })
}
