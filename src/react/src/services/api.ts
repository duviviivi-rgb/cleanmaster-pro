import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

// API方法
export const apiService = {
  // 磁盘相关
  getDisks: async () => {
    return api.get('/disks');
  },

  getDiskDetail: async (letter: string) => {
    return api.get(`/disk/${letter}`);
  },

  // 扫描相关
  startScan: async (disk: string, scanType: string) => {
    return api.post('/scan/start', { disk, scan_type: scanType });
  },

  getScanStatus: async () => {
    return api.get('/scan/status');
  },

  stopScan: async () => {
    return api.post('/scan/stop');
  },

  // 清理相关
  startClean: async (disk: string, files: string[]) => {
    return api.post('/clean/start', { disk, files });
  },

  getCleanStatus: async () => {
    return api.get('/clean/status');
  },

  stopClean: async () => {
    return api.post('/clean/stop');
  },

  setAutoClean: async (enabled: boolean, frequency: string, time: string) => {
    return api.post('/clean/autoclean', { enabled, frequency, time });
  },

  // 空间管理
  analyzeSpace: async (disk: string) => {
    return api.post('/space/analyze', { disk });
  },

  getLargeFiles: async (disk: string, minSize: number) => {
    return api.get(`/space/large-files?disk=${disk}&min_size=${minSize}`);
  },

  getDuplicateFiles: async (disk: string) => {
    return api.get(`/space/duplicate-files?disk=${disk}`);
  },

  // 应用管理
  scanApps: async () => {
    return api.post('/app/scan');
  },

  uninstallApp: async (appIds: string[]) => {
    return api.post('/app/uninstall', { app_ids: appIds });
  },

  getAppDetail: async (appId: string) => {
    return api.get(`/app/detail/${appId}`);
  },

  // 数据治理
  analyzeData: async (disk: string) => {
    return api.post('/governance/analyze', { disk });
  },

  optimizeData: async (disk: string) => {
    return api.post('/governance/optimize', { disk });
  },

  backupData: async (source: string, destination: string) => {
    return api.post('/governance/backup', { source, destination });
  },

  // 历史记录
  getHistory: async () => {
    return api.get('/history');
  },

  getHistoryAnalysis: async () => {
    return api.get('/history/analysis');
  },

  deleteHistory: async (id: string) => {
    return api.delete(`/history/${id}`);
  },

  clearHistory: async () => {
    return api.post('/history/clear');
  },

  // 系统优化
  analyzeSystem: async () => {
    return api.post('/optimization/analyze');
  },

  manageStartup: async (startupItems: any[]) => {
    return api.post('/optimization/startup', { startup_items: startupItems });
  },

  manageServices: async (services: any[]) => {
    return api.post('/optimization/services', { services });
  },

  defragDisk: async (disk: string) => {
    return api.post('/optimization/defrag', { disk });
  },

  // 文件恢复
  scanRecovery: async (disk: string, scanType: string) => {
    return api.post('/recovery/scan', { disk, scan_type: scanType });
  },

  startRecovery: async (files: string[], destination: string) => {
    return api.post('/recovery/start', { files, destination });
  },

  getRecoveryStatus: async () => {
    return api.get('/recovery/status');
  },

  stopRecovery: async () => {
    return api.post('/recovery/stop');
  },
};

export default apiService;