<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const gameId = route.params.id
const game = ref(null)
const loading = ref(false)
</script>

<template>
  <div class="game-detail">
    <el-card v-loading="loading">
      <template #header>
        <span>游戏详情 #{{ gameId }}</span>
      </template>
      <el-empty description="功能开发中" />
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.game-detail {
  padding: 0;
}
</style>
