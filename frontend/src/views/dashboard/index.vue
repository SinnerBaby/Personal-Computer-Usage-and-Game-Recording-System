<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboard'
import { useGamesStore } from '@/stores/games'
import { formatDuration } from '@/utils/format'
import { ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'

const router = useRouter()
const dashboardStore = useDashboardStore()
const gamesStore = useGamesStore()

const barChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()
let barChart: echarts.ECharts | null = null
let pieChart: echarts.ECharts | null = null

const pieDate = ref(new Date().toISOString().slice(0, 10))

onMounted(async () => {
  await Promise.all([
    dashboardStore.fetchOverview(),
    dashboardStore.fetchTimeline(7),
    dashboardStore.fetchGameBreakdown(),
    gamesStore.fetchGames(),
  ])

  nextTick(() => {
    initBarChart()
    initPieChart()
  })
})

watch(() => dashboardStore.timeline, () => {
  nextTick(() => initBarChart())
})

watch(pieDate, (val) => {
  dashboardStore.fetchGameBreakdown(val)
})

watch(() => dashboardStore.gameBreakdown, () => {
  nextTick(() => initPieChart())
})

function initBarChart() {
  if (!barChartRef.value || !dashboardStore.timeline) return
  if (!barChart) {
    barChart = echarts.init(barChartRef.value, null, { renderer: 'canvas' })
  }

  const data = dashboardStore.timeline
  const appData = data.app_usage.map((v: number) => Math.round(v / 60))
  const gameData = data.game_usage.map((v: number) => Math.round(v / 60))

  const labels = data.labels.map((d: string) => {
    const parts = d.split('-')
    return `${parts[1]}/${parts[2]}`
  })

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'var(--bg-elevated, #fff)',
      borderColor: 'var(--border-subtle, #e8e9eb)',
      borderWidth: 1,
      textStyle: { color: 'var(--text-primary, #1a1a2e)', fontSize: 12 },
      valueFormatter: (v: any) => `${v} 分钟`,
    },
    legend: {
      data: ['应用使用', '游戏使用'],
      bottom: 0,
      icon: 'circle',
      itemWidth: 8,
      itemHeight: 8,
      textStyle: { fontSize: 12, color: 'var(--text-secondary, #8e8ea0)' },
    },
    grid: { left: 48, right: 16, bottom: 40, top: 12 },
    xAxis: {
      type: 'category',
      data: labels,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { fontSize: 11, color: 'var(--text-secondary, #8e8ea0)' },
    },
    yAxis: {
      type: 'value',
      name: '分钟',
      nameTextStyle: { fontSize: 11, color: 'var(--text-secondary, #8e8ea0)' },
      splitLine: { lineStyle: { color: 'var(--border-subtle, #e8e9eb)', type: 'dashed' } },
      axisLabel: { fontSize: 11, color: 'var(--text-secondary, #8e8ea0)' },
    },
    series: [
      {
        name: '应用使用',
        type: 'bar',
        stack: 'total',
        data: appData,
        itemStyle: { color: '#2563eb', borderRadius: [3, 3, 0, 0] },
        barMaxWidth: 32,
      },
      {
        name: '游戏使用',
        type: 'bar',
        stack: 'total',
        data: gameData,
        itemStyle: { color: '#f59e0b', borderRadius: [3, 3, 0, 0] },
        barMaxWidth: 32,
      },
    ],
  }

  barChart.setOption(option, true)
  barChart.resize()
}

function initPieChart() {
  if (!pieChartRef.value) return
  if (!pieChart) {
    pieChart = echarts.init(pieChartRef.value, null, { renderer: 'canvas' })
  }

  const games = dashboardStore.gameBreakdown?.games || []

  if (games.length === 0) {
    pieChart.clear()
    pieChart.setOption({
      title: {
        text: '当天无游戏记录',
        left: 'center',
        top: 'center',
        textStyle: { fontSize: 13, color: 'var(--text-secondary, #8e8ea0)', fontWeight: 400 },
      },
    })
    return
  }

  const palette = ['#2563eb', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#06b6d4']

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'var(--bg-elevated, #fff)',
      borderColor: 'var(--border-subtle, #e8e9eb)',
      borderWidth: 1,
      textStyle: { color: 'var(--text-primary, #1a1a2e)', fontSize: 12 },
      formatter: (p: any) => {
        const mins = Math.round(p.value / 60)
        return `<strong>${p.name}</strong><br/>${mins} 分钟 (${p.percent}%)`
      },
    },
    series: [
      {
        type: 'pie',
        radius: ['38%', '62%'],
        center: ['50%', '48%'],
        padAngle: 2,
        data: games.map((g: any, idx: number) => ({
          name: g.name || '未知',
          value: g.duration || 0,
          itemStyle: {
            color: palette[idx % palette.length],
            borderColor: 'var(--bg-card, #fff)',
            borderWidth: 2,
          },
        })),
        label: {
          formatter: (p: any) => `${Math.round(p.value / 60)}m`,
          fontSize: 12,
          fontWeight: 600,
          color: 'var(--text-secondary, #8e8ea0)',
        },
        labelLine: {
          length: 8,
          length2: 10,
          lineStyle: { color: 'var(--border-subtle, #e8e9eb)' },
        },
      },
    ],
  }

  pieChart.setOption(option, true)
  pieChart.resize()
}

