<template>
  <div class="material-edit-container">
    <el-card class="filter-card">
      <template #header>
        <div class="card-header">
          <span>材料筛选</span>
        </div>
      </template>
      <div class="filter-form">
        <el-form :inline="true" :model="filterForm" class="demo-form-inline">
          <el-form-item label="楼层">
            <el-select v-model="filterForm.floor" placeholder="选择楼层">
              <el-option label="全部" value="" />
              <el-option label="一层" value="一层" />
              <el-option label="二层" value="二层" />
              <el-option label="三层" value="三层" />
              <el-option label="四层" value="四层" />
              <el-option label="三层夹层" value="三层夹层" />
            </el-select>
          </el-form-item>
          <el-form-item label="图纸号">
            <el-input v-model="filterForm.drawingNumber" placeholder="输入图纸号" />
          </el-form-item>
          <el-form-item label="材料名称">
            <el-input v-model="filterForm.materialName" placeholder="输入材料名称" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="applyFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    
    <el-card class="material-list-card">
      <template #header>
        <div class="card-header">
          <span>材料列表</span>
          <el-button type="primary" @click="generateReport">
            生成报告
          </el-button>
        </div>
      </template>
      <div class="material-list">
        <el-table :data="filteredMaterials" style="width: 100%">
          <el-table-column prop="drawing_number" label="图纸号" width="120" />
          <el-table-column prop="drawing_name" label="图纸名称" width="180" />
          <el-table-column prop="floor" label="楼层" width="100" />
          <el-table-column prop="name" label="材料名称" />
          <el-table-column prop="model" label="型号" width="120" />
          <el-table-column prop="quantity" label="数量" width="100" />
          <el-table-column prop="unit" label="单位" width="80" />
          <el-table-column prop="position" label="位置" width="150" />
          <el-table-column prop="category" label="分类" width="150" />
          <el-table-column prop="inspection_batch" label="检验批" width="150" />
          <el-table-column prop="standard" label="标准" width="200" />
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button type="primary" size="small" @click="editMaterial(scope.row)">
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="deleteMaterial(scope.row.id)">
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
            :total="filteredMaterials.length"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>
    
    <el-dialog
      v-model="editDialogVisible"
      title="编辑材料"
      width="60%"
    >
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="图纸号">
          <el-input v-model="editForm.drawing_number" />
        </el-form-item>
        <el-form-item label="图纸名称">
          <el-input v-model="editForm.drawing_name" />
        </el-form-item>
        <el-form-item label="楼层">
          <el-select v-model="editForm.floor">
            <el-option label="一层" value="一层" />
            <el-option label="二层" value="二层" />
            <el-option label="三层" value="三层" />
            <el-option label="四层" value="四层" />
            <el-option label="三层夹层" value="三层夹层" />
          </el-select>
        </el-form-item>
        <el-form-item label="材料名称">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="型号">
          <el-input v-model="editForm.model" />
        </el-form-item>
        <el-form-item label="数量">
          <el-input type="number" v-model="editForm.quantity" />
        </el-form-item>
        <el-form-item label="单位">
          <el-input v-model="editForm.unit" />
        </el-form-item>
        <el-form-item label="位置">
          <el-input v-model="editForm.position" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="editForm.category">
            <el-option label="建筑给排水和水暖" value="建筑给排水和水暖" />
            <el-option label="通风空调" value="通风空调" />
            <el-option label="电气" value="电气" />
            <el-option label="智能建筑" value="智能建筑" />
            <el-option label="医疗气体工程" value="医疗气体工程" />
            <el-option label="建筑装饰" value="建筑装饰" />
            <el-option label="主体结构" value="主体结构" />
            <el-option label="建筑节能" value="建筑节能" />
          </el-select>
        </el-form-item>
        <el-form-item label="检验批">
          <el-input v-model="editForm.inspection_batch" />
        </el-form-item>
        <el-form-item label="标准">
          <el-input v-model="editForm.standard" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveMaterial">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMaterialStore, Material } from '../store/material'

