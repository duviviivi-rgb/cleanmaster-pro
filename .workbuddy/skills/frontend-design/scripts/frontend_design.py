#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

class FrontendDesign:
    def __init__(self):
        self.design_templates = {
            "component": self._generate_component_design,
            "layout": self._generate_layout_design,
            "page": self._generate_page_design,
            "style": self._generate_style_design
        }
    
    def run(self, input_data):
        """运行前端设计技能"""
        try:
            # 解析输入参数
            params = input_data.get('parameters', {})
            design_type = params.get('design_type', 'component')
            framework = params.get('framework', 'vue')
            target_platform = params.get('target_platform', 'desktop')
            requirements = params.get('requirements', '')
            
            # 生成设计方案
            if design_type in self.design_templates:
                design_function = self.design_templates[design_type]
                design_result = design_function(framework, target_platform, requirements)
                
                return {
                    "success": True,
                    "data": {
                        "design_type": design_type,
                        "framework": framework,
                        "target_platform": target_platform,
                        "requirements": requirements,
                        "design_result": design_result
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"不支持的设计类型: {design_type}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_component_design(self, framework, target_platform, requirements):
        """生成组件设计方案"""
        design = {
            "name": "组件设计",
            "framework": framework,
            "target_platform": target_platform,
            "requirements": requirements,
            "structure": "",
            "style": "",
            "interaction": "",
            "code": ""
        }
        
        # 根据需求生成具体的组件设计
        if "文件上传" in requirements:
            design["name"] = "文件上传组件"
            design["structure"] = "包含拖拽区域、文件列表、上传按钮和进度条"
            design["style"] = "使用现代简约风格，支持深色和浅色主题"
            design["interaction"] = "支持拖拽上传、文件预览、批量上传和上传进度显示"
            design["code"] = f"""
<template>
  <div class="file-upload">
    <div class="upload-area" 
         @drop="handleDrop"
         @dragover.prevent
         @dragenter.prevent
         @dragleave.prevent>
      <el-icon class="upload-icon"><UploadFilled /></el-icon>
      <p v-if="!files.length">拖拽文件到此处或 <el-button type="primary" @click="triggerUpload">点击上传</el-button></p>
      <p v-else>已选择 {{ files.length }} 个文件</p>
      <input type="file" ref="fileInput" multiple @change="handleFileSelect" style="display: none" />
    </div>
    <div v-if="files.length" class="file-list">
      <div v-for="(file, index) in files" :key="index" class="file-item">
        <div class="file-info">
          <el-icon><Document /></el-icon>
          <span>{{ file.name }}</span>
          <span class="file-size">{{ formatSize(file.size) }}</span>
        </div>
        <el-progress v-if="uploading" :percentage="50" :format="() => '上传中...'" />
        <el-button type="danger" size="small" @click="removeFile(index)">
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
    </div>
    <div class="upload-actions">
      <el-button type="primary" @click="uploadFiles" :loading="uploading">
        上传文件
      </el-button>
      <el-button @click="clearFiles">
        清空
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UploadFilled, Document, Delete } from '@element-plus/icons-vue'

const fileInput = ref(null)
const files = ref([])
const uploading = ref(false)

const triggerUpload = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  files.value = [...files.value, ...selectedFiles]
}

const handleDrop = (event) => {
  event.preventDefault()
  const droppedFiles = Array.from(event.dataTransfer.files)
  files.value = [...files.value, ...droppedFiles]
}

const removeFile = (index) => {
  files.value.splice(index, 1)
}

const clearFiles = () => {
  files.value = []
}

const uploadFiles = async () => {
  if (files.value.length === 0) return
  
  uploading.value = true
  // 模拟上传过程
  setTimeout(() => {
    uploading.value = false
    ElMessage.success('文件上传成功')
    files.value = []
  }, 2000)
}

const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style scoped>
.file-upload {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  padding: 20px;
  transition: all 0.3s;
}

.file-upload:hover {
  border-color: #409EFF;
}

.upload-area {
  text-align: center;
  padding: 40px 20px;
}

.upload-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 16px;
}

.file-list {
  margin-top: 20px;
  border-top: 1px solid #e8e8e8;
  padding-top: 20px;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  margin-bottom: 10px;
}

.file-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.file-info .el-icon {
  margin-right: 8px;
  color: #409EFF;
}

.file-size {
  margin-left: 16px;
  font-size: 12px;
  color: #999;
}

.upload-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
"""
        
        # 其他组件设计可以根据需求扩展
        
        return design
    
    def _generate_layout_design(self, framework, target_platform, requirements):
        """生成布局设计方案"""
        design = {
            "name": "布局设计",
            "framework": framework,
            "target_platform": target_platform,
            "requirements": requirements,
            "structure": "",
            "components": "",
            "responsive": "",
            "code": ""
        }
        
        # 根据需求生成具体的布局设计
        if "首页" in requirements:
            design["name"] = "首页布局"
            design["structure"] = "顶部导航栏 + 左侧功能菜单 + 主内容区 + 底部状态栏"
            design["components"] = "文件上传组件、最近处理记录列表、功能导航卡片"
            design["responsive"] = "支持桌面端响应式布局，适配不同屏幕尺寸"
            design["code"] = f"""
<template>
  <div class="home-layout">
    <!-- 顶部导航栏 -->
    <el-header height="60px" class="header">
      <div class="logo">
        <h1>检验批容量与隐蔽工程报告生成工具</h1>
      </div>
      <div class="header-actions">
        <el-dropdown>
          <span class="user">
            <el-avatar size="small">U</el-avatar>
            <span>用户</span>
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>设置</el-dropdown-item>
              <el-dropdown-item divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <div class="main-content">
      <!-- 左侧功能菜单 -->
      <el-aside width="200px" class="sidebar">
        <el-menu
          default-active="1"
          class="menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="1">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon><Document /></el-icon>
            <span>文件处理</span>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon><Edit /></el-icon>
            <span>材料编辑</span>
          </el-menu-item>
          <el-menu-item index="4">
            <el-icon><View /></el-icon>
            <span>报告预览</span>
          </el-menu-item>
          <el-menu-item index="5">
            <el-icon><Setting /></el-icon>
            <span>配置</span>
          </el-menu-item>
          <el-menu-item index="6">
            <el-icon><Time /></el-icon>
            <span>历史记录</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-main class="content">
        <div class="welcome-section">
          <h2>欢迎使用检验批容量与隐蔽工程报告生成工具</h2>
          <p>上传图纸文件，自动生成检验批容量和隐蔽工程报告</p>
        </div>
        
        <!-- 文件上传区域 -->
        <div class="upload-section">
          <h3>文件上传</h3>
          <file-upload @upload-success="handleUploadSuccess" />
        </div>
        
        <!-- 最近处理记录 -->
        <div class="history-section">
          <h3>最近处理记录</h3>
          <el-table :data="recentHistory" style="width: 100%">
            <el-table-column prop="file_name" label="文件名" />
            <el-table-column prop="processed_at" label="处理时间" />
            <el-table-column prop="status" label="状态" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" @click="viewReport(scope.row)">查看报告</el-button>
                <el-button size="small" type="primary" @click="reprocess(scope.row)">重新处理</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <!-- 功能导航 -->
        <div class="feature-section">
          <h3>功能导航</h3>
          <div class="feature-cards">
            <el-card class="feature-card" @click="navigateTo('file-processing')">
              <template #header>
                <div class="card-header">
                  <el-icon class="card-icon"><Document /></el-icon>
                  <span>文件处理</span>
                </div>
              </template>
              <p>上传和处理图纸文件</p>
            </el-card>
            <el-card class="feature-card" @click="navigateTo('material-edit')">
              <template #header>
                <div class="card-header">
                  <el-icon class="card-icon"><Edit /></el-icon>
                  <span>材料编辑</span>
                </div>
              </template>
              <p>查看和编辑提取的材料信息</p>
            </el-card>
            <el-card class="feature-card" @click="navigateTo('report-preview')">
              <template #header>
                <div class="card-header">
                  <el-icon class="card-icon"><View /></el-icon>
                  <span>报告预览</span>
                </div>
              </template>
              <p>预览和导出生成的报告</p>
            </el-card>
            <el-card class="feature-card" @click="navigateTo('config')">
              <template #header>
                <div class="card-header">
                  <el-icon class="card-icon"><Setting /></el-icon>
                  <span>配置</span>
                </div>
              </template>
              <p>调整系统设置和偏好</p>
            </el-card>
          </div>
        </div>
      </el-main>
    </div>
    
    <!-- 底部状态栏 -->
    <el-footer height="40px" class="footer">
      <p>© 2026 检验批容量与隐蔽工程报告生成工具</p>
    </el-footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { House, Document, Edit, View, Setting, Time, ArrowDown } from '@element-plus/icons-vue'
import FileUpload from '@/components/FileUpload.vue'

const recentHistory = ref([
  {
    id: 1,
    file_name: '医气给排水-东方肝胆项目医疗专项审图20251229_t3.dxf',
    processed_at: '2026-04-14 10:00:00',
    status: '成功'
  },
  {
    id: 2,
    file_name: '通风空调-东方肝胆项目医疗专项审图20251229_t2.dxf',
    processed_at: '2026-04-13 15:30:00',
    status: '成功'
  },
  {
    id: 3,
    file_name: '电气-东方肝胆项目医疗专项审图20251229_t1.dxf',
    processed_at: '2026-04-12 09:15:00',
    status: '成功'
  }
])

const handleMenuSelect = (key) => {
  console.log('Menu selected:', key)
  // 导航到对应页面
}

const handleUploadSuccess = (files) => {
  console.log('Files uploaded:', files)
  // 处理文件上传成功后的逻辑
}

const viewReport = (row) => {
  console.log('View report:', row)
  // 查看报告
}

const reprocess = (row) => {
  console.log('Reprocess:', row)
  // 重新处理文件
}

const navigateTo = (page) => {
  console.log('Navigate to:', page)
  // 导航到对应页面
}
</script>

<style scoped>
.home-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo h1 {
  font-size: 18px;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
}

.user {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user .el-icon {
  margin-left: 8px;
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.sidebar {
  background-color: #f5f7fa;
  border-right: 1px solid #e8e8e8;
}

.menu {
  height: 100%;
  border-right: none;
}

.content {
  padding: 20px;
  overflow-y: auto;
}

.welcome-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f0f9ff;
  border-radius: 8px;
  border: 1px solid #e1f5fe;
}

.welcome-section h2 {
  margin-top: 0;
  color: #1890ff;
}

.upload-section,
.history-section,
.feature-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.upload-section h3,
.history-section h3,
.feature-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #303133;
  font-size: 16px;
  border-bottom: 1px solid #e8e8e8;
  padding-bottom: 10px;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.feature-card {
  cursor: pointer;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
}

.card-icon {
  font-size: 20px;
  margin-right: 10px;
  color: #409EFF;
}

.footer {
  background-color: #f5f7fa;
  border-top: 1px solid #e8e8e8;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer p {
  margin: 0;
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100% !important;
    height: auto;
    border-right: none;
    border-bottom: 1px solid #e8e8e8;
  }
  
  .menu {
    display: flex;
    overflow-x: auto;
  }
  
  .feature-cards {
    grid-template-columns: 1fr;
  }
}
</style>
"""
        
        # 其他布局设计可以根据需求扩展
        
        return design
    
    def _generate_page_design(self, framework, target_platform, requirements):
        """生成页面设计方案"""
        design = {
            "name": "页面设计",
            "framework": framework,
            "target_platform": target_platform,
            "requirements": requirements,
            "structure": "",
            "modules": "",
            "interaction": "",
            "code": ""
        }
        
        # 根据需求生成具体的页面设计
        if "报告预览" in requirements:
            design["name"] = "报告预览页面"
            design["structure"] = "顶部导航栏 + 格式选择 + 报告内容预览 + 导出按钮"
            design["modules"] = "报告内容展示、格式切换、导出功能"
            design["interaction"] = "支持Markdown、HTML和Excel格式的报告预览和导出"
            design["code"] = f"""
<template>
  <div class="report-preview">
    <!-- 顶部导航栏 -->
    <el-header height="60px" class="header">
      <div class="header-left">
        <el-button @click="goBack" icon="ArrowLeft">返回</el-button>
        <h2>报告预览</h2>
      </div>
      <div class="header-right">
        <el-select v-model="reportFormat" placeholder="选择格式" @change="switchFormat">
          <el-option label="Markdown" value="markdown" />
          <el-option label="HTML" value="html" />
          <el-option label="Excel" value="excel" />
        </el-select>
        <el-button type="primary" @click="exportReport" style="margin-left: 10px">
          <el-icon><Download /></el-icon> 导出报告
        </el-button>
      </div>
    </el-header>
    
    <!-- 主内容区 -->
    <el-main class="content">
      <!-- 报告信息 -->
      <div class="report-info">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card>
              <template #header>
                <div class="card-header">
                  <el-icon><Document /></el-icon>
                  <span>报告信息</span>
                </div>
              </template>
              <el-descriptions :column="1">
                <el-descriptions-item label="项目名称">
                  {{ reportInfo.project_name }}
                </el-descriptions-item>
                <el-descriptions-item label="生成时间">
                  {{ reportInfo.generated_at }}
                </el-descriptions-item>
                <el-descriptions-item label="总材料数">
                  {{ reportInfo.total_materials }}
                </el-descriptions-item>
                <el-descriptions-item label="总检验批数">
                  {{ reportInfo.total_inspection_batches }}
                </el-descriptions-item>
                <el-descriptions-item label="当前格式">
                  {{ formatMap[reportFormat] }}
                </el-descriptions-item>
              </el-descriptions>
            </el-card>
          </el-col>
          <el-col :span="16">
            <el-card>
              <template #header>
                <div class="card-header">
                  <el-icon><Filter /></el-icon>
                  <span>过滤选项</span>
                </div>
              </template>
              <el-form :inline="true" :model="filterForm">
                <el-form-item label="楼层">
                  <el-select v-model="filterForm.floor" placeholder="选择楼层">
                    <el-option label="全部" value="" />
                    <el-option v-for="floor in floors" :key="floor" :label="floor" :value="floor" />
                  </el-select>
                </el-form-item>
                <el-form-item label="分类">
                  <el-select v-model="filterForm.category" placeholder="选择分类">
                    <el-option label="全部" value="" />
                    <el-option v-for="category in categories" :key="category" :label="category" :value="category" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="applyFilter">应用过滤</el-button>
                  <el-button @click="resetFilter">重置</el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 报告内容 -->
      <div class="report-content">
        <el-card style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <el-icon><View /></el-icon>
              <span>报告内容</span>
            </div>
          </template>
          
          <!-- Markdown预览 -->
          <div v-if="reportFormat === 'markdown'" class="markdown-preview">
            <pre>{{ reportContent.markdown }}</pre>
          </div>
          
          <!-- HTML预览 -->
          <div v-else-if="reportFormat === 'html'" class="html-preview" v-html="reportContent.html"></div>
          
          <!-- Excel预览 -->
          <div v-else-if="reportFormat === 'excel'" class="excel-preview">
            <el-table :data="excelData" style="width: 100%">
              <el-table-column prop="name" label="材料名称" />
              <el-table-column prop="model" label="型号" />
              <el-table-column prop="quantity" label="数量" />
              <el-table-column prop="unit" label="单位" />
              <el-table-column prop="floor" label="楼层" />
              <el-table-column prop="drawing_number" label="图纸号" />
              <el-table-column prop="category" label="分类" />
              <el-table-column prop="inspection_batch" label="检验批" />
            </el-table>
          </div>
        </el-card>
      </div>
    </el-main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowLeft, Document, Filter, View, Download } from '@element-plus/icons-vue'

const reportFormat = ref('markdown')
const filterForm = ref({
  floor: '',
  category: ''
})

const formatMap = {
  markdown: 'Markdown',
  html: 'HTML',
  excel: 'Excel'
}

const reportInfo = ref({
  project_name: '东方肝胆医院医疗净化工程',
  generated_at: '2026-04-14 10:00:00',
  total_materials: 40,
  total_inspection_batches: 33
})

const floors = ref(['三层', '四层', '三层夹层'])
const categories = ref(['建筑给排水和水暖', '通风与空调', '建筑电气', '智能建筑', '医疗气体工程'])

const reportContent = ref({
  markdown: '# 检验批容量与隐蔽工程报告\n\n## 项目信息\n- 项目名称：东方肝胆医院医疗净化工程\n- 生成时间：2026-04-14 10:00:00\n\n## 检验批容量\n...',
  html: '<h1>检验批容量与隐蔽工程报告</h1><h2>项目信息</h2><ul><li>项目名称：东方肝胆医院医疗净化工程</li><li>生成时间：2026-04-14 10:00:00</li></ul><h2>检验批容量</h2>...',
  excel: '材料名称,型号,数量,单位,楼层,图纸号,分类,检验批\n304金属钢管,DN50,10,m,三层,水施-03,建筑给排水和水暖,给排水管道安装\n...'
})

const excelData = ref([
  {
    name: '304金属钢管',
    model: 'DN50',
    quantity: 10,
    unit: 'm',
    floor: '三层',
    drawing_number: '水施-03',
    category: '建筑给排水和水暖',
    inspection_batch: '给排水管道安装'
  },
  {
    name: 'PPR管',
    model: 'DN32',
    quantity: 15,
    unit: 'm',
    floor: '四层',
    drawing_number: '水施-04',
    category: '建筑给排水和水暖',
    inspection_batch: '给排水管道安装'
  },
  {
    name: '镀锌钢板风管',
    model: 'DN200',
    quantity: 8,
    unit: 'm',
    floor: '三层夹层',
    drawing_number: '风施-03',
    category: '通风与空调',
    inspection_batch: '风管安装'
  }
])

const goBack = () => {
  console.log('Go back')
  // 返回上一页
}

const switchFormat = (format) => {
  console.log('Switch format to:', format)
  // 切换报告格式
}

const exportReport = () => {
  console.log('Export report in format:', reportFormat.value)
  // 导出报告
  ElMessage.success('报告导出成功')
}

const applyFilter = () => {
  console.log('Apply filter:', filterForm.value)
  // 应用过滤
}

const resetFilter = () => {
  filterForm.value = {
    floor: '',
    category: ''
  }
  console.log('Reset filter')
  // 重置过滤
}
</script>

<style scoped>
.report-preview {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-left h2 {
  font-size: 18px;
  margin: 0;
  margin-left: 10px;
}

.header-right {
  display: flex;
  align-items: center;
}

.content {
  padding: 20px;
  overflow-y: auto;
}

.report-info {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
}

.card-header .el-icon {
  margin-right: 8px;
  color: #409EFF;
}

.report-content {
  margin-top: 20px;
}

.markdown-preview {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
  white-space: pre-wrap;
  font-family: 'Courier New', Courier, monospace;
}

.html-preview {
  padding: 20px;
  background-color: white;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
}

.excel-preview {
  padding: 20px;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    height: auto;
    padding: 10px;
  }
  
  .header-left,
  .header-right {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  .content {
    padding: 10px;
  }
}
</style>
"""
        
        # 其他页面设计可以根据需求扩展
        
        return design
    
    def _generate_style_design(self, framework, target_platform, requirements):
        """生成样式设计方案"""
        design = {
            "name": "样式设计",
            "framework": framework,
            "target_platform": target_platform,
            "requirements": requirements,
            "colors": "",
            "typography": "",
            "components": "",
            "code": ""
        }
        
        # 生成样式设计方案
        design["name"] = "统一样式系统"
        design["colors"] = "主色调：#409EFF，辅助色：#67C23A，警告色：#E6A23C，危险色：#F56C6C，信息色：#909399"
        design["typography"] = "字体：Microsoft YaHei, sans-serif；标题字体大小：18px，16px，14px；正文字体大小：14px，12px"
        design["components"] = "按钮、表单、卡片、表格、对话框等组件的统一样式"
        design["code"] = f"""
/* 全局样式 */
:root {
  /* 颜色 */
  --primary-color: #409EFF;
  --success-color: #67C23A;
  --warning-color: #E6A23C;
  --danger-color: #F56C6C;
  --info-color: #909399;
  
  /* 背景色 */
  --bg-color: #f5f7fa;
  --bg-color-white: #ffffff;
  
  /* 边框色 */
  --border-color: #e8e8e8;
  --border-color-light: #f0f0f0;
  
  /* 文字颜色 */
  --text-color-primary: #303133;
  --text-color-regular: #606266;
  --text-color-secondary: #909399;
  --text-color-placeholder: #c0c4cc;
  
  /* 字体 */
  --font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
  
  /* 字体大小 */
  --font-size-extra-large: 18px;
  --font-size-large: 16px;
  --font-size-medium: 14px;
  --font-size-small: 12px;
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  /* 圆角 */
  --border-radius-sm: 2px;
  --border-radius-md: 4px;
  --border-radius-lg: 8px;
  
  /* 阴影 */
  --box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  --box-shadow-light: 0 1px 2px rgba(0, 0, 0, 0.05);
  --box-shadow-dark: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 全局重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  font-size: var(--font-size-medium);
  color: var(--text-color-primary);
  background-color: var(--bg-color);
  line-height: 1.5;
}

/* 按钮样式 */
.btn {
  display: inline-block;
  padding: 8px 16px;
  border: 1px solid transparent;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-medium);
  font-weight: 500;
  text-align: center;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.3s;
  outline: none;
}

.btn-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: #fff;
}

.btn-primary:hover {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

.btn-success {
  background-color: var(--success-color);
  border-color: var(--success-color);
  color: #fff;
}

.btn-success:hover {
  background-color: #85ce61;
  border-color: #85ce61;
}

.btn-warning {
  background-color: var(--warning-color);
  border-color: var(--warning-color);
  color: #fff;
}

.btn-warning:hover {
  background-color: #ebb563;
  border-color: #ebb563;
}

.btn-danger {
  background-color: var(--danger-color);
  border-color: var(--danger-color);
  color: #fff;
}

.btn-danger:hover {
  background-color: #f78989;
  border-color: #f78989;
}

.btn-info {
  background-color: var(--info-color);
  border-color: var(--info-color);
  color: #fff;
}

.btn-info:hover {
  background-color: #a6a9ad;
  border-color: #a6a9ad;
}

.btn-outline {
  background-color: transparent;
  border-color: var(--border-color);
  color: var(--text-color-primary);
}

.btn-outline:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

/* 表单样式 */
.form {
  width: 100%;
}

.form-item {
  margin-bottom: var(--spacing-md);
}

.form-label {
  display: inline-block;
  width: 120px;
  font-weight: 500;
  color: var(--text-color-primary);
  margin-bottom: var(--spacing-xs);
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-medium);
  color: var(--text-color-primary);
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.form-control::placeholder {
  color: var(--text-color-placeholder);
}

/* 卡片样式 */
.card {
  background-color: var(--bg-color-white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-light);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  transition: box-shadow 0.3s;
}

.card:hover {
  box-shadow: var(--box-shadow);
}

.card-header {
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color-light);
  margin-bottom: var(--spacing-md);
}

.card-title {
  font-size: var(--font-size-large);
  font-weight: 500;
  color: var(--text-color-primary);
  margin: 0;
}

/* 表格样式 */
.table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--bg-color-white);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--box-shadow-light);
}

.table th,
.table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color-light);
}

.table th {
  background-color: #fafafa;
  font-weight: 500;
  color: var(--text-color-primary);
}

.table tr:hover {
  background-color: #f5f7fa;
}

/* 对话框样式 */
.dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background-color: var(--bg-color-white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-dark);
  width: 90%;
  max-width: 500px;
  max-height: 80%;
  overflow-y: auto;
}

.dialog-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dialog-title {
  font-size: var(--font-size-large);
  font-weight: 500;
  color: var(--text-color-primary);
  margin: 0;
}

.dialog-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: var(--text-color-secondary);
  transition: color 0.3s;
}

.dialog-close:hover {
  color: var(--text-color-primary);
}

.dialog-body {
  padding: var(--spacing-lg);
}

.dialog-footer {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--border-color-light);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--spacing-md);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-label {
    width: 100%;
    margin-bottom: var(--spacing-xs);
  }
  
  .card {
    padding: var(--spacing-md);
  }
  
  .dialog-content {
    width: 95%;
  }
}

/* 动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

/* 工具类 */
.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.mt-1 { margin-top: var(--spacing-xs); }
.mt-2 { margin-top: var(--spacing-sm); }
.mt-3 { margin-top: var(--spacing-md); }
.mt-4 { margin-top: var(--spacing-lg); }
.mt-5 { margin-top: var(--spacing-xl); }

.mb-1 { margin-bottom: var(--spacing-xs); }
.mb-2 { margin-bottom: var(--spacing-sm); }
.mb-3 { margin-bottom: var(--spacing-md); }
.mb-4 { margin-bottom: var(--spacing-lg); }
.mb-5 { margin-bottom: var(--spacing-xl); }

.ml-1 { margin-left: var(--spacing-xs); }
.ml-2 { margin-left: var(--spacing-sm); }
.ml-3 { margin-left: var(--spacing-md); }
.ml-4 { margin-left: var(--spacing-lg); }
.ml-5 { margin-left: var(--spacing-xl); }

.mr-1 { margin-right: var(--spacing-xs); }
.mr-2 { margin-right: var(--spacing-sm); }
.mr-3 { margin-right: var(--spacing-md); }
.mr-4 { margin-right: var(--spacing-lg); }
.mr-5 { margin-right: var(--spacing-xl); }

.p-1 { padding: var(--spacing-xs); }
.p-2 { padding: var(--spacing-sm); }
.p-3 { padding: var(--spacing-md); }
.p-4 { padding: var(--spacing-lg); }
.p-5 { padding: var(--spacing-xl); }

/* 深色主题 */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #1a1a1a;
    --bg-color-white: #2c2c2c;
    --border-color: #444;
    --border-color-light: #333;
    --text-color-primary: #e0e0e0;
    --text-color-regular: #b0b0b0;
    --text-color-secondary: #808080;
    --text-color-placeholder: #606060;
    --box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    --box-shadow-light: 0 1px 2px rgba(0, 0, 0, 0.2);
    --box-shadow-dark: 0 4px 12px rgba(0, 0, 0, 0.4);
  }
}
"""
        
        return design

if __name__ == "__main__":
    # 测试前端设计技能
    design = FrontendDesign()
    test_input = {
        "parameters": {
            "design_type": "component",
            "framework": "vue",
            "target_platform": "desktop",
            "requirements": "设计一个文件上传组件，支持拖拽上传、文件预览和批量上传功能"
        }
    }
    result = design.run(test_input)
    print(json.dumps(result, ensure_ascii=False, indent=2))