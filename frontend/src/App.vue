<template>
  <div id="app">
    <el-menu
      v-if="showNavigation"
      :default-active="$route.path"
      mode="horizontal"
      class="main-menu"
      @select="handleMenuSelect"
    >
      <el-menu-item index="/well-list">井盖训练数据管理</el-menu-item>
      <el-menu-item index="/upload">井盖隐患预测</el-menu-item>
      <el-menu-item index="/monitor">井盖预警管理</el-menu-item>
      <el-menu-item index="/history">井盖预测历史</el-menu-item>
      <el-menu-item index="/label">井盖数据标注</el-menu-item>
      <el-menu-item index="__logout__" class="logout-item">退出登录</el-menu-item>
    </el-menu>

    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const showNavigation = computed(() => route.path !== '/login')

const handleMenuSelect = (routePath) => {
  if (routePath === '__logout__') {
    logout()
    return
  }
  router.push(routePath)
}

const logout = () => {
  sessionStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.main-menu {
  margin-bottom: 20px;
}

.logout-item {
  margin-left: auto;
}
</style>
