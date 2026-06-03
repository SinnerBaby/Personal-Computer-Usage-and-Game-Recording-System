import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getGameList, getGameTags, deleteGame } from '@/api/games'
import { ElMessage } from 'element-plus'

export const useGamesStore = defineStore('games', () => {
  const gameList = ref<any[]>([])
  const tags = ref<any[]>([])
  const loading = ref(false)
  const viewMode = ref<'card' | 'list'>('card')
  const pagination = ref({
    page: 1,
    pageSize: 20,
    total: 0,
  })

  async function fetchGames(params?: any) {
    loading.value = true
    try {
      const data = await getGameList({
        page: pagination.value.page,
        page_size: pagination.value.pageSize,
        ...params,
      })
      gameList.value = data.list
      pagination.value.total = data.pagination.total
    } finally {
      loading.value = false
    }
  }

  async function fetchTags() {
    tags.value = await getGameTags()
  }

  async function removeGame(id: number): Promise<boolean> {
    try {
      await deleteGame(id)
      ElMessage.success('已删除')
      gameList.value = gameList.value.filter(g => g.id !== id)
      pagination.value.total--
      return true
    } catch {
      ElMessage.error('删除失败')
      return false
    }
  }

  function setViewMode(mode: 'card' | 'list') {
    viewMode.value = mode
  }

  return {
    gameList,
    tags,
    loading,
    viewMode,
    pagination,
    fetchGames,
    fetchTags,
    removeGame,
    setViewMode,
  }
})
