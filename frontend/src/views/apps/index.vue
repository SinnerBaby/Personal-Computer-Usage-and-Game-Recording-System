<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAppsStore } from '@/stores/apps'
import { formatDuration } from '@/utils/format'

const appsStore = useAppsStore()
const searchName = ref('')

onMounted(() => {
  appsStore.fetchApps()
})
</script>

<template>
  <div class="apps-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>应用使用记录</span>
          <div class="filters">
            <el-input
              v-model="searchName"
              placeholder="搜索应用"
              clearable
              style="width: 200px"
            />
          </div>
        </div>
      </template>

      <el-table :data="appsStore.appList" v-loading="appsStore.loading" stripe>
        <el-table-column prop="app_name" label="应用名称" min-width="150" />
        <el-table-column prop="process_name" label="进程名" min-width="120" />
        <el-table-column prop="duration" label="使用时长" width="120">
          <template #default="{ row }">
            {{ formatDuration(row.duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="180" />
        <el-table-column prop="date" label="日期" width="120" />
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="appsStore.pagination.page"
          v-model:page-size="appsStore.pagination.pageSize"
          :total="appsStore.pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="appsStore.fetchApps()"
          @size-change="appsStore.fetchApps()"
        />
      </div>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.apps-page {
  padding: 0;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
