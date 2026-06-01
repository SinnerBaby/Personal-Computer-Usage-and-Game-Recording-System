<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import { formatDuration } from '@/utils/format'
import { Monitor, VideoPlay, Timer, TrendCharts } from '@element-plus/icons-vue'

const dashboardStore = useDashboardStore()

onMounted(() => {
  dashboardStore.fetchOverview()
})
</script>

<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #409eff">
            <el-icon><Timer /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">
              {{ formatDuration(dashboardStore.overview?.total_duration || 0) }}
            </div>
            <div class="stat-label">今日总时长</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #67c23a">
            <el-icon><Monitor /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">
              {{ dashboardStore.overview?.app_count || 0 }}
            </div>
            <div class="stat-label">应用数量</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #e6a23c">
            <el-icon><VideoPlay /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">
              {{ formatDuration(dashboardStore.overview?.game_duration || 0) }}
            </div>
            <div class="stat-label">游戏时长</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #f56c6c">
            <el-icon><TrendCharts /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">
              {{ dashboardStore.overview?.game_count || 0 }}
            </div>
            <div class="stat-label">游戏数量</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>使用趋势</span>
          </template>
          <div class="chart-placeholder">
            <el-empty description="图表功能开发中" />
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <span>最常用应用</span>
          </template>
          <div v-if="dashboardStore.overview?.most_used_app" class="most-used">
            <div class="app-name">{{ dashboardStore.overview.most_used_app.name }}</div>
            <div class="app-duration">
              {{ formatDuration(dashboardStore.overview.most_used_app.duration) }}
            </div>
          </div>
          <el-empty v-else description="暂无数据" :image-size="60" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped lang="scss">
.dashboard {
  padding: 0;
}

.stat-card {
  :deep(.el-card__body) {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
  }
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.mt-20 {
  margin-top: 20px;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.most-used {
  text-align: center;
  padding: 20px 0;
}

.app-name {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 8px;
}

.app-duration {
  font-size: 28px;
  font-weight: 600;
  color: #409eff;
}
</style>
