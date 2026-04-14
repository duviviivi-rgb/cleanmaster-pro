<template>
  <div class="config-container">
    <el-card class="config-card">
      <template #header>
        <div class="card-header">
          <span>配置管理</span>
          <el-button type="primary" @click="saveConfig">
            保存配置
          </el-button>
        </div>
      </template>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本配置">
          <el-form :model="configForm" label-width="150px">
            <el-form-item label="默认输出格式">
              <el-select v-model="configForm.defaultOutputFormat">
                <el-option label="HTML" value="html" />
                <el-option label="Markdown" value="markdown" />
                <el-option label="Excel" value="excel" />
              </el-select>
            </el-form-item>
            <el-form-item label="默认模板">
              <el-select v-model="configForm.defaultTemplate">
                <el-option label="标准模板" value="standard" />
                <el-option label="简洁模板" value="simple" />
                <el-option label="详细模板" value="detailed" />
              </el-select>
            </el-form-item>
            <el-form-item label="输出路径">
              <el-input v-model="configForm.outputPath" />
              <el-button type="primary" size="small" @click="selectOutputPath">选择路径</el-button>
            </el-form-item>
            <el-form-item label="自动保存">
              <el-switch v-model="configForm.autoSave" />
            </el-form-item>
            <el-form-item label="显示预览">
              <el-switch v-model="configForm.showPreview" />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="提取规则">
          <el-form :model="extractionRules" label-width="150px">
            <el-form-item label="材料关键词">
              <el-tag
                v-for="(keyword, index) in extractionRules.materialKeywords"
                :key="index"
                closable
                @close="removeKeyword(index)"
                style="margin-right: 8px; margin-bottom: 8px;"
              >
                {{ keyword }}
              </el-tag>
              <el-input
                v-model="newKeyword"
                placeholder="输入关键词"
                style="width: 200px; margin-right: 8px;"
                @keyup.enter="addKeyword"
              />
              <el-button type="primary" size="small" @click="addKeyword">添加</el-button>
            </el-form-item>
            <el-form-item label="型号模式">
              <el-tag
                v-for="(pattern, index) in extractionRules.modelPatterns"
                :key="index"
                closable
                @close="removeModelPattern(index)"
                style="margin-right: 8px; margin-bottom: 8px;"
              >
                {{ pattern }}
              </el-tag>
              <el-input
                v-model="newModelPattern"
                placeholder="输入型号模式"
                style="width: 200px; margin-right: 8px;"
                @keyup.enter="addModelPattern"
              />
              <el-button type="primary" size="small" @click="addModelPattern">添加</el-button>
            </el-form-item>
            <el-form-item label="数量模式">
              <el-tag
                v-for="(pattern, index) in extractionRules.quantityPatterns"
                :key="index"
                closable
                @close="removeQuantityPattern(index)"
                style="margin-right: 8px; margin-bottom: 8px;"
              >
                {{ pattern }}
              </el-tag>
              <el-input
                v-model="newQuantityPattern"
                placeholder="输入数量模式"
                style="width: 200px; margin-right: 8px;"
                @keyup.enter="addQuantityPattern"
              />
              <el-button type="primary" size="small" @click="addQuantityPattern">添加</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="报告模板">
          <el-form :model="reportTemplates" label-width="150px">
            <el-form-item label="模板名称">
              <el-input v-model="newTemplate.name" placeholder="输入模板名称" />
            </el-form-item>
            <el-form-item label="模板描述">
              <el-input type="textarea" v-model="newTemplate.description" placeholder="输入模板描述" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addTemplate">添加模板</el-button>
            </el-form-item>
            <el-form-item label="现有模板">
              <el-table :data="reportTemplates.templates" style="width: 100%">
                <el-table-column prop="name" label="模板名称" />
                <el-table-column prop="description" label="描述" />
                <el-table-column label="操作" width="150">
                  <template #default="scope">
                    <el-button type="primary" size="small" @click="editTemplate(scope.row)">
                      编辑
                    </el-button>
                    <el-button type="danger" size="small" @click="deleteTemplate(scope.row.id)">
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const activeTab = ref('0')
const configForm = ref({
  defaultOutputFormat: 'html',
  defaultTemplate: 'standard',
  outputPath: 'C:\\Reports',
  autoSave: true,
  showPreview: true
})

const extractionRules = ref({
  materialKeywords: ['钢管', '管道', '电缆', '风管', '阀门', '设备'],
  modelPatterns: ['DN\\d+', 'YJV-\\d+x\\d+', '\\d+mm', '\\d+x\\d+'],
  quantityPatterns: ['\\d+\\s*m', '\\d+\\s*m²', '\\d+\\s*个', '\\d+\\s*套']
})

const reportTemplates = ref({
  templates: [
    {
      id: 1,
      name: '标准模板',
      description: '包含所有材料信息的标准报告模板'
    },
    {
      id: 2,
      name: '简洁模板',
      description: '只包含关键信息的简洁报告模板'
    },
    {
      id: 3,
      name: '详细模板',
      description: '包含详细材料信息和检查内容的报告模板'
    }
  ]
})

const newKeyword = ref('')
const newModelPattern = ref('')
const newQuantityPattern = ref('')
const newTemplate = ref({
  name: '',
  description: ''
})

const saveConfig = () => {
  // 实际应用中，这里会将配置保存到后端
  ElMessage.success('配置保存成功')
}

const selectOutputPath = () => {
  // 实际应用中，这里会打开文件选择对话框
  ElMessage.success('路径选择功能开发中...')
}

const addKeyword = () => {
  if (newKeyword.value) {
    extractionRules.value.materialKeywords.push(newKeyword.value)
    newKeyword.value = ''
  }
}

const removeKeyword = (index: number) => {
  extractionRules.value.materialKeywords.splice(index, 1)
}

const addModelPattern = () => {
  if (newModelPattern.value) {
    extractionRules.value.modelPatterns.push(newModelPattern.value)
    newModelPattern.value = ''
  }
}

const removeModelPattern = (index: number) => {
  extractionRules.value.modelPatterns.splice(index, 1)
}

const addQuantityPattern = () => {
  if (newQuantityPattern.value) {
    extractionRules.value.quantityPatterns.push(newQuantityPattern.value)
    newQuantityPattern.value = ''
  }
}

const removeQuantityPattern = (index: number) => {
  extractionRules.value.quantityPatterns.splice(index, 1)
}

const addTemplate = () => {
  if (newTemplate.value.name) {
    const newTemplateItem = {
      id: reportTemplates.value.templates.length + 1,
      name: newTemplate.value.name,
      description: newTemplate.value.description
    }
    reportTemplates.value.templates.push(newTemplateItem)
    newTemplate.value = {
      name: '',
      description: ''
    }
  }
}

const editTemplate = (template: any) => {
  // 实际应用中，这里会打开编辑对话框
  ElMessage.success('模板编辑功能开发中...')
}

const deleteTemplate = (id: number) => {
  reportTemplates.value.templates = reportTemplates.value.templates.filter(t => t.id !== id)
  ElMessage.success('模板删除成功')
}

onMounted(() => {
  // 实际应用中，这里会从后端获取配置数据
  console.log('ConfigView mounted')
})
</script>

<style scoped>
.config-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.config-card {
  max-width: 1200px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-tabs {
  margin-top: 20px;
}

.el-form {
  margin-top: 20px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}
</style>
