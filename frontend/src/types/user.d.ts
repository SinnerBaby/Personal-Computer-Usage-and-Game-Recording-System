export interface User {
  id: number
  username: string
  nickname: string
  avatar: string | null
  created_at: string
  updated_at: string
}

export interface LoginForm {
  username: string
  password: string
}

export interface ChangePasswordForm {
  oldPassword: string
  newPassword: string
  confirmPassword: string
}
