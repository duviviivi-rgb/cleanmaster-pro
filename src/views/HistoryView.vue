<template>
  <div class="history-container">
    <el-card class="filter-card">
      <template #header>
        <div class="card-header">
          <span>历史记录筛选</span>
        </div>
      </template>
      <div class="filter-form">
        <el-form :inline="true" :model="filterForm" class="demo-form-inline">
          <el-form-item label="开始日期">
            <el-date-picker
              v-model="filterForm.startDate"
              type="date"
              placeholder="选择开始日期"
              style="width: 150px"
            />
          </el-form-item>
          <el-form-item label="结束日期">
            <el-date-picker
              v-model="filterForm.endDate"
              type="date"
              placeholder="选择结束日期"
              style="width: 150px"
            />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filterForm.status" placeholder="选择状态">
              <el-option label="全部" value="" />
              <el-option label="成功" value="success" />
              <el-option label="失败" value="error" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="applyFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    
    <el-card class="history-list-card">
      <template #header>
        <div class="card-header">
          <span>历史记录</span>
          <el-button type="danger" @click="deleteAllHistory" :disabled="filteredHistory.length === 0">
            清空历史
          </el-button>
        </div>
      </template>
      <div class="history-list">
        <el-table :data="filteredHistory" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="processed_at" label="处理时间" width="180" />
          <el-table-column prop="file_paths" label="文件">
            <template #default="scope">
              <el-tag v-for="(file, index) in scope.row.file_paths" :key="index" size="small" style="margin-right: 5px; margin-bottom: 5px;">
                {{ file }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="materials_count" label="材料数量" width="100" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
                {{ scope.row.status === 'success' ? '成功' : '失败' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button type="primary" size="small" @click="viewReport(scope.row.id)">
                查看报告
              </el-button>
              <el-button type="warning" size="small" @click="reprocess(scope.row.id)">
                重新处理
              </el-button>
              <el-button type="danger" size="small" @click="deleteHistory(scope.row.id)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="filteredHistory.length"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const filterForm = ref({
  startDate: null as any,
  endDate: null as any,
  status: ''
})

const currentPage = ref(1)
const pageSize = ref(20)

// 模拟历史记录数据
const mockHistory = [
  {
    id: 1,
    file_paths: ['水施-03.dwg', '电施-05.dxf'],
    processed_at: '2026-04-14 10:00:00',
    materials_count: 40,
    report_path: 'path/to/report1.html',
    status: 'success'
  },
  {
    id: 2,
    file_paths: ['风施-02.dwg'],
    processed_at: '2026-04-14 09:30:00',
    materials_count: 25,
    report_path: 'path/to/report2.html',
    status: 'success'
  },
  {
    id: 3,
    file_paths: ['医气-01.dwg'],
    processed_at: '2026-04-14 09:00:00',
    materials_count: 15,
    report_path: 'path/to/report3.html',
    status: 'error'
  },
  {
    id: 4,
    file_paths: ['建施-01.dwg', '结施-02.dwg'],
    processed_at: '2026-04-13 16:00:00',
    materials_count: 30,
    report_path: 'path/to/report4.html',
    status: 'success'
  },
  {
    id: 5,
    file_paths: ['电施-01.dwg', '电施-02.dwg', '电施-03.dwg'],
    processed_at: '2026-04-13 14:00:00',
    materials_count: 50,
    report_path: 'path/to/report5.html',
    status: 'success'
  }
]

const history = ref(mockHistory)

const filteredHistory = computed(() => {
  let result = [...history.value]
  
  if (filterForm.value.startDate) {
    const startDate = new Date(filterForm.value.startDate)
    result = result.filter(item => {
      const itemDate = new Date(item.processed_at)
      return itemDate >= startDate
    })
  }
  
  if (filterForm.value.endDate) {
    const endDate = new Date(filterForm.value.endDate)
    endDate.setHours(23, 59, 59, 999)
    result = result.filter(item => {
      const itemDate = new Date(item.processed_at)
      return itemDate <= endDate
    })
  }
  
  if (filterForm.value.status) {
    result = result.filter(item => item.status === filterForm.value.status)
  }
  
  return result
})

const applyFilter = () => {
  // 筛选逻辑已在computed中实现
}

const resetFilter = () => {
  filterForm.value = {
    startDate: null,
    endDate: null,
    status: ''
  }
}

const viewReport = (id: number) => {
  router.push(`/report-preview?id=${id}`)
}

const reprocess = (id: number) => {
  // 实际应用中，这里会重新处理历史文件
  ElMessage.success('重新处理功能开发中...')
}

const deleteHistory = (id: number) => {
  history.value = history.value.filter(item => item.id !== id)
  ElMessage.success('历史记录删除成功')
}

const deleteAllHistory = () => {
  history.value = []
  ElMessage.success('历史记录清空成功')
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

onMounted(() => {
  // 实际应用中，这里会从后端获取历史记录数据
  console.log('HistoryView mounted')
})
</script>

<style scoped>
.history-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filter-card {
  max-width: 1200px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-form {
  margin-top: 20px;
}

.history-list-card {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
