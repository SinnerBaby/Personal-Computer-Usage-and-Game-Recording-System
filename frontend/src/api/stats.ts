import request from './index'

export function getUsageTrend(params: any): Promise<any> {
  return request.get('/stats/trend', { params })
}

export function getTimeDistribution(params?: any): Promise<any> {
  return request.get('/stats/time-distribution', { params })
}

export function getAppRanking(params?: any): Promise<any> {
  return request.get('/stats/app-ranking', { params })
}

export function getGameRanking(params?: any): Promise<any> {
  return request.get('/stats/game-ranking', { params })
}

export function getComparison(params: any): Promise<any> {
  return request.get('/stats/comparison', { params })
}
