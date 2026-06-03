import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getDashboardOverview,
  getTrendData,
  getUsageTimeline,
  getGameDailyBreakdown,
} from '@/api/dashboard'

export const useDashboardStore = defineStore('dashboard', () => {
  const overview = ref<any>(null)
  const trendData = ref<any>(null)
  const timeline = ref<any>(null)
  const gameBreakdown = ref<any>(null)
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

  async function fetchTimeline(days: number = 7) {
    timeline.value = await getUsageTimeline(days)
  }

  async function fetchGameBreakdown(targetDate?: string) {
    gameBreakdown.value = await getGameDailyBreakdown(targetDate)
  }

  return {
    overview,
    trendData,
    timeline,
    gameBreakdown,
    loading,
    fetchOverview,
    fetchTrend,
    fetchTimeline,
    fetchGameBreakdown,
  }
})
