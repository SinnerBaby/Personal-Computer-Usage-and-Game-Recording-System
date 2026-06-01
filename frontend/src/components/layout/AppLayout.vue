<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const isCollapse = ref(false)

const menuItems = [
  { path: '/dashboard', title: '仪表盘' },
  { path: '/apps', title: '应用记录' },
  { path: '/games', title: '游戏记录' },
  { path: '/stats', title: '统计分析' },
  { path: '/data', title: '数据管理' },
  { path: '/settings', title: '系统设置' },
]

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <el-container class="layout-container">
    <el-aside :width="isCollapse ? '64px' : '220px'" class="layout-aside">
      <div class="logo">
        <span v-if="!isCollapse">PC Tracker</span>
        <span v-else>PC</span>
      </div>

      <el-menu
        :default-active="route.path"
        :collapse="isCollapse"
        router
        class="aside-menu"
      >
        <el-menu-item
          v-for="item in menuItems"
          :key="item.path"
          :index="item.path"
        >
          <template #title>{{ item.title }}</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="layout-header">
        <div class="header-left">
          <el-button @click="isCollapse = !isCollapse">
            {{ isCollapse ? '展开' : '收起' }}
          </el-button>
          <span class="page-title">{{ route.meta.title }}</span>
        </div>

        <div class="header-right">
          <el-switch
            v-model="themeStore.isDark"
            inline-prompt
            active-text="暗"
            inactive-text="亮"
            @change="themeStore.toggleTheme()"
          />
          <el-dropdown @command="handleLogout">
            <span class="user-info">
              {{ authStore.userInfo?.nickname || '用户' }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
}

.layout-aside {
  background: #141414;
  transition: width 0.3s;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  border-bottom: 1px solid #2d2d2d;
}

.aside-menu {
  border-right: none;
  background: transparent;

  :deep(.el-menu-item) {
    color: #bfcbd9;

    &:hover {
      background: #263445;
      color: #fff;
    }

    &.is-active {
      color: #409eff;
      background: #1a2a3a;
    }
  }

  :deep(.el-menu-item.is-active) {
    color: #409eff;
  }
}

.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #dcdfe6;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  color: #606266;
}

.layout-main {
  background: #f5f7fa;
  overflow-y: auto;
}
</style>
