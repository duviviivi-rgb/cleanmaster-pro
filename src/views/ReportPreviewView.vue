<template>
  <div class="report-preview-container">
    <el-card class="report-header-card">
      <template #header>
        <div class="card-header">
          <span>报告预览</span>
          <div class="report-actions">
            <el-select v-model="reportFormat" placeholder="选择格式" style="width: 120px; margin-right: 10px;">
              <el-option label="HTML" value="html" />
              <el-option label="Markdown" value="markdown" />
              <el-option label="Excel" value="excel" />
            </el-select>
            <el-button type="primary" @click="exportReport">
              导出报告
            </el-button>
          </div>
        </div>
      </template>
      <div class="report-info">
        <el-form :inline="true" :model="reportInfo" class="demo-form-inline">
          <el-form-item label="项目名称">
            <el-input v-model="reportInfo.projectName" placeholder="输入项目名称" />
          </el-form-item>
          <el-form-item label="生成时间">
            <el-date-picker
              v-model="reportInfo.generatedAt"
              type="datetime"
              placeholder="选择日期时间"
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="generateReport">
              重新生成报告
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    
    <el-card class="report-content-card">
      <template #header>
        <div class="card-header">
          <span>报告内容</span>
        </div>
      </template>
      <div class="report-content">
        <div v-if="reportFormat === 'html'" class="html-preview">
          <div v-html="htmlReportContent"></div>
        </div>
        <div v-else-if="reportFormat === 'markdown'" class="markdown-preview">
          <pre>{{ markdownReportContent }}</pre>
        </div>
        <div v-else-if="reportFormat === 'excel'" class="excel-preview">
          <el-alert
            title="Excel格式预览"
            type="info"
            description="Excel格式报告将在导出后查看"
            show-icon
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMaterialStore } from '../store/material'

const materialStore = useMaterialStore()

const reportFormat = ref('html')
const reportInfo = ref({
  projectName: '东方肝胆医院医疗净化工程',
  generatedAt: new Date()
})

const materials = computed(() => materialStore.materials)

// 生成HTML报告内容
const htmlReportContent = computed(() => {
  let content = `
    <h1 style="text-align: center; margin-bottom: 30px;">检验批容量与隐蔽工程报告</h1>
    <div style="margin-bottom: 20px;">
      <p><strong>项目名称：</strong>${reportInfo.value.projectName}</p>
      <p><strong>生成时间：</strong>${reportInfo.value.generatedAt.toLocaleString()}</p>
      <p><strong>材料总数：</strong>${materials.value.length}</p>
    </div>
    <h2 style="margin-top: 30px; margin-bottom: 20px;">材料清单</h2>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
      <thead>
        <tr style="background-color: #f5f7fa;">
          <th style="border: 1px solid #ddd; padding: 8px;">图纸号</th>
          <th style="border: 1px solid #ddd; padding: 8px;">图纸名称</th>
          <th style="border: 1px solid #ddd; padding: 8px;">楼层</th>
          <th style="border: 1px solid #ddd; padding: 8px;">材料名称</th>
          <th style="border: 1px solid #ddd; padding: 8px;">型号</th>
          <th style="border: 1px solid #ddd; padding: 8px;">数量</th>
          <th style="border: 1px solid #ddd; padding: 8px;">单位</th>
          <th style="border: 1px solid #ddd; padding: 8px;">分类</th>
          <th style="border: 1px solid #ddd; padding: 8px;">检验批</th>
          <th style="border: 1px solid #ddd; padding: 8px;">标准</th>
        </tr>
      </thead>
      <tbody>
  `
  
  materials.value.forEach(material => {
    content += `
      <tr>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.drawing_number}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.drawing_name}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.floor}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.name}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.model}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.quantity}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.unit}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.category}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.inspection_batch}</td>
        <td style="border: 1px solid #ddd; padding: 8px;">${material.standard}</td>
      </tr>
    `
  })
  
  content += `
      </tbody>
    </table>
    <h2 style="margin-top: 30px; margin-bottom: 20px;">隐蔽工程检查内容</h2>
    <p>根据提取的材料信息，以下是隐蔽工程检查内容：</p>
    <ul style="margin-left: 20px;">
      <li>管道安装：检查管道材质、规格、连接方式是否符合设计要求</li>
      <li>电气线路：检查线路敷设、接地装置是否符合规范</li>
      <li>通风空调：检查风管安装、保温措施是否到位</li>
      <li>医疗气体：检查气体管道安装、压力测试是否合格</li>
    </ul>
  `
  
  return content
})

// 生成Markdown报告内容
const markdownReportContent = computed(() => {
  let content = `# 检验批容量与隐蔽工程报告

## 项目信息
- **项目名称：** ${reportInfo.value.projectName}
- **生成时间：** ${reportInfo.value.generatedAt.toLocaleString()}
- **材料总数：** ${materials.value.length}

## 材料清单

| 图纸号 | 图纸名称 | 楼层 | 材料名称 | 型号 | 数量 | 单位 | 分类 | 检验批 | 标准 |
|--------|----------|------|----------|------|------|------|------|--------|------|
`
  
  materials.value.forEach(material => {
    content += `| ${material.drawing_number} | ${material.drawing_name} | ${material.floor} | ${material.name} | ${material.model} | ${material.quantity} | ${material.unit} | ${material.category} | ${material.inspection_batch} | ${material.standard} |
`
  })
  
  content += `
## 隐蔽工程检查内容

根据提取的材料信息，以下是隐蔽工程检查内容：

- 管道安装：检查管道材质、规格、连接方式是否符合设计要求
- 电气线路：检查线路敷设、接地装置是否符合规范
- 通风空调：检查风管安装、保温措施是否到位
- 医疗气体：检查气体管道安装、压力测试是否合格
`
  
  return content
})

const generateReport = () => {
  ElMessage.success('报告重新生成成功')
}

const exportReport = () => {
  if (reportFormat.value === 'html') {
    // 导出HTML报告
    const blob = new Blob([htmlReportContent.value], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `report_${Date.now()}.html`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } else if (reportFormat.value === 'markdown') {
    // 导出Markdown报告
    const blob = new Blob([markdownReportContent.value], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `report_${Date.now()}.md`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } else if (reportFormat.value === 'excel') {
    // 导出Excel报告（模拟）
    ElMessage.success('Excel报告导出功能开发中...')
  }
  
  ElMessage.success('报告导出成功')
}

onMounted(() => {
  // 实际应用中，这里会从后端获取报告数据
  console.log('ReportPreviewView mounted')
})
</script>

<style scoped>
.report-preview-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.report-header-card {
  max-width: 1200px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.report-actions {
  display: flex;
  align-items: center;
}

.report-info {
  margin-top: 20px;
}

.report-content-card {
  margin-top: 20px;
}

.report-content {
  min-height: 600px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.html-preview {
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

.markdown-preview {
  font-family: 'Courier New', monospace;
  white-space: pre-wrap;
  line-height: 1.5;
}

.excel-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}
</style>
