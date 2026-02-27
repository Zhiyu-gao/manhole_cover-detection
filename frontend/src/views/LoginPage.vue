<template>
  <div class="login-page">
    <el-card class="login-card">
      <h1>系统登录</h1>
      <el-input v-model.trim="username" placeholder="账号" class="form-item" />
      <el-input
        v-model="password"
        type="password"
        placeholder="密码"
        show-password
        class="form-item"
        @keyup.enter="handleLogin"
      />
      <el-button type="primary" :loading="isLoading" class="submit-btn" @click="handleLogin">
        登录
      </el-button>
      <p class="error-text" v-if="errorMessage">{{ errorMessage }}</p>
    </el-card>
  </div>
</template>

<script setup>
import { inject, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const axios = inject('axios')
const router = useRouter()

const username = ref('admin')
const password = ref('123456')
const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = '请输入账号和密码'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await axios.post('/User/jwtLogin', {
      username: username.value,
      password: password.value
    })
    sessionStorage.setItem('token', response.data.token)
    ElMessage.success('登录成功')
    router.push('/monitor')
  } catch (error) {
    errorMessage.value = '账号或密码错误'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
}

.login-card {
  width: 420px;
}

.form-item {
  margin: 12px 0;
}

.submit-btn {
  width: 100%;
  margin-top: 10px;
}

.error-text {
  color: #f56c6c;
  margin-top: 10px;
}
</style>
