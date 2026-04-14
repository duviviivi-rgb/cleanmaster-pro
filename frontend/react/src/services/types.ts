// API类型定义

// 解析文件请求
export interface ParseFilesRequest {
  file_paths: string[];
}

// 解析文件响应
export interface ParseFilesResponse {
  success: boolean;
  data?: {
    file_path: string;
    texts: string[];
    notes: string[];
    drawing_info: {
      name: string;
      number: string;
      format: string;
      software: string;
    };
  }[];
  error?: string;
}

// 提取材料请求
export interface ExtractMaterialsRequest {
  texts: string[];
  notes: string[];
}

// 材料信息
export interface Material {
  name: string;
  model: string;
  quantity: number;
  unit: string;
  position: string;
  floor: string;
  drawing_number: string;
  drawing_name: string;
  category: string;
  inspection_batch: string;
  standard: string;
}

// 提取材料响应
export interface ExtractMaterialsResponse {
  success: boolean;
  data?: Material[];
  error?: string;
}

// 生成检测批请求
export interface GenerateInspectionBatchRequest {
  materials: Material[];
}

// 生成检测批响应
export interface GenerateInspectionBatchResponse {
  success: boolean;
  data?: any;
  error?: string;
}

// 配置信息
export interface Config {
  [key: string]: any;
}

// 历史记录
export interface HistoryRecord {
  id: string;
  type: string;
  data: any;
  timestamp: string;
}

// 历史记录响应
export interface HistoryResponse {
  success: boolean;
  data?: HistoryRecord[];
  error?: string;
}