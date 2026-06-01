<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGamesStore } from '@/stores/games'
import { formatDuration } from '@/utils/format'
import { Plus, Grid, List } from '@element-plus/icons-vue'

const router = useRouter()
const gamesStore = useGamesStore()

onMounted(() => {
  gamesStore.fetchGames()
})

function handleAdd() {
  router.push('/games/add')
}

function handleView(id: number) {
  router.push(`/games/${id}`)
}
</script>

<template>
  <div class="games-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>游戏列表</span>
          <div class="actions">
            <el-radio-group v-model="gamesStore.viewMode" size="small">
              <el-radio-button value="card">
                <el-icon><Grid /></el-icon>
              </el-radio-button>
              <el-radio-button value="list">
                <el-icon><List /></el-icon>
              </el-radio-button>
            </el-radio-group>
            <el-button type="primary" :icon="Plus" @click="handleAdd">
              添加游戏
            </el-button>
          </div>
        </div>
      </template>

      <!-- 卡片视图 -->
      <div v-if="gamesStore.viewMode === 'card'" class="game-grid">
        <el-card
          v-for="game in gamesStore.gameList"
          :key="game.id"
          shadow="hover"
          class="game-card"
          @click="handleView(game.id)"
        >
          <div class="game-cover">
            <el-image
              v-if="game.cover_image"
              :src="game.cover_image"
              fit="cover"
            />
            <div v-else class="cover-placeholder">
              <el-icon :size="48"><VideoPlay /></el-icon>
            </div>
          </div>
          <div class="game-info">
            <h3>{{ game.name }}</h3>
            <div class="game-meta">
              <span>{{ formatDuration(game.total_duration) }}</span>
              <span>{{ game.session_count }} 次游玩</span>
            </div>
            <div v-if="game.tags?.length" class="game-tags">
              <el-tag
                v-for="tag in game.tags.slice(0, 3)"
                :key="tag.id"
                size="small"
                :color="tag.color"
              >
                {{ tag.name }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 列表视图 -->
      <el-table v-else :data="gamesStore.gameList" v-loading="gamesStore.loading" stripe>
        <el-table-column prop="name" label="游戏名称" min-width="150" />
        <el-table-column prop="platform" label="平台" width="100" />
        <el-table-column prop="total_duration" label="总时长" width="120">
          <template #default="{ row }">
            {{ formatDuration(row.total_duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="session_count" label="游玩次数" width="100" />
        <el-table-column prop="rating" label="评分" width="100">
          <template #default="{ row }">
            <el-rate v-model="row.rating" disabled :max="5" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleView(row.id)">
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.games-page {
  padding: 0;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.actions {
  display: flex;
  gap: 12px;
}

.game-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.game-card {
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-4px);
  }
}

.game-cover {
  height: 160px;
  overflow: hidden;
  border-radius: 4px;
  margin-bottom: 12px;
}

.cover-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  color: #c0c4cc;
}

.game-info h3 {
  margin: 0 0 8px;
  font-size: 16px;
  color: #303133;
}

.game-meta {
  font-size: 13px;
  color: #909399;
  display: flex;
  gap: 12px;
}

.game-tags {
  margin-top: 8px;
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
</style>
