/**
 * 日期工具函数
 */

/**
 * 格式化日期为 YYYY-MM-DD
 */
export function formatDate(date: Date | string): string {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

/**
 * 格式化时间为 HH:mm:ss
 */
export function formatTime(date: Date | string): string {
  const d = new Date(date)
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  return `${hours}:${minutes}:${seconds}`
}

/**
 * 格式化日期时间为 YYYY-MM-DD HH:mm:ss
 */
export function formatDateTime(date: Date | string): string {
  return `${formatDate(date)} ${formatTime(date)}`
}

/**
 * 获取今天的日期字符串
 */
export function getToday(): string {
  return formatDate(new Date())
}

/**
 * 获取昨天的日期字符串
 */
export function getYesterday(): string {
  const date = new Date()
  date.setDate(date.getDate() - 1)
  return formatDate(date)
}

/**
 * 获取本周的起止日期
 */
export function getWeekRange(): { start: string; end: string } {
  const now = new Date()
  const dayOfWeek = now.getDay()
  const start = new Date(now)
  start.setDate(now.getDate() - dayOfWeek + 1)
  const end = new Date(start)
  end.setDate(start.getDate() + 6)
  return { start: formatDate(start), end: formatDate(end) }
}

/**
 * 获取本月的起止日期
 */
export function getMonthRange(): { start: string; end: string } {
  const now = new Date()
  const start = new Date(now.getFullYear(), now.getMonth(), 1)
  const end = new Date(now.getFullYear(), now.getMonth() + 1, 0)
  return { start: formatDate(start), end: formatDate(end) }
}

/**
 * 计算两个日期之间的天数差
 */
export function daysBetween(date1: string, date2: string): number {
  const d1 = new Date(date1)
  const d2 = new Date(date2)
  const diffTime = Math.abs(d2.getTime() - d1.getTime())
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

/**
 * 判断是否是今天
 */
export function isToday(date: string): boolean {
  return formatDate(new Date()) === date
}

/**
 * 判断是否是本周
 */
export function isThisWeek(date: string): boolean {
  const { start, end } = getWeekRange()
  return date >= start && date <= end
}
