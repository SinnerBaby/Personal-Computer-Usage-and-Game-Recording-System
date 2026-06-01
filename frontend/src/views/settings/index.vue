<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useThemeStore } from '@/stores/theme'
import { ElMessage } from 'element-plus'

const settingsStore = useSettingsStore()
const themeStore = useThemeStore()

onMounted(() => {
  settingsStore.fetchSettings()
})

function handleSave() {
  settingsStore.saveSettings(settingsStore.settings)
  ElMessage.success('保存成功')
}
</script>

<template>
  <div class="settings-page">
    <el-card>
      <template #header>
        <span>系统设置</span>
      </template>

      <el-form label-width="140px" style="max-width: 600px">
        <el-divider content-position="left">基本设置</el-divider>

        <el-form-item label="主题模式">
          <el-radio-group v-model="themeStore.themeMode">
            <el-radio value="light">浅色</el-radio>
            <el-radio value="dark">深色</el-radio>
            <el-radio value="auto">跟随系统</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-divider content-position="left">采集设置</el-divider>

        <el-form-item label="闲置判定阈值">
          <el-input-number
            v-model="settingsStore.settings.idle_threshold"
            :min="60"
            :max="3600"
            :step="60"
          />
          <span class="form-tip">秒</span>
        </el-form-item>

        <el-form-item label="数据同步间隔">
          <el-input-number
            v-model="settingsStore.settings.sync_interval"
            :min="10"
            :max="3600"
            :step="10"
          />
          <span class="form-tip">秒</span>
        </el-form-item>

        <el-divider content-position="left">数据设置</el-divider>

        <el-form-item label="数据保留天数">
          <el-input-number
            v-model="settingsStore.settings.data_retention_days"
            :min="30"
            :max="3650"
            :step="30"
          />
          <span class="form-tip">天</span>
        </el-form-item>

        <el-form-item label="自动清理">
          <el-switch v-model="settingsStore.settings.auto_cleanup" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSave">保存设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.settings-page {
  padding: 0;
}

.form-tip {
  margin-left: 8px;
  color: #909399;
}
</style>
