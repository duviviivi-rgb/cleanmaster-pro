// API服务

// 基础URL - 使用相对路径，通过Vite代理解决跨域问题
const API_BASE_URL = '/api';

// 通用请求函数
async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    console.log(`发送API请求: ${API_BASE_URL}${endpoint}`);
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log(`API请求成功: ${API_BASE_URL}${endpoint}`, data);
    return data as T;
  } catch (error) {
    console.error(`API请求失败: ${API_BASE_URL}${endpoint}`, error);
    throw error;
  }
}

// 扫描相关API
export const scanApi = {
  // 快速扫描
  quickScan: (disk: string = 'C:') => {
    return request<{
      totalSpace: number;
      usedSpace: number;
      cleanableSpace: number;
      fileTypes: Array<{
        type: string;
        size: number;
        percentage: number;
      }>;
    }>(`/scan/quick?disk=${disk}`, {
      method: 'GET',
    });
  },

  // 深度扫描
  deepScan: (disk: string = 'C:') => {
    return request<{
      totalSpace: number;
      usedSpace: number;
      cleanableSpace: number;
      fileTypes: Array<{
        type: string;
        size: number;
        percentage: number;
      }>;
      files: Array<{
        path: string;
        size: number;
        lastModified: string;
        type: string;
      }>;
    }>(`/scan/deep?disk=${disk}`, {
      method: 'GET',
    });
  },

  // 智能分析
  intelligentAnalysis: (disk: string = 'C:') => {
    return request<{
      usageFrequency: Array<{
        range: string;
        percentage: number;
      }>;
      suggestions: Array<string>;
      estimatedSpaceSaved: number;
    }>(`/scan/analysis?disk=${disk}`, {
      method: 'GET',
    });
  },
};

// 清理相关API
export const cleanApi = {
  // 执行清理
  executeClean: (files: string[], disk: string = 'C:') => {
    return request<{
      success: boolean;
      spaceSaved: number;
      filesDeleted: number;
    }>('/clean/execute', {
      method: 'POST',
      body: JSON.stringify({ files, disk }),
    });
  },

  // 自动清理设置
  setAutoClean: (settings: {
    enabled: boolean;
    frequency: 'daily' | 'weekly' | 'monthly';
    time: string;
    disk: string;
    fileTypes: string[];
  }) => {
    return request<{ success: boolean }>('/clean/auto', {
      method: 'POST',
      body: JSON.stringify(settings),
    });
  },
};

// 空间分析API
export const spaceApi = {
  // 获取空间使用情况
  getSpaceUsage: (disk: string = 'C:') => {
    return request<{
      totalSpace: number;
      usedSpace: number;
      freeSpace: number;
      fileTypes: Array<{
        type: string;
        size: number;
        percentage: number;
      }>;
      largeFiles: Array<{
        path: string;
        size: number;
      }>;
    }>(`/space/usage?disk=${disk}`, {
      method: 'GET',
    });
  },
};

// 文件恢复API
export const recoveryApi = {
  // 扫描可恢复文件
  scanRecoverableFiles: () => {
    return request<Array<{
      id: string;
      name: string;
      size: number;
      deletedTime: string;
      path: string;
    }>>('/recovery/scan', {
      method: 'GET',
    });
  },

  // 恢复文件
  recoverFile: (fileId: string) => {
    return request<{ success: boolean }>(`/recovery/recover/${fileId}`, {
      method: 'POST',
    });
  },
};

// 系统优化API
export const optimizationApi = {
  // 管理启动项
  getStartupItems: () => {
    return request<Array<{
      id: string;
      name: string;
      enabled: boolean;
      path: string;
    }>>('/optimization/startup', {
      method: 'GET',
    });
  },

  // 启用/禁用启动项
  toggleStartupItem: (id: string, enabled: boolean) => {
    return request<{ success: boolean }>('/optimization/startup/toggle', {
      method: 'POST',
      body: JSON.stringify({ id, enabled }),
    });
  },

  // 清理注册表
  cleanRegistry: () => {
    return request<{
      success: boolean;
      itemsCleaned: number;
      spaceSaved: number;
    }>('/optimization/registry', {
      method: 'POST',
    });
  },
};

// 设置API
export const settingsApi = {
  // 获取用户设置
  getSettings: () => {
    return request<{
      language: string;
      theme: 'light' | 'dark';
      autoStart: boolean;
      defaultCleanLevel: 'standard' | 'deep' | 'custom';
      historyRetention: number; // 天数
    }>('/settings', {
      method: 'GET',
    });
  },

  // 保存用户设置
  saveSettings: (settings: {
    language: string;
    theme: 'light' | 'dark';
    autoStart: boolean;
    defaultCleanLevel: 'standard' | 'deep' | 'custom';
    historyRetention: number;
  }) => {
    return request<{ success: boolean }>('/settings', {
      method: 'POST',
      body: JSON.stringify(settings),
    });
  },
};

// 历史记录API
export const historyApi = {
  // 获取清理历史
  getCleanHistory: () => {
    return request<Array<{
      id: string;
      timestamp: string;
      disk: string;
      cleanType: string;
      spaceSaved: number;
      filesDeleted: number;
    }>>('/history', {
      method: 'GET',
    });
  },
};

// 磁盘信息API
export const diskApi = {
  // 获取所有磁盘信息
  getDisks: () => {
    return request<Array<{
      letter: string;
      name: string;
      totalSpace: number;
      usedSpace: number;
      freeSpace: number;
      percentage: number;
    }>>('/disk', {
      method: 'GET',
    });
  },
};

// AI服务API
export const aiApi = {
  // 分析文件
  analyzeFile: (filePath: string) => {
    return request<string>('/ai/analyze-file', {
      method: 'GET',
    });
  },

  // 分类文件
  categorizeFiles: (filePaths: string[]) => {
    return request<Array<string>>('/ai/categorize-files', {
      method: 'GET',
    });
  },

  // 生成文件名
  generateFileName: (filePath: string) => {
    return request<string>('/ai/generate-filename', {
      method: 'GET',
    });
  },

  // 获取清理建议
  getCleaningSuggestions: (diskPath: string) => {
    return request<string>('/ai/cleaning-suggestions', {
      method: 'GET',
    });
  },
};