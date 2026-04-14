<template>
  <div class="file-process-container">
    <el-card class="upload-card">
      <template #header>
        <div class="card-header">
          <span>文件上传</span>
          <el-button type="primary" @click="parseFiles" :loading="isParsing">
            解析文件
          </el-button>
        </div>
      </template>
      <div class="upload-area">
        <el-upload
          class="upload-demo"
          drag
          action=""
          :auto-upload="false"
          :on-change="handleFileChange"
          :file-list="fileList"
          :limit="10"
          :accept=".dwg,.dxf,.pdf"
        >
          <div class="el-upload__text">
            将文件拖到此处，或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持上传 DWG、DXF、PDF 格式的文件
            </div>
          </template>
        </el-upload>
      </div>
    </el-card>
    
    <el-card class="file-list-card">
      <template #header>
        <div class="card-header">
          <span>文件列表</span>
          <el-button type="danger" @click="clearFiles" :disabled="fileList.length === 0">
            清空列表
          </el-button>
        </div>
      </template>
      <el-table :data="fileList" style="width: 100%">
        <el-table-column prop="name" label="文件名" />
        <el-table-column prop="size" label="大小" width="100">
          <template #default="scope">
            {{ formatFileSize(scope.row.size) }}
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="100" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="progress" label="进度" width="150">
          <template #default="scope">
            <el-progress 
              v-if="scope.row.status === 'processing'" 
              :percentage="scope.row.progress" 
              :stroke-width="10"
            />
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="previewFile(scope.row)" :disabled="scope.row.status !== 'success'">
              预览
            </el-button>
            <el-button type="danger" size="small" @click="removeFile(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog
      v-model="previewDialogVisible"
      title="图纸预览"
      width="80%"
      height="80%"
    >
      <div class="preview-content">
        <div v-if="currentPreviewFile" class="file-preview">
          <h3>{{ currentPreviewFile.name }}</h3>
          <div class="preview-placeholder">
            <p>图纸预览功能开发中...</p>
            <p>文件信息：</p>
            <ul>
              <li>文件名：{{ currentPreviewFile.name }}</li>
              <li>大小：{{ formatFileSize(currentPreviewFile.size) }}</li>
              <li>类型：{{ currentPreviewFile.type }}</li>
              <li>状态：{{ getStatusText(currentPreviewFile.status) }}</li>
            </ul>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useFileStore, FileItem } from '../store/file'

const router = useRouter()
const fileStore = useFileStore()

const fileList = computed(() => fileStore.files)
const isParsing = ref(false)
const previewDialogVisible = ref(false)
const currentPreviewFile = ref<FileItem | null>(null)

const handleFileChange = (file: any) => {
  const newFile: FileItem = {
    id: Date.now().toString(),
    name: file.name,
    path: file.path || '',
    type: file.name.split('.').pop() || '',
    size: file.size,
    status: 'pending',
    progress: 0
  }
  fileStore.addFile(newFile)
}

const parseFiles = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('请先上传文件')
    return
  }
  
  isParsing.value = true
  
  // 模拟文件解析过程
  for (const file of fileList.value) {
    fileStore.updateFileStatus(file.id, 'processing')
    
    // 模拟进度
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 100))
      fileStore.updateFileProgress(file.id, i)
    }
    
    fileStore.updateFileStatus(file.id, 'success')
  }
  
  isParsing.value = false
  ElMessage.success('文件解析完成')
  
  // 跳转到材料编辑页面
  router.push('/material-edit')
}

const removeFile = (id: string) => {
  fileStore.removeFile(id)
}

const clearFiles = () => {
  fileStore.clearFiles()
}

const previewFile = (file: FileItem) => {
  currentPreviewFile.value = file
  previewDialogVisible.value = true
}

const formatFileSize = (size: number): string => {
  if (size < 1024) {
    return `${size} B`
  } else if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(2)} KB`
  } else {
    return `${(size / (1024 * 1024)).toFixed(2)} MB`
  }
}

const getStatusType = (status: FileItem['status']): string => {
  switch (status) {
    case 'success': return 'success'
    case 'error': return 'danger'
    case 'processing': return 'warning'
    default: return 'info'
  }
}

const getStatusText = (status: FileItem['status']): string => {
  switch (status) {
    case 'pending': return '待处理'
    case 'processing': return '处理中'
    case 'success': return '成功'
    case 'error': return '失败'
    default: return '未知'
  }
}
</script>

<style scoped>
.file-process-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.upload-card {
  max-width: 800px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-area {
  margin-top: 20px;
}

.file-list-card {
  margin-top: 20px;
}

.preview-content {
  height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-preview {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.file-preview h3 {
  margin-bottom: 20px;
}

.preview-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background-color: #f5f7fa;
  border-radius: 8px;
  text-align: center;
}

.placeholder-icon {
  font-size: 48px;
  color: #909399;
  margin-bottom: 20px;
}

.preview-placeholder p {
  margin: 10px 0;
  color: #606266;
}

.preview-placeholder ul {
  text-align: left;
  margin-top: 20px;
  color: #606266;
}

.preview-placeholder li {
  margin: 5px 0;
}
</style>
