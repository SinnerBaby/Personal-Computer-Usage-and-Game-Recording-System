<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('trend')
</script>

<template>
  <div class="stats-page">
    <el-card>
      <template #header>
        <span>统计分析</span>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="趋势分析" name="trend">
          <div class="chart-placeholder">
            <el-empty description="趋势图表开发中" />
          </div>
        </el-tab-pane>
        <el-tab-pane label="对比分析" name="comparison">
          <div class="chart-placeholder">
            <el-empty description="对比图表开发中" />
          </div>
        </el-tab-pane>
        <el-tab-pane label="分布分析" name="distribution">
          <div class="chart-placeholder">
            <el-empty description="分布图表开发中" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.stats-page {
  padding: 0;
}

.chart-placeholder {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
