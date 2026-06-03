<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getGameDetail, createGame, updateGame } from '@/api/games'

const route = useRoute()
const router = useRouter()
const gameId = route.params.id as string | undefined
const isEdit = !!gameId
const loading = ref(false)

const form = ref({
  name: '',
  developer: '',
  publisher: '',
  platform: '',
  rating: null as number | null,
  notes: '',
})

onMounted(async () => {
  if (isEdit) {
    loading.value = true
    try {
      const res = await getGameDetail(Number(gameId))
      if (res) {
        form.value = { ...res }
      }
    } catch (e) {
      console.error('加载游戏信息失败', e)
    } finally {
      loading.value = false
    }
  }
})

async function handleSave() {
  if (!form.value.name.trim()) {
    return
  }

  loading.value = true
  try {
    if (isEdit) {
      await updateGame(Number(gameId), form.value)
    } else {
      await createGame(form.value)
    }
    router.push('/games')
  } catch (e) {
    console.error('保存失败', e)
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  router.push('/games')
}
</script>

<template>
  <div class="game-edit">
    <el-card>
      <template #header>
        <span>{{ isEdit ? '编辑游戏' : '添加游戏' }}</span>
      </template>
      <el-form :model="form" label-width="100px" @submit.prevent="handleSave">
        <el-form-item label="游戏名称" required>
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
          <el-button type="primary" :loading="loading" @click="handleSave">
            保存
          </el-button>
          <el-button @click="handleCancel">取消</el-button>
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