/* === 游戏列表辅助函数 === */
function nameColor(name: string): string {
  const colors = [
    '#2563eb', '#10b981', '#f59e0b', '#ef4444',
    '#8b5cf6', '#06b6d4', '#f43f5e', '#14b8a6',
    '#6366f1', '#84cc16', '#eab308', '#ec4899',
  ]
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  return colors[Math.abs(hash) % colors.length]
}

function nameIcon(name: string): string {
  return name.slice(0, 2)
}

function handleViewGame(id: number) {
  router.push(`/games/${id}`)
}

function handleAddGame() {
  router.push('/games/add')
}

function handleDeleteGame(id: number, name: string) {
  ElMessageBox.confirm(
    `确定要删除游戏「${name}」吗？相关的游玩记录也会一并删除。`,
    '删除确认',
    {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    gamesStore.removeGame(id)
  }).catch(() => {})
}

import { useResizeObserver } from '@vueuse/core'
useResizeObserver(barChartRef, () => barChart?.resize())
useResizeObserver(pieChartRef, () => pieChart?.resize())
</script>

<template>
  <div class="dashboard">
    <!-- 统计卡片区 -->
    <div class="stats-grid">
      <div class="stat-card stat-total">
        <div class="stat-label">今日总时长</div>
        <div class="stat-value">{{ formatDuration(dashboardStore.overview?.total_duration || 0) }}</div>
        <div v-if="dashboardStore.overview?.vs_yesterday?.total_change !== 0" class="stat-trend">
          <span :class="dashboardStore.overview?.vs_yesterday?.total_change > 0 ? 'up' : 'down'">
            {{ dashboardStore.overview?.vs_yesterday?.total_change > 0 ? '↑' : '↓' }}
            {{ Math.abs(dashboardStore.overview?.vs_yesterday?.total_change_pct || 0) }}%
          </span>
          <span class="trend-label">vs 昨日</span>
        </div>
      </div>

      <div class="stat-card stat-apps">
        <div class="stat-label">应用数量</div>
        <div class="stat-value">{{ dashboardStore.overview?.app_count || 0 }}</div>
        <div class="stat-meta">{{ dashboardStore.overview?.total_duration ? '有活跃记录的应用' : '暂无数据' }}</div>
      </div>

      <div class="stat-card stat-game">
        <div class="stat-label">游戏时长</div>
        <div class="stat-value">{{ formatDuration(dashboardStore.overview?.game_duration || 0) }}</div>
        <div class="stat-meta">{{ dashboardStore.overview?.game_count ? '今日有游戏记录' : '今日未玩' }}</div>
      </div>

      <div class="stat-card stat-count">
        <div class="stat-label">游戏数量</div>
        <div class="stat-value">{{ dashboardStore.overview?.game_count || 0 }}</div>
        <div class="stat-meta">已收录的游戏总数</div>
      </div>
    </div>

    <!-- 图表区 -->
    <div class="charts-grid">
      <div class="chart-card">
        <div class="chart-header">
          <h3>使用趋势</h3>
        </div>
        <div ref="barChartRef" class="chart-body" />
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3>游戏日占比</h3>
          <el-date-picker
            v-model="pieDate"
            type="date"
            size="small"
            placeholder="选择日期"
            style="width: 136px"
            value-format="YYYY-MM-DD"
          />
        </div>
        <div ref="pieChartRef" class="chart-body chart-pie" />
      </div>
    </div>

    <!-- 游戏记录区 -->
    <section class="games-section">
      <div class="section-header">
        <h3>游戏记录</h3>
        <div class="section-actions">
          <el-radio-group v-model="gamesStore.viewMode" size="small">
            <el-radio-button value="card">卡片</el-radio-button>
            <el-radio-button value="list">列表</el-radio-button>
          </el-radio-group>
          <el-button type="primary" size="small" @click="handleAddGame">
            添加游戏
          </el-button>
        </div>
      </div>

      <!-- 卡片视图 -->
      <div v-if="gamesStore.viewMode === 'card'" class="game-grid">
        <div
          v-for="(game, idx) in gamesStore.gameList"
          :key="game.id"
          class="game-card"
          :style="{ animationDelay: `${idx * 0.04}s` }"
        >
          <div class="game-cover" @click="handleViewGame(game.id)">
            <div v-if="game.cover_image" class="cover-bg-cover">
              <div
                class="cover-img-bg"
                :style="{ backgroundImage: `url(/api/v1/games/${game.id}/cover)` }"
              ></div>
              <img
                :src="'/api/v1/games/' + game.id + '/cover'"
                class="cover-img"
                :alt="game.name"
                loading="lazy"
              />
              <button class="delete-btn" title="删除" @click.stop="handleDeleteGame(game.id, game.name)">✕</button>
            </div>
            <!-- 无封面时用图标占位 -->
            <div
              v-else
              class="cover-bg"
              :style="{ background: `linear-gradient(135deg, ${nameColor(game.name)}22, ${nameColor(game.name)}08)` }"
            >
              <el-image
                v-if="game.exe_path"
                :src="'/api/v1/games/' + game.id + '/icon'"
                class="icon-img"
                fit="contain"
              >
                <template #error>
                  <span class="cover-letter" :style="{ color: nameColor(game.name) }">{{ nameIcon(game.name) }}</span>
                </template>
              </el-image>
              <span v-else class="cover-letter" :style="{ color: nameColor(game.name) }">
                {{ nameIcon(game.name) }}
              </span>
              <button class="delete-btn" title="删除" @click.stop="handleDeleteGame(game.id, game.name)">✕</button>
            </div>
          </div>
          <div class="game-info" @click="handleViewGame(game.id)">
            <h4>{{ game.name }}</h4>
            <div class="game-meta">
              <span>{{ formatDuration(game.total_duration) }}</span>
              <span class="meta-divider">·</span>
              <span>{{ game.session_count }} 次游玩</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 列表视图 -->
      <div v-else class="table-wrapper">
        <el-table :data="gamesStore.gameList" v-loading="gamesStore.loading" stripe>
          <el-table-column label="" width="48">
            <template #default="{ row }">
              <div class="list-icon" :style="{ background: nameColor(row.name) + '18' }">
                <span :style="{ color: nameColor(row.name) }">{{ nameIcon(row.name) }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="游戏名称" min-width="140" />
          <el-table-column prop="total_duration" label="总时长" width="90">
            <template #default="{ row }">{{ formatDuration(row.total_duration) }}</template>
          </el-table-column>
          <el-table-column prop="session_count" label="游玩次数" width="80" />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button type="primary" link @click="handleViewGame(row.id)">查看</el-button>
              <el-button type="danger" link @click="handleDeleteGame(row.id, row.name)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ===== 统计卡片 ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  border-radius: var(--radius-md);
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  transition: box-shadow 0.2s, transform 0.2s;

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.5px;
  line-height: 1.2;
  margin-bottom: 6px;
}