const router = useRouter()
const materialStore = useMaterialStore()

const filterForm = ref({
  floor: '',
  drawingNumber: '',
  materialName: ''
})

const currentPage = ref(1)
const pageSize = ref(20)
const editDialogVisible = ref(false)
const editForm = ref<Material>({
  id: '',
  name: '',
  model: '',
  quantity: 0,
  unit: '',
  position: '',
  floor: '',
  drawing_number: '',
  drawing_name: '',
  category: '',
  inspection_batch: '',
  standard: ''
})

// 模拟材料数据
const mockMaterials: Material[] = [
  {
    id: '1',
    name: '304金属钢管',
    model: 'DN50',
    quantity: 10,
    unit: 'm',
    position: '图中未知区域',
    floor: '三层',
    drawing_number: '水施-03',
    drawing_name: '三层排水系统',
    category: '建筑给排水和水暖',
    inspection_batch: '给排水管道安装',
    standard: 'GB50242-2002, GB50268-2008'
  },
  {
    id: '2',
    name: 'PPR管',
    model: 'DN32',
    quantity: 20,
    unit: 'm',
    position: '图中未知区域',
    floor: '三层',
    drawing_number: '水施-03',
    drawing_name: '三层排水系统',
    category: '建筑给排水和水暖',
    inspection_batch: '给排水管道安装',
    standard: 'GB50242-2002, GB50268-2008'
  },
  {
    id: '3',
    name: '镀锌钢板风管',
    model: '1000x500',
    quantity: 15,
    unit: 'm²',
    position: '图中未知区域',
    floor: '四层',
    drawing_number: '风施-02',
    drawing_name: '四层通风系统',
    category: '通风空调',
    inspection_batch: '风管安装',
    standard: 'GB50243-2016'
  },
  {
    id: '4',
    name: '电缆',
    model: 'YJV-3x2.5',
    quantity: 50,
    unit: 'm',
    position: '图中未知区域',
    floor: '三层夹层',
    drawing_number: '电施-05',
    drawing_name: '三层夹层电气系统',
    category: '电气',
    inspection_batch: '电气线路安装',
    standard: 'GB50303-2015'
  },
  {
    id: '5',
    name: '医用氧气管道',
    model: 'DN25',
    quantity: 8,
    unit: 'm',
    position: '图中未知区域',
    floor: '三层',
    drawing_number: '医气-01',
    drawing_name: '三层医气系统',
    category: '医疗气体工程',
    inspection_batch: '医疗气体管道安装',
    standard: 'GB50751-2012'
  }
]

const materials = computed(() => materialStore.materials)
const filteredMaterials = computed(() => {
  let result = materials.value
  
  if (filterForm.value.floor) {
    result = result.filter(m => m.floor === filterForm.value.floor)
  }
  
  if (filterForm.value.drawingNumber) {
    result = result.filter(m => m.drawing_number.includes(filterForm.value.drawingNumber))
  }
  
  if (filterForm.value.materialName) {
    result = result.filter(m => m.name.includes(filterForm.value.materialName))
  }
  
  return result
})

const applyFilter = () => {
  // 筛选逻辑已在computed中实现
}

const resetFilter = () => {
  filterForm.value = {
    floor: '',
    drawingNumber: '',
    materialName: ''
  }
}

const editMaterial = (material: Material) => {
  editForm.value = { ...material }
  editDialogVisible.value = true
}

const saveMaterial = () => {
  materialStore.updateMaterial(editForm.value.id, editForm.value)
  editDialogVisible.value = false
  ElMessage.success('材料信息更新成功')
}

const deleteMaterial = (id: string) => {
  materialStore.removeMaterial(id)
  ElMessage.success('材料删除成功')
}

const generateReport = () => {
  // 跳转到报告预览页面
  router.push('/report-preview')
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

onMounted(() => {
  // 模拟从后端获取材料数据
  materialStore.clearMaterials()
  mockMaterials.forEach(material => {
    materialStore.addMaterial(material)
  })
})
</script>

<style scoped>
.material-edit-container {
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

.material-list-card {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
