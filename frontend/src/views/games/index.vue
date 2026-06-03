<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGamesStore } from '@/stores/games'
import { formatDuration } from '@/utils/format'
import { ElMessageBox } from 'element-plus'

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

function handleDelete(id: number, name: string) {
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
</script>

<template>
  <section class="games-section">
    <div class="section-header">
      <h2>游戏列表</h2>
      <div class="section-actions">
        <el-radio-group v-model="gamesStore.viewMode" size="small">
          <el-radio-button value="card">卡片</el-radio-button>
          <el-radio-button value="list">列表</el-radio-button>
        </el-radio-group>
        <el-button type="primary" @click="handleAdd">
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
        :style="{ animationDelay: `${idx * 0.05}s` }"
      >
        <div class="game-cover" @click="handleView(game.id)">
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
            <button class="delete-btn" title="删除" @click.stop="handleDelete(game.id, game.name)">✕</button>
          </div>
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
            <span v-else class="cover-letter" :style="{ color: nameColor(game.name) }">{{ nameIcon(game.name) }}</span>
            <button class="delete-btn" title="删除" @click.stop="handleDelete(game.id, game.name)">✕</button>
          </div>
        </div>

        <div class="game-info" @click="handleView(game.id)">
          <h3>{{ game.name }}</h3>
          <div class="game-meta">
            <span class="meta-duration">{{ formatDuration(game.total_duration) }}</span>
            <span class="meta-divider">·</span>
            <span class="meta-sessions">{{ game.session_count }} 次游玩</span>
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
      </div>
    </div>

    <!-- 列表视图 -->
    <div v-else class="list-container">
      <el-table :data="gamesStore.gameList" v-loading="gamesStore.loading" stripe>
        <el-table-column label="" width="52">
          <template #default="{ row }">
            <div class="list-icon" :style="{ background: nameColor(row.name) + '18' }">
              <span :style="{ color: nameColor(row.name) }">{{ nameIcon(row.name) }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="游戏名称" min-width="150" />
        <el-table-column prop="platform" label="平台" width="100" />
        <el-table-column prop="total_duration" label="总时长" width="100">
          <template #default="{ row }">
            {{ formatDuration(row.total_duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="session_count" label="游玩次数" width="80" />
        <el-table-column prop="rating" label="评分" width="120">
          <template #default="{ row }">
            <el-rate v-model="row.rating" disabled :max="5" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="130">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleView(row.id)">查看</el-button>
            <el-button type="danger" link @click="handleDelete(row.id, row.name)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </section>
</template>

<style scoped lang="scss">
.games-section {
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
  gap: 10px;
  align-items: center;
}

/* ===== 卡片视图 ===== */
.game-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 16px;
}

.game-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
  animation: fadeInUp 0.35s ease-out both;

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-3px);
  }
}

.game-cover {
  position: relative;
  height: 140px;
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
    max-width: 80%;
    max-height: 80%;
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
  font-size: 46px;
  font-weight: bold;
  opacity: 0.8;
  line-height: 1;
}

.delete-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border-radius: 7px;
  border: none;
  background: rgba(0, 0, 0, 0.35);
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s, background 0.2s;

  .game-card:hover & {
    opacity: 1;
  }

  &:hover {
    background: #ef4444;
  }
}

.game-info {
  padding: 12px 14px 14px;

  h3 {
    margin: 0 0 6px;
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.game-meta {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  gap: 4px;

  .meta-duration {
    font-variant-numeric: tabular-nums;
    font-weight: 500;
    color: var(--text-regular);
  }

  .meta-divider {
    color: var(--border-default);
  }
}

.game-tags {
  margin-top: 8px;
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

/* ===== 列表视图 ===== */
.list-container {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.list-icon {
  width: 32px;
  height: 32px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
