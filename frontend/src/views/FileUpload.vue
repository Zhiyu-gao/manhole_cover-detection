<template>
  <div class="upload-page">
    <el-upload
      ref="uploadRef"
      class="upload-demo"
      name="upload_file"
      :auto-upload="false"
      list-type="picture"
      :http-request="customUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
    >
      <template #trigger>
        <el-button type="primary">选择图片</el-button>
      </template>
      <el-button type="success" class="upload-btn" @click="submitUpload">上传并检测</el-button>
    </el-upload>

    <div v-if="imageUrl" class="result-card">
      <h3>检测结果</h3>
      <img :src="imageUrl" alt="检测图片" class="preview-image" />
      <p>状态：{{ labelText }}</p>
    </div>
  </div>
</template>

<script setup>
import { inject, ref } from 'vue'
import { ElMessage } from 'element-plus'

import { getCategoryText } from '../constants/categories'

const axios = inject('axios')
const uploadRef = ref(null)
const imageUrl = ref('')
const labelText = ref('')

const submitUpload = () => {
  uploadRef.value?.submit()
}

const customUpload = async (uploadRequest) => {
  const formData = new FormData()
  formData.append('upload_file', uploadRequest.file)

  const response = await axios.post('/well/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

  uploadRequest.onSuccess(response.data)
}

const handleSuccess = (response) => {
  imageUrl.value = response.path
  labelText.value = getCategoryText(response.label)
  ElMessage.success('检测完成')
}

const handleError = () => {
  ElMessage.error('上传或检测失败，请重试')
}
</script>

<style scoped>
.upload-page {
  padding: 20px;
}

.upload-btn {
  margin-left: 10px;
}

.result-card {
  margin-top: 20px;
}

.preview-image {
  max-height: 300px;
}
</style>
