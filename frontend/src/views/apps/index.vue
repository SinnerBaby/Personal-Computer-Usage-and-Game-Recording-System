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
  <section class="apps-section">
    <div class="section-header">
      <h2>应用使用记录</h2>
      <div class="section-actions">
        <el-input
          v-model="searchName"
          placeholder="搜索应用"
          clearable
          style="width: 200px"
        />
      </div>
    </div>

    <div class="table-wrapper">

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
    </div>
  </section>
</template>

<style scoped lang="scss">
.apps-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  h2 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
  }
}

.section-actions {
  display: flex;
  gap: 12px;
}

.table-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.pagination {
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid var(--border-subtle);
}
</style>
