import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getSettings, updateSettings } from '@/api/settings'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<any>({
    idleThreshold: 300,
    syncInterval: 60,
    dataRetentionDays: 365,
    autoCleanup: false,
  })
  const loading = ref(false)

  async function fetchSettings() {
    loading.value = true
    try {
      settings.value = await getSettings()
    } finally {
      loading.value = false
    }
  }

  async function saveSettings(newSettings: any) {
    loading.value = true
    try {
      settings.value = await updateSettings(newSettings)
    } finally {
      loading.value = false
    }
  }

  return {
    settings,
    loading,
    fetchSettings,
    saveSettings,
  }
})
