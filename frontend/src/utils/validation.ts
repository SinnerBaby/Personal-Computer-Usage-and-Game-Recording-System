/**
 * 表单验证规则
 */

export const required = (message: string = '此项为必填项') => ({
  required: true,
  message,
  trigger: 'blur',
})

export const minLength = (min: number, message?: string) => ({
  min,
  message: message || `长度不能少于 ${min} 个字符`,
  trigger: 'blur',
})

export const maxLength = (max: number, message?: string) => ({
  max,
  message: message || `长度不能超过 ${max} 个字符`,
  trigger: 'blur',
})

export const email = (message: string = '请输入有效的邮箱地址') => ({
  type: 'email',
  message,
  trigger: 'blur',
})

export const pattern = (regex: RegExp, message: string) => ({
  pattern: regex,
  message,
  trigger: 'blur',
})

/**
 * 用户名验证：3-20位字母、数字、下划线
 */
export const usernameRules = [
  required('请输入用户名'),
  minLength(3, '用户名长度不能少于3位'),
  maxLength(20, '用户名长度不能超过20位'),
  pattern(/^[a-zA-Z0-9_]+$/, '用户名只能包含字母、数字和下划线'),
]

/**
 * 密码验证：6-20位
 */
export const passwordRules = [
  required('请输入密码'),
  minLength(6, '密码长度不能少于6位'),
  maxLength(20, '密码长度不能超过20位'),
]

/**
 * 确认密码验证
 */
export const confirmPasswordRules = (getFieldValue: (field: string) => any) => [
  required('请再次输入密码'),
  {
    validator: (_rule: any, value: string, callback: (error?: Error) => void) => {
      if (value !== getFieldValue('password')) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    },
    trigger: 'blur',
  },
]

/**
 * 数字验证
 */
export const numberRules = (message: string = '请输入有效的数字') => [
  required(),
  { type: 'number', message, trigger: 'blur' },
]

/**
 * 评分验证（1-10）
 */
export const ratingRules = [
  { type: 'number', min: 1, max: 10, message: '评分范围为 1-10', trigger: 'blur' },
]
