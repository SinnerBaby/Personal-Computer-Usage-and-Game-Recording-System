<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import {
  Monitor,
  Grid,
  VideoPlay,
  TrendCharts,
  FolderOpened,
  Setting,
  ArrowDown,
  Sunny,
  Moon,
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const menuItems = [
  { path: '/dashboard', title: '首页', icon: Monitor },
  { path: '/apps', title: '应用记录', icon: Grid },
  { path: '/games', title: '游戏记录', icon: VideoPlay },
  { path: '/stats', title: '统计分析', icon: TrendCharts },
  { path: '/data', title: '数据管理', icon: FolderOpened },
  { path: '/settings', title: '系统设置', icon: Setting },
]
</script>

<template>
  <div class="app-wrapper">
    <header class="top-header">
      <div class="header-inner">
        <router-link to="/dashboard" class="logo">
          <div class="logo-mark" />
          <span class="logo-text">PC Tracker</span>
        </router-link>

        <nav class="nav-links">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-link"
            :class="{ active: route.path.startsWith(item.path) }"
          >
            <component :is="item.icon" class="nav-icon" />
            {{ item.title }}
          </router-link>
        </nav>

        <div class="header-actions">
          <button
            class="theme-btn"
            :title="themeStore.isDark ? '切换到亮色' : '切换到暗色'"
            @click="themeStore.toggleTheme()"
          >
            <span v-if="themeStore.isDark" class="icon-sun"><Sunny /></span>
            <span v-else class="icon-moon"><Moon /></span>
          </button>

          <el-dropdown trigger="click">
            <button class="user-btn">
              <span class="user-avatar">{{ (authStore.userInfo?.nickname || '用')[0] }}</span>
              <span class="user-name">{{ authStore.userInfo?.nickname || '用户' }}</span>
              <el-icon class="arrow"><ArrowDown /></el-icon>
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped lang="scss">
.app-wrapper {
  min-height: 100vh;
  background: var(--bg-body);
  display: flex;
  flex-direction: column;
}

/* ===== 顶部导航 ===== */
.top-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-subtle);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.header-inner {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 52px;
  padding: 0 24px;
  gap: 32px;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-mark {
  width: 28px;
  height: 28px;
  background: var(--accent);
  border-radius: 7px;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    inset: 5px;
    background: #fff;
    border-radius: 3px;
    opacity: 0.85;
  }
}

.logo-text {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}

/* 导航链接 */
.nav-links {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 52px;
  padding: 0 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
  white-space: nowrap;
  position: relative;

  .nav-icon {
    font-size: 16px;
    opacity: 0.7;
    transition: opacity 0.2s;
  }

  &:hover {
    color: var(--text-primary);

    .nav-icon {
      opacity: 1;
    }
  }

  &.active {
    color: var(--accent);
    border-bottom-color: var(--accent);

    .nav-icon {
      opacity: 1;
    }
  }
}

/* 右侧操作区 */
.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.theme-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  transition: background 0.2s, color 0.2s;

  &:hover {
    background: var(--bg-subtle);
    color: var(--text-primary);
  }
}

.icon-sun { color: #f59e0b; }
.icon-moon { color: #6366f1; }

.user-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 4px;
  border-radius: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: var(--bg-subtle);
  }
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 7px;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;
}

.user-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.arrow {
  font-size: 10px;
  color: var(--text-secondary);
}

/* ===== 主内容区 ===== */
.main-content {
  flex: 1;
  padding: 20px 24px;
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
}

/* ===== 路由切换动画 ===== */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
