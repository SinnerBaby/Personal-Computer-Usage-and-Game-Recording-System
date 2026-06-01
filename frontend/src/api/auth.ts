import request from './index'

export interface LoginParams {
  username: string
  password: string
}

export interface LoginResult {
  token: string
  refreshToken: string
  user: {
    id: number
    username: string
    nickname: string
  }
}

export function login(data: LoginParams): Promise<LoginResult> {
  return request.post('/auth/login', data)
}

export function refreshToken(refreshToken: string): Promise<{ token: string }> {
  return request.post('/auth/refresh', { refreshToken })
}

export function getUserInfo(): Promise<any> {
  return request.get('/auth/me')
}

export function changePassword(data: { oldPassword: string; newPassword: string }): Promise<any> {
  return request.post('/auth/change-password', data)
}
