import request from './index'

export function getGameList(params?: any): Promise<any> {
  return request.get('/games', { params })
}

export function getGameDetail(id: number): Promise<any> {
  return request.get(`/games/${id}`)
}

export function createGame(data: any): Promise<any> {
  return request.post('/games', data)
}

export function updateGame(id: number, data: any): Promise<any> {
  return request.put(`/games/${id}`, data)
}

export function deleteGame(id: number): Promise<any> {
  return request.delete(`/games/${id}`)
}

export function getGameTags(): Promise<any> {
  return request.get('/games/tags')
}

export function createGameTag(data: any): Promise<any> {
  return request.post('/games/tags', data)
}

export function getGameSessions(gameId: number, params?: any): Promise<any> {
  return request.get(`/games/${gameId}/sessions`, { params })
}

export function addGameSession(gameId: number, data: any): Promise<any> {
  return request.post(`/games/${gameId}/sessions`, data)
}
