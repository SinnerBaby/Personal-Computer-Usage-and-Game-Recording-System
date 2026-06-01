/**
 * 将秒数格式化为人类可读的时长
 * @param seconds 秒数
 * @returns 如 "2h 30m" 或 "1h 05m 30s"
 */
export function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  if (h > 0) {
    return s > 0 ? `${h}h ${pad(m)}m ${pad(s)}s` : `${h}h ${pad(m)}m`
  }
  return s > 0 ? `${m}m ${pad(s)}s` : `${m}m`
}

/**
 * 将秒数格式化为紧凑时长（用于图表轴标签）
 */
export function formatDurationShort(seconds: number): string {
  if (seconds < 3600) return `${Math.round(seconds / 60)}m`
  const h = Math.floor(seconds / 3600)
  const m = Math.round((seconds % 3600) / 60)
  return m > 0 ? `${h}.${m}h` : `${h}h`
}

/**
 * 格式化数字（添加千位分隔符）
 */
export function formatNumber(num: number): string {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 格式化百分比
 */
export function formatPercent(value: number, decimals: number = 1): string {
  return `${value.toFixed(decimals)}%`
}

/**
 * 格式化文件大小
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

function pad(n: number): string {
  return n.toString().padStart(2, '0')
}
