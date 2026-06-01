<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const exportType = ref('apps')
const exportFormat = ref('csv')

function handleExport() {
  ElMessage.info('导出功能开发中')
}

function handleImport() {
  ElMessage.info('导入功能开发中')
}

function handleBackup() {
  ElMessage.info('备份功能开发中')
}
</script>

<template>
  <div class="data-page">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>数据导出</span>
          </template>
          <el-form label-width="80px">
            <el-form-item label="数据类型">
              <el-select v-model="exportType">
                <el-option label="应用记录" value="apps" />
                <el-option label="游戏记录" value="games" />
              </el-select>
            </el-form-item>
            <el-form-item label="导出格式">
              <el-radio-group v-model="exportFormat">
                <el-radio value="csv">CSV</el-radio>
                <el-radio value="json">JSON</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleExport">导出</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header>
            <span>数据导入</span>
          </template>
          <el-upload
            drag
            action="#"
            :auto-upload="false"
            accept=".csv,.json"
          >
            <el-icon :size="48"><UploadFilled /></el-icon>
            <div>拖拽文件到此处或<em>点击上传</em></div>
            <template #tip>
              <div class="el-upload__tip">支持 CSV 和 JSON 格式文件</div>
            </template>
          </el-upload>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>数据库备份</span>
          </template>
          <el-button type="primary" @click="handleBackup">创建备份</el-button>
          <el-empty description="暂无备份记录" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped lang="scss">
.data-page {
  padding: 0;
}

.mt-20 {
  margin-top: 20px;
}
</style>
