<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const gameId = route.params.id
const isEdit = !!gameId

const form = ref({
  name: '',
  developer: '',
  publisher: '',
  platform: '',
  rating: null,
  notes: '',
})
</script>

<template>
  <div class="game-edit">
    <el-card>
      <template #header>
        <span>{{ isEdit ? '编辑游戏' : '添加游戏' }}</span>
      </template>
      <el-form :model="form" label-width="100px">
        <el-form-item label="游戏名称">
          <el-input v-model="form.name" placeholder="请输入游戏名称" />
        </el-form-item>
        <el-form-item label="开发商">
          <el-input v-model="form.developer" placeholder="请输入开发商" />
        </el-form-item>
        <el-form-item label="发行商">
          <el-input v-model="form.publisher" placeholder="请输入发行商" />
        </el-form-item>
        <el-form-item label="平台">
          <el-select v-model="form.platform" placeholder="请选择平台">
            <el-option label="Steam" value="Steam" />
            <el-option label="Epic" value="Epic" />
            <el-option label="PC" value="PC" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="评分">
          <el-rate v-model="form.rating" :max="5" show-score />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.notes" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary">保存</el-button>
          <el-button>取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.game-edit {
  padding: 0;
}
</style>
