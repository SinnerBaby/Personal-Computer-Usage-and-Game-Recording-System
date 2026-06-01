<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/dashboard')
}
</script>

<template>
  <div class="error-page">
    <div class="error-content">
      <h1>404</h1>
      <p>页面不存在</p>
      <el-button type="primary" @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.error-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f5f7fa;
}

.error-content {
  text-align: center;

  h1 {
    font-size: 120px;
    font-weight: bold;
    color: #409eff;
    margin: 0;
    line-height: 1;
  }

  p {
    font-size: 24px;
    color: #909399;
    margin: 20px 0 30px;
  }
}
</style>
