import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/file-process',
    name: 'FileProcess',
    component: () => import('../views/FileProcessView.vue')
  },
  {
    path: '/material-edit',
    name: 'MaterialEdit',
    component: () => import('../views/MaterialEditView.vue')
  },
  {
    path: '/report-preview',
    name: 'ReportPreview',
    component: () => import('../views/ReportPreviewView.vue')
  },
  {
    path: '/config',
    name: 'Config',
    component: () => import('../views/ConfigView.vue')
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/HistoryView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
