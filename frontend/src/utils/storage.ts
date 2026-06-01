/**
 * 本地存储封装
 */

const PREFIX = 'pc_tracker_'

export function setStorage(key: string, value: any, expiry?: number): void {
  const data = {
    value,
    timestamp: Date.now(),
    expiry: expiry ? Date.now() + expiry * 1000 : null,
  }
  localStorage.setItem(`${PREFIX}${key}`, JSON.stringify(data))
}

export function getStorage<T = any>(key: string): T | null {
  const item = localStorage.getItem(`${PREFIX}${key}`)
  if (!item) return null

  try {
    const data = JSON.parse(item)
    if (data.expiry && Date.now() > data.expiry) {
      localStorage.removeItem(`${PREFIX}${key}`)
      return null
    }
    return data.value as T
  } catch {
    return null
  }
}

export function removeStorage(key: string): void {
  localStorage.removeItem(`${PREFIX}${key}`)
}

export function clearStorage(): void {
  const keys = Object.keys(localStorage)
  keys.forEach((key) => {
    if (key.startsWith(PREFIX)) {
      localStorage.removeItem(key)
    }
  })
}
