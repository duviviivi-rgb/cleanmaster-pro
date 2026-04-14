<template>
  <div class="home-container">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <span>欢迎使用检验批容量与隐蔽工程报告生成系统</span>
        </div>
      </template>
      <div class="welcome-content">
        <p>本系统用于解析图纸文件，提取材料信息，生成检验批容量和隐蔽工程报告。</p>
        <p>主要功能包括：</p>
        <el-list>
          <el-list-item>
            <span>文件上传与解析</span>
          </el-list-item>
          <el-list-item>
            <span>材料信息提取与编辑</span>
          </el-list-item>
          <el-list-item>
            <span>报告预览与导出</span>
          </el-list-item>
          <el-list-item>
            <span>系统配置管理</span>
          </el-list-item>
          <el-list-item>
            <span>历史记录查询</span>
          </el-list-item>
        </el-list>
        <div class="action-buttons">
          <el-button type="primary" @click="goToFileProcess">
            开始上传文件
          </el-button>
        </div>
      </div>
    </el-card>
    
    <el-card class="recent-records">
      <template #header>
        <div class="card-header">
          <span>最近处理记录</span>
        </div>
      </template>
      <el-table :data="recentRecords" style="width: 100%">
        <el-table-column prop="processed_at" label="处理时间" width="180" />
        <el-table-column prop="file_paths" label="文件" />
        <el-table-column prop="materials_count" label="材料数量" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
              {{ scope.row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewReport(scope.row.id)">
              查看报告
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const recentRecords = ref([
  {
    id: 1,
    file_paths: ['水施-03.dwg', '电施-05.dxf'],
    processed_at: '2026-04-14 10:00:00',
    materials_count: 40,
    status: 'success'
  },
  {
    id: 2,
    file_paths: ['风施-02.dwg'],
    processed_at: '2026-04-14 09:30:00',
    materials_count: 25,
    status: 'success'
  },
  {
    id: 3,
    file_paths: ['医气-01.dwg'],
    processed_at: '2026-04-14 09:00:00',
    materials_count: 15,
    status: 'error'
  }
])

const goToFileProcess = () => {
  router.push('/file-process')
}

const viewReport = (id: number) => {
  router.push(`/report-preview?id=${id}`)
}

onMounted(() => {
  // 实际应用中，这里会从后端获取最近处理记录
  console.log('HomeView mounted')
})
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.welcome-card {
  max-width: 800px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-content {
  padding: 20px 0;
}

.welcome-content p {
  margin-bottom: 16px;
  line-height: 1.5;
}

.el-list {
  margin: 20px 0;
}

.el-list-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
}

.action-buttons {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.recent-records {
  margin-top: 20px;
}

.el-table {
  margin-top: 20px;
}
</style>
