import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('@/components/layout/AppLayout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘' },
      },
      {
        path: 'apps',
        name: 'Apps',
        component: () => import('@/views/apps/index.vue'),
        meta: { title: '应用记录' },
      },
      {
        path: 'apps/:id',
        name: 'AppDetail',
        component: () => import('@/views/apps/detail.vue'),
        meta: { title: '应用详情' },
      },
      {
        path: 'games',
        name: 'Games',
        component: () => import('@/views/games/index.vue'),
        meta: { title: '游戏记录' },
      },
      {
        path: 'games/:id',
        name: 'GameDetail',
        component: () => import('@/views/games/detail.vue'),
        meta: { title: '游戏详情' },
      },
      {
        path: 'games/add',
        name: 'GameAdd',
        component: () => import('@/views/games/edit.vue'),
        meta: { title: '添加游戏' },
      },
      {
        path: 'games/:id/edit',
        name: 'GameEdit',
        component: () => import('@/views/games/edit.vue'),
        meta: { title: '编辑游戏' },
      },
      {
        path: 'stats',
        name: 'Stats',
        component: () => import('@/views/stats/index.vue'),
        meta: { title: '统计分析' },
      },
      {
        path: 'data',
        name: 'Data',
        component: () => import('@/views/data/index.vue'),
        meta: { title: '数据管理' },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/index.vue'),
        meta: { title: '系统设置' },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫（开发阶段暂时跳过登录验证）
router.beforeEach((to, _from, next) => {
  if (to.path === '/') {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
