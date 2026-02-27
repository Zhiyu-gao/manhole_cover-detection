<template>
  <div class="well-page">
    <div class="workspace">
      <el-card class="editor-card">
        <template #header>
          <div class="card-header">井盖数据标注</div>
        </template>

        <el-steps :active="currentStep - 1" finish-status="success" simple>
          <el-step title="隐患类型" />
          <el-step title="BBox 标注" />
          <el-step title="提交" />
        </el-steps>

        <div class="editor-content">
          <div class="preview-panel">
            <img
              v-if="selectedImageUrl"
              :src="selectedImageUrl"
              alt="井盖图片"
              class="well-image"
              ref="annotationImage"
              @mousedown="startDrawing"
              @mousemove="drawBbox"
              @mouseup="stopDrawing"
              @mouseleave="stopDrawing"
            />
            <div v-else class="placeholder">请先在下方表格中选择一条数据</div>
            <div
              v-if="bboxCoordinates"
              class="bbox"
              :style="{
                left: `${bboxCoordinates.x1}px`,
                top: `${bboxCoordinates.y1}px`,
                width: `${bboxCoordinates.width}px`,
                height: `${bboxCoordinates.height}px`
              }"
            />
          </div>

          <div class="form-panel">
            <el-form label-position="top">
              <el-form-item label="隐患类型">
                <el-radio-group v-model="selectedCategory">
                  <el-radio v-for="(name, code) in CATEGORY_TEXT_MAP" :key="code" :label="code">
                    {{ name }}
                  </el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="BBox (x1,y1,x2,y2)">
                <el-input :value="bboxText" readonly />
              </el-form-item>

              <el-form-item>
                <div class="button-group">
                  <el-button @click="goToStep(1)">步骤1</el-button>
                  <el-button @click="goToStep(2)">步骤2</el-button>
                  <el-button @click="goToStep(3)">步骤3</el-button>
                </div>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" :loading="isSubmitting" @click="submitAnnotation" :disabled="!canSubmit">
                  提交标注
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-card>

      <el-card>
        <el-table :data="tableData" stripe @row-click="handleRowClick" :row-class-name="tableRowClassName">
          <el-table-column prop="id" label="ID" width="100" />
          <el-table-column label="图像" width="150">
            <template #default="scope">
              <img :src="scope.row.wellurl" class="thumb" alt="well" />
            </template>
          </el-table-column>
          <el-table-column prop="bbox" label="边界框" />
          <el-table-column label="分类" width="140">
            <template #default="scope">
              <el-tag :type="getCategoryTagType(scope.row.category)">
                {{ getCategoryText(scope.row.category) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-row">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="total"
            :page-size="pageSize"
            :current-page="page"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import { CATEGORY_TEXT_MAP, getCategoryTagType, getCategoryText } from '../constants/categories'

const axios = inject('axios')
const router = useRouter()

const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const tableData = ref([])
const selectedRow = ref(null)

const currentStep = ref(1)
const selectedImageUrl = ref('')
const selectedCategory = ref('')
const bboxCoordinates = ref(null)
const bboxForm = ref({ x1: 0, y1: 0, x2: 0, y2: 0 })

const annotationImage = ref(null)
const isDrawing = ref(false)
const startPoint = ref(null)
const isSubmitting = ref(false)

const bboxText = computed(() => {
  const { x1, y1, x2, y2 } = bboxForm.value
  return `${x1},${y1},${x2},${y2}`
})

const canSubmit = computed(() => {
  return Boolean(selectedRow.value && selectedCategory.value && bboxCoordinates.value)
})

const ensureLogin = () => {
  const token = sessionStorage.getItem('token')
  if (!token) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return false
  }
  return true
}

const loadTableData = async () => {
  if (!ensureLogin()) {
    return
  }

  try {
    const response = await axios.get('/well/wellApi', {
      params: {
        page: page.value,
        page_size: pageSize.value
      }
    })
    tableData.value = response.data.wellData || []
    total.value = response.data.total || 0
  } catch (error) {
    ElMessage.error('加载井盖数据失败，请重试')
  }
}

onMounted(loadTableData)

const handlePageChange = async (nextPage) => {
  page.value = nextPage
  await loadTableData()
}

const goToStep = (step) => {
  currentStep.value = step
}

const handleRowClick = (row) => {
  selectedRow.value = row
  selectedImageUrl.value = row.wellurl
  selectedCategory.value = row.category || ''

  if (row.bbox) {
    const [x1, y1, x2, y2] = row.bbox.split(',').map(Number)
    bboxCoordinates.value = {
      x1,
      y1,
      width: Math.max(x2 - x1, 0),
      height: Math.max(y2 - y1, 0)
    }
    bboxForm.value = { x1, y1, x2, y2 }
  } else {
    bboxCoordinates.value = null
    bboxForm.value = { x1: 0, y1: 0, x2: 0, y2: 0 }
  }

  currentStep.value = 1
}

const tableRowClassName = ({ row }) => (row === selectedRow.value ? 'selected-row' : '')

const startDrawing = (event) => {
  if (!annotationImage.value || !selectedImageUrl.value) {
    return
  }
  const rect = annotationImage.value.getBoundingClientRect()
  startPoint.value = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }
  isDrawing.value = true
}

const drawBbox = (event) => {
  if (!isDrawing.value || !startPoint.value || !annotationImage.value) {
    return
  }
  const rect = annotationImage.value.getBoundingClientRect()
  const currentX = event.clientX - rect.left
  const currentY = event.clientY - rect.top

  const x1 = Math.min(startPoint.value.x, currentX)
  const y1 = Math.min(startPoint.value.y, currentY)
  const x2 = Math.max(startPoint.value.x, currentX)
  const y2 = Math.max(startPoint.value.y, currentY)

  bboxCoordinates.value = { x1, y1, width: x2 - x1, height: y2 - y1 }
  bboxForm.value = {
    x1: Math.round(x1),
    y1: Math.round(y1),
    x2: Math.round(x2),
    y2: Math.round(y2)
  }
}

const stopDrawing = () => {
  isDrawing.value = false
}

const submitAnnotation = async () => {
  if (!canSubmit.value) {
    ElMessage.warning('请选择数据、类别并完成 BBox 标注')
    return
  }

  isSubmitting.value = true
  try {
    await axios.put('/well/updateAnnotation', {
      id: selectedRow.value.id,
      category: selectedCategory.value,
      bbox: bboxText.value,
      user: '当前用户'
    })

    ElMessage.success('标注信息已更新')
    await loadTableData()
    currentStep.value = 1
  } catch (error) {
    ElMessage.error('更新失败，请重试')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.well-page {
  padding: 20px;
}

.workspace {
  display: grid;
  gap: 16px;
}

.card-header {
  font-weight: 600;
}

.editor-content {
  display: flex;
  gap: 20px;
  margin-top: 12px;
}

.preview-panel {
  flex: 1;
  min-height: 360px;
  border: 1px dashed #dcdfe6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: #fafafa;
}

.placeholder {
  color: #909399;
}

.well-image {
  max-width: 100%;
  max-height: 360px;
  object-fit: contain;
  cursor: crosshair;
}

.bbox {
  position: absolute;
  border: 2px solid #f56c6c;
  pointer-events: none;
}

.form-panel {
  width: 360px;
}

.button-group {
  display: flex;
  gap: 8px;
}

.thumb {
  height: 50px;
}

.pagination-row {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

:deep(.selected-row > td) {
  background-color: #ecf5ff !important;
}
</style>
