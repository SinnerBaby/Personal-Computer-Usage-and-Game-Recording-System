import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, refreshToken as refreshTokenApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const refreshTokenValue = ref<string>(localStorage.getItem('refreshToken') || '')
  const userInfo = ref<any>(null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(username: string, password: string) {
    const data = await loginApi({ username, password })
    token.value = data.token
    refreshTokenValue.value = data.refreshToken
    userInfo.value = data.user
    localStorage.setItem('token', data.token)
    localStorage.setItem('refreshToken', data.refreshToken)
    return data
  }

  async function refresh() {
    if (!refreshTokenValue.value) return
    const data = await refreshTokenApi(refreshTokenValue.value)
    token.value = data.token
    localStorage.setItem('token', data.token)
    return data
  }

  function logout() {
    token.value = ''
    refreshTokenValue.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }

  return {
    token,
    refreshToken: refreshTokenValue,
    userInfo,
    isLoggedIn,
    login,
    refresh,
    logout,
  }
})
