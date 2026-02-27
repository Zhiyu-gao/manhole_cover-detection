<template>
  <div class="warning-container">
    <div class="left-panel" v-if="selectedRow">
      <div class="image-container">
        <img
          :src="`/static/${selectedRow.img}.jpg`"
          alt="井盖图像"
          class="cover-img"
          @error="handleImgError"
        />
      </div>
      <div class="hidden-type">
        <p>隐患类型：{{ getCategoryText(toCategoryKey(selectedRow.category)) }}</p>
        <p>ID：{{ selectedRow.id }}</p>
        <p>时间：{{ selectedRow.time }}</p>
        <p>点位：{{ selectedRow.position }}</p>
      </div>
    </div>

    <div class="left-panel empty-state" v-else>
      <p>请从右侧表格选择一条记录查看详情</p>
    </div>

    <el-table
      :data="tableData"
      border
      stripe
      class="table-container"
      @row-click="handleRowClick"
    >
      <el-table-column prop="id" label="ID" width="120" />
      <el-table-column prop="time" label="时间" width="180" />
      <el-table-column prop="position" label="点位" />
      <el-table-column label="类别" width="150">
        <template #default="scope">
          {{ getCategoryText(toCategoryKey(scope.row.category)) }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { inject, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'

import { getCategoryText } from '../constants/categories'

const axios = inject('axios')
const tableData = ref([])
const selectedRow = ref(null)

const toCategoryKey = (value) => {
  if (typeof value !== 'string') {
    return ''
  }
  return value.startsWith('[') ? value : `[${value}]`
}

const loadTableData = async () => {
  try {
    const response = await axios.get('/well/monitor/')
    tableData.value = response.data
  } catch (error) {
    ElMessage.error('数据加载失败，请重试')
  }
}

onMounted(loadTableData)

const handleRowClick = (row) => {
  selectedRow.value = row
}

const handleImgError = (event) => {
  event.target.src = '/static/default-cover.jpg'
  ElMessage.warning('图片加载失败')
}
</script>

<style scoped>
.warning-container {
  display: flex;
  padding: 20px;
  gap: 20px;
  min-height: calc(100vh - 40px);
  box-sizing: border-box;
}

.left-panel {
  width: 40%;
  padding: 15px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.image-container {
  width: 100%;
  max-width: 400px;
  max-height: 300px;
  margin: 0 auto 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-img {
  width: 100%;
  height: auto;
  max-height: 300px;
  border-radius: 6px;
  border: 1px solid #f0f0f0;
  object-fit: contain;
}

.hidden-type {
  font-size: 16px;
  color: #333;
  padding: 10px;
  background: #fafafa;
  border-radius: 6px;
  line-height: 1.8;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 350px;
  color: #999;
  border: 1px dashed #e0e0e0;
}

.table-container {
  width: 60%;
}
</style>