.stat-total { border-left: 3px solid #2563eb; }
.stat-apps { border-left: 3px solid #10b981; }
.stat-game { border-left: 3px solid #f59e0b; }
.stat-count { border-left: 3px solid #8b5cf6; }

.stat-trend {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;

  .up { color: #10b981; font-weight: 600; }
  .down { color: #ef4444; font-weight: 600; }
  .trend-label { color: var(--text-secondary); }
}

.stat-meta {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.3;
}

/* ===== 图表区 ===== */
.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}

.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: box-shadow 0.2s;

  &:hover { box-shadow: var(--shadow-md); }
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px 0;

  h3 {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
  }
}

.chart-body {
  height: 300px;
  width: 100%;
}

.chart-pie { height: 280px; }

/* ===== 游戏记录区 ===== */
.games-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  h3 {
    font-size: 17px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
  }
}

.section-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* 游戏卡片 grid */
.game-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 14px;
}

.game-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
  animation: fadeInUp 0.3s ease-out both;

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-3px);
  }
}

.game-cover {
  position: relative;
  height: 120px;
  overflow: hidden;
}

.cover-bg-cover {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.cover-img-bg {
  position: absolute;
  inset: -30px;
  background-size: cover;
  background-position: center;
  filter: blur(18px);
  opacity: 0.5;
}

.cover-img {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  padding: 6px;
}

.cover-bg {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;

  :deep(.el-image) {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  :deep(.el-image__inner) {
    width: auto;
    height: auto;
    max-width: 75%;
    max-height: 75%;
    object-fit: contain;
  }

  :deep(.el-image__error) {
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    height: auto;
    width: auto;
  }
}

.cover-letter {
  font-size: 40px;
  font-weight: bold;
  opacity: 0.8;
  line-height: 1;
}

.delete-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  border: none;
  background: rgba(0, 0, 0, 0.35);
  color: #fff;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s, background 0.2s;

  .game-card:hover & { opacity: 1; }
  &:hover { background: #ef4444; }
}

.game-info {
  padding: 10px 14px 12px;

  h4 {
    margin: 0 0 4px;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.game-meta {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  gap: 4px;

  .meta-divider { color: var(--border-default); }
}

/* 列表视图 */
.table-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.list-icon {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
