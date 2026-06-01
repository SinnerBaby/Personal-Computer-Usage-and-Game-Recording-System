import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getAppList, getAppCategories } from '@/api/apps'

export const useAppsStore = defineStore('apps', () => {
  const appList = ref<any[]>([])
  const categories = ref<any[]>([])
  const loading = ref(false)
  const pagination = ref({
    page: 1,
    pageSize: 20,
    total: 0,
  })

  async function fetchApps(params?: any) {
    loading.value = true
    try {
      const data = await getAppList({
        page: pagination.value.page,
        page_size: pagination.value.pageSize,
        ...params,
      })
      appList.value = data.list
      pagination.value.total = data.pagination.total
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    categories.value = await getAppCategories()
  }

  return {
    appList,
    categories,
    loading,
    pagination,
    fetchApps,
    fetchCategories,
  }
})
