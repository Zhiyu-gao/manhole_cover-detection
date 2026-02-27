import { createRouter, createWebHistory } from 'vue-router'

import DataLabel from '../views/DataLabel.vue'
import FileUpload from '../views/FileUpload.vue'
import LoginPage from '../views/LoginPage.vue'
import PredictHistory from '../views/PredictHistory.vue'
import WarningList from '../views/WarningList.vue'
import WellList from '../views/WellList.vue'

const routes = [
  { path: '/login', name: 'LoginPage', component: LoginPage },
  { path: '/well-list', name: 'WellList', component: WellList, meta: { requiresAuth: true } },
  { path: '/upload', name: 'FileUpload', component: FileUpload, meta: { requiresAuth: true } },
  { path: '/monitor', name: 'WarningList', component: WarningList, meta: { requiresAuth: true } },
  { path: '/history', name: 'PredictHistory', component: PredictHistory, meta: { requiresAuth: true } },
  { path: '/label', name: 'DataLabel', component: DataLabel, meta: { requiresAuth: true } },
  { path: '/', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }
  if (to.path === '/login' && token) {
    next('/monitor')
    return
  }
  next()
})

export default router
