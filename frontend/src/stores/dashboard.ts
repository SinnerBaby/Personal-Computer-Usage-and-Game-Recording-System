import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDashboardOverview, getTrendData } from '@/api/dashboard'

export const useDashboardStore = defineStore('dashboard', () => {
  const overview = ref<any>(null)
  const trendData = ref<any>(null)
  const loading = ref(false)

  async function fetchOverview() {
    loading.value = true
    try {
      overview.value = await getDashboardOverview()
    } finally {
      loading.value = false
    }
  }

  async function fetchTrend(days: number = 7) {
    trendData.value = await getTrendData(days)
  }

  return {
    overview,
    trendData,
    loading,
    fetchOverview,
    fetchTrend,
  }
})
