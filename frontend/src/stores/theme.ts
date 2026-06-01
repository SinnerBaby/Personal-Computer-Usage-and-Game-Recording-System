import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { usePreferredDark } from '@vueuse/core'

type ThemeMode = 'light' | 'dark' | 'auto'

export const useThemeStore = defineStore('theme', () => {
  const themeMode = ref<ThemeMode>(
    (localStorage.getItem('themeMode') as ThemeMode) || 'auto'
  )
  const systemDark = usePreferredDark()

  const isDark = computed(() => {
    if (themeMode.value === 'auto') return systemDark.value
    return themeMode.value === 'dark'
  })

  function setTheme(mode: ThemeMode) {
    themeMode.value = mode
    localStorage.setItem('themeMode', mode)
  }

  function toggleTheme() {
    const newMode = isDark.value ? 'light' : 'dark'
    setTheme(newMode)
  }

  // 监听主题变化，更新 DOM
  watch(
    isDark,
    (dark) => {
      document.documentElement.classList.toggle('dark', dark)
      document.documentElement.setAttribute(
        'data-theme',
        dark ? 'dark' : 'light'
      )
    },
    { immediate: true }
  )

  return {
    themeMode,
    isDark,
    setTheme,
    toggleTheme,
  }
})
