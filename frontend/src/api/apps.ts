import request from './index'

export function getAppList(params?: any): Promise<any> {
  return request.get('/apps', { params })
}

export function getAppDetail(id: number): Promise<any> {
  return request.get(`/apps/${id}`)
}

export function getAppCategories(): Promise<any> {
  return request.get('/apps/categories')
}

export function createAppCategory(data: any): Promise<any> {
  return request.post('/apps/categories', data)
}

export function updateAppCategory(id: number, data: any): Promise<any> {
  return request.put(`/apps/categories/${id}`, data)
}

export function deleteAppCategory(id: number): Promise<any> {
  return request.delete(`/apps/categories/${id}`)
}
