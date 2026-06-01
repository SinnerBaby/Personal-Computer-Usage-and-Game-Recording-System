import request from './index'

export function getSettings(): Promise<any> {
  return request.get('/settings')
}

export function updateSettings(data: any): Promise<any> {
  return request.put('/settings', data)
}

export function exportData(params: any): Promise<any> {
  return request.post('/data/export', params, { responseType: 'blob' })
}

export function importData(file: File): Promise<any> {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/data/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function createBackup(): Promise<any> {
  return request.post('/data/backup')
}

export function getBackupList(): Promise<any> {
  return request.get('/data/backups')
}

export function restoreBackup(id: number): Promise<any> {
  return request.post(`/data/backups/${id}/restore`)
}

export function cleanupData(params: any): Promise<any> {
  return request.post('/data/cleanup', params)
}
