<script setup lang="ts">
import { useThemeStore } from './stores/theme'

const themeStore = useThemeStore()
</script>

<template>
  <el-config-provider>
    <router-view />
  </el-config-provider>
</template>

<style lang="scss">
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif;
}

#app {
  height: 100%;
}
</style>
