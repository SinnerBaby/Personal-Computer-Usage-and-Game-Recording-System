<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const appId = route.params.id
</script>

<template>
  <div class="app-detail">
    <el-card>
      <template #header>
        <span>应用详情 #{{ appId }}</span>
      </template>
      <el-empty description="功能开发中" />
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.app-detail {
  padding: 0;
}
</style>
