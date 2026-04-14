import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 文件解析接口
export const parseFiles = async (filePaths: string[]) => {
  try {
    const response = await api.post('/parse', {
      file_paths: filePaths
    })
    return response.data
  } catch (error) {
    console.error('文件解析失败:', error)
    throw error
  }
}

// 材料提取接口
export const extractMaterials = async (texts: string[], notes: string[]) => {
  try {
    const response = await api.post('/extract', {
      texts,
      notes
    })
    return response.data
  } catch (error) {
    console.error('材料提取失败:', error)
    throw error
  }
}

// 报告生成接口
export const generateReport = async (data: any, format: string) => {
  try {
    const response = await api.post('/generate', {
      data,
      format
    })
    return response.data
  } catch (error) {
    console.error('报告生成失败:', error)
    throw error
  }
}

// 配置管理接口
export const getConfig = async (key: string) => {
  try {
    const response = await api.get('/config', {
      data: { key }
    })
    return response.data
  } catch (error) {
    console.error('获取配置失败:', error)
    throw error
  }
}

export const setConfig = async (key: string, value: any) => {
  try {
    const response = await api.post('/config', {
      key,
      value
    })
    return response.data
  } catch (error) {
    console.error('设置配置失败:', error)
    throw error
  }
}

// 历史记录接口
export const getHistory = async (filters: any) => {
  try {
    const response = await api.get('/history', {
      data: { filters }
    })
    return response.data
  } catch (error) {
    console.error('获取历史记录失败:', error)
    throw error
  }
}

export const addHistory = async (record: any) => {
  try {
    const response = await api.post('/history', {
      record
    })
    return response.data
  } catch (error) {
    console.error('添加历史记录失败:', error)
    throw error
  }
}

export const getHistoryById = async (id: number) => {
  try {
    const response = await api.get(`/history/${id}`)
    return response.data
  } catch (error) {
    console.error('获取历史记录失败:', error)
    throw error
  }
}

export const deleteHistory = async (id: number) => {
  try {
    const response = await api.delete(`/history/${id}`)
    return response.data
  } catch (error) {
    console.error('删除历史记录失败:', error)
    throw error
  }
}

export const reprocessHistory = async (id: number) => {
  try {
    const response = await api.post(`/history/${id}/reprocess`)
    return response.data
  } catch (error) {
    console.error('重新处理失败:', error)
    throw error
  }
}

export default {
  parseFiles,
  extractMaterials,
  generateReport,
  getConfig,
  setConfig,
  getHistory,
  addHistory,
  getHistoryById,
  deleteHistory,
  reprocessHistory
}
