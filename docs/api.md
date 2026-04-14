# CleanMaster Pro API 契约文档

> **版本**: v1.1.0  
> **最后更新**: 2026-04-01  
> **文档用途**: 前后端开发契约，确保接口一致性

---

## 1. 基础信息

### 1.1 服务器配置
- **开发环境**: `http://localhost:5009`
- **前端代理**: `http://localhost:5173` (Vite开发服务器)
- **基础路径**: `/api`
- **内容类型**: `application/json`

### 1.2 通用响应格式

#### 成功响应
```json
{
  "success": true,
  "data": { /* 具体数据 */ },
  "message": "操作成功",
  "timestamp": "2026-04-01T10:00:00.000Z"
}
```

#### 错误响应
```json
{
  "success": false,
  "message": "错误描述",
  "error": "详细错误信息（可选）",
  "timestamp": "2026-04-01T10:00:00.000Z"
}
```

### 1.3 HTTP 状态码
| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | 成功 | 所有成功请求 |
| 400 | 请求参数错误 | 参数缺失或格式错误 |
| 404 | 接口不存在 | 请求路径错误 |
| 405 | 方法不允许 | HTTP方法错误 |
| 500 | 服务器内部错误 | 服务器异常 |

---

## 2. 数据模型定义

### 2.1 磁盘信息 (Disk)
```typescript
interface Disk {
  letter: string;           // 盘符，如 "C:"
  name: string;             // 磁盘名称，如 "系统盘"
  totalSpace: number;       // 总空间（字节）
  usedSpace: number;        // 已用空间（字节）
  freeSpace: number;        // 可用空间（字节）
  percentage: number;       // 使用百分比（0-100）
}
```

### 2.2 用户设置 (Settings)
```typescript
interface Settings {
  language: 'zh-CN' | 'en-US';  // 语言
  theme: 'light' | 'dark';      // 主题
  autoStart: boolean;           // 自动启动
  defaultCleanLevel: 'quick' | 'standard' | 'deep';  // 默认清理级别
  historyRetention: number;     // 历史保留天数
}
```

### 2.3 扫描结果 (ScanResult)
```typescript
interface ScanResult {
  totalSpace: number;       // 总空间
  usedSpace: number;        // 已用空间
  cleanableSpace: number;   // 可清理空间
  fileTypes: FileType[];    // 文件类型分布
  files?: FileInfo[];       // 详细文件列表（深度扫描）
}

interface FileType {
  type: string;             // 类型名称
  size: number;             // 大小（字节）
  percentage: number;       // 占比（0-100）
}

interface FileInfo {
  path: string;             // 文件路径
  size: number;             // 文件大小
  lastModified: string;     // 最后修改时间（ISO 8601）
  type: string;             // 文件类型
}
```

### 2.4 智能分析 (Analysis)
```typescript
interface Analysis {
  usageFrequency: FrequencyItem[];  // 使用频率分布
  suggestions: string[];            // 优化建议
  estimatedSpaceSaved: number;      // 预计可节省空间
}

interface FrequencyItem {
  range: string;            // 时间范围，如 "1天内"
  percentage: number;       // 占比（0-100）
}
```

### 2.5 空间使用 (SpaceUsage)
```typescript
interface SpaceUsage {
  totalSpace: number;       // 总空间
  usedSpace: number;        // 已用空间
  freeSpace: number;        // 可用空间
  fileTypes: FileType[];    // 文件类型分布
  largeFiles: LargeFile[];  // 大文件列表
}

interface LargeFile {
  path: string;             // 文件路径
  size: number;             // 文件大小
}
```

### 2.6 可恢复文件 (RecoverableFile)
```typescript
interface RecoverableFile {
  id: string;               // 文件ID
  name: string;             // 文件名
  size: number;             // 文件大小
  deletedTime: string;      // 删除时间（ISO 8601）
  path: string;             // 原始路径
}
```

### 2.7 启动项 (StartupItem)
```typescript
interface StartupItem {
  id: string;               // 启动项ID
  name: string;             // 名称
  enabled: boolean;         // 是否启用
  path: string;             // 程序路径
}
```

### 2.8 清理历史 (CleanHistory)
```typescript
interface CleanHistory {
  id: string;               // 记录ID
  timestamp: string;        // 清理时间（ISO 8601）
  disk: string;             // 磁盘
  cleanType: string;        // 清理类型
  spaceSaved: number;       // 节省空间
  filesDeleted: number;     // 删除文件数
}
```

### 2.9 文件夹分类 (FolderCategory)
```typescript
interface FolderCategorization {
  categories: Category[];   // 分类列表
  suggestions: string[];    // 归类建议
}

interface Category {
  name: string;             // 分类名称
  extensions: string[];     // 文件扩展名列表
  path: string;             // 文件夹路径
  files: number;            // 文件数量
  size: number;             // 总大小
}
```

### 2.10 文件元数据 (FileMetadata)
```typescript
interface FileMetadataItem {
  id: string;               // 文件ID
  path: string;             // 文件路径
  name: string;             // 文件名
  size: number;             // 文件大小
  lastModified: string;     // 最后修改时间
  extension: string;        // 扩展名
  metadata: Metadata;       // 元数据
}

interface Metadata {
  author: string;           // 作者
  created: string;          // 创建时间
  tags: string[];           // 标签
  description: string;      // 描述
}
```

### 2.11 重复文件 (DuplicateFile)
```typescript
interface DuplicateFiles {
  duplicateGroups: DuplicateGroup[];  // 重复文件组
  totalSize: number;                  // 总可节省空间
}

interface DuplicateGroup {
  groupId: string;          // 组ID
  files: DuplicateFile[];   // 重复文件列表
  size: number;             // 单个文件大小
}

interface DuplicateFile {
  id: string;               // 文件ID
  path: string;             // 文件路径
  size: number;             // 文件大小
  lastModified: string;     // 最后修改时间
}
```

### 2.12 文件版本 (FileVersion)
```typescript
interface FileVersionItem {
  id: string;               // 文件ID
  path: string;             // 文件路径
  name: string;             // 文件名
  currentVersion: string;   // 当前版本号
  versions: Version[];      // 版本列表
}

interface Version {
  version: string;          // 版本号
  size: number;             // 版本大小
  created: string;          // 创建时间
  description: string;      // 版本描述
}
```

### 2.13 应用程序信息 (Application)
```typescript
interface Application {
  id: string;               // 应用ID
  name: string;             // 应用名称
  displayName: string;      // 显示名称
  version: string;          // 版本号
  publisher: string;        // 发布者
  installDate: string;      // 安装日期（ISO 8601）
  installLocation: string;  // 安装路径
  installSource: string;    // 安装源路径
  uninstallString: string;  // 卸载命令
  size: number;             // 占用空间（字节）
  iconPath?: string;        // 图标路径
  
  // 使用状态
  lastUsedTime?: string;    // 最后使用时间
  usageCount: number;       // 使用次数
  
  // 健康状态
  status: 'healthy' | 'broken' | 'incomplete' | 'dormant' | 'unknown';
  statusReason: string;     // 状态原因描述
  
  // 清理建议
  recommendation: 'keep' | 'remove' | 'review';
  recommendationReason: string;  // 建议原因
  confidence: number;       // 建议置信度（0-100）
  
  // 残留文件
  residualFiles?: ResidualFile[];
  registryEntries?: RegistryEntry[];
}

interface ResidualFile {
  path: string;             // 文件路径
  size: number;             // 文件大小
  type: 'executable' | 'config' | 'data' | 'log' | 'temp';
  lastModified: string;     // 最后修改时间
}

interface RegistryEntry {
  key: string;              // 注册表键
  value: string;            // 注册表值
  type: string;             // 值类型
}

interface ApplicationScanResult {
  applications: Application[];           // 应用程序列表
  totalSize: number;                     // 总占用空间
  brokenApps: Application[];             // 损坏的应用
  incompleteApps: Application[];         // 未完全卸载的应用
  dormantApps: Application[];            // 沉睡应用
  recommendations: AppRecommendation[];  // 清理建议
}

interface AppRecommendation {
  appId: string;            // 应用ID
  appName: string;          // 应用名称
  action: 'remove' | 'keep' | 'review';
  reason: string;           // 建议原因
  spaceSaved: number;       // 预计节省空间
  risk: 'low' | 'medium' | 'high';  // 风险等级
}
```

---

## 3. API 接口列表

### 3.1 测试接口

#### GET /api/test
**描述**: 测试后端服务是否正常运行

**请求参数**: 无

**响应示例**:
```json
{
  "success": true,
  "data": {
    "message": "Hello from CleanMaster Pro backend!",
    "status": "success",
    "timestamp": "2026-04-01T10:00:00.000Z"
  },
  "message": "测试接口调用成功",
  "timestamp": "2026-04-01T10:00:00.000Z"
}
```

---

### 3.2 磁盘管理

#### GET /api/disk
**描述**: 获取所有磁盘信息

**请求参数**: 无

**响应数据**: `Disk[]`

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "letter": "C:",
      "name": "系统盘",
      "totalSpace": 135000000000,
      "usedSpace": 100000000000,
      "freeSpace": 35000000000,
      "percentage": 74
    }
  ],
  "message": "获取磁盘信息成功"
}
```

---

### 3.3 用户设置

#### GET /api/settings
**描述**: 获取用户设置

**请求参数**: 无

**响应数据**: `Settings`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "language": "zh-CN",
    "theme": "light",
    "autoStart": false,
    "defaultCleanLevel": "standard",
    "historyRetention": 30
  },
  "message": "获取用户设置成功"
}
```

#### POST /api/settings
**描述**: 保存用户设置

**请求体**: `Settings`

**请求示例**:
```json
{
  "language": "zh-CN",
  "theme": "dark",
  "autoStart": true,
  "defaultCleanLevel": "deep",
  "historyRetention": 60
}
```

**响应数据**:
```typescript
{
  settings: Settings;       // 保存的设置
  message: string;          // 成功消息
}
```

---

### 3.4 扫描功能

#### GET /api/scan/quick
**描述**: 执行快速扫描

**请求参数**: 无

**响应数据**: `ScanResult`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "totalSpace": 135000000000,
    "usedSpace": 100000000000,
    "cleanableSpace": 2500000000,
    "fileTypes": [
      { "type": "临时文件", "size": 1000000000, "percentage": 40 },
      { "type": "浏览器缓存", "size": 750000000, "percentage": 30 }
    ]
  },
  "message": "快速扫描成功"
}
```

#### GET /api/scan/deep
**描述**: 执行深度扫描

**请求参数**: 无

**响应数据**: `ScanResult`（包含files字段）

**响应示例**:
```json
{
  "success": true,
  "data": {
    "totalSpace": 135000000000,
    "usedSpace": 100000000000,
    "cleanableSpace": 5000000000,
    "fileTypes": [...],
    "files": [
      {
        "path": "C:\\Temp\\temp1.txt",
        "size": 1000000,
        "lastModified": "2026-03-28T10:00:00Z",
        "type": "临时文件"
      }
    ]
  },
  "message": "深度扫描成功"
}
```

#### GET /api/scan/analysis
**描述**: 执行智能分析

**请求参数**: 无

**响应数据**: `Analysis`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "usageFrequency": [
      { "range": "1天内", "percentage": 10 },
      { "range": "1-7天", "percentage": 20 }
    ],
    "suggestions": ["清理临时文件", "清理浏览器缓存"],
    "estimatedSpaceSaved": 5000000000
  },
  "message": "智能分析成功"
}
```

---

### 3.5 空间管理

#### GET /api/space/usage
**描述**: 获取空间使用情况

**请求参数**: 无

**响应数据**: `SpaceUsage`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "totalSpace": 135000000000,
    "usedSpace": 100000000000,
    "freeSpace": 35000000000,
    "fileTypes": [...],
    "largeFiles": [
      { "path": "C:\\Program Files\\App1\\app1.exe", "size": 5000000000 }
    ]
  },
  "message": "获取空间使用情况成功"
}
```

---

### 3.6 文件恢复

#### GET /api/recovery/scan
**描述**: 扫描可恢复文件

**请求参数**: 无

**响应数据**: `RecoverableFile[]`

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "name": "document.txt",
      "size": 1000000,
      "deletedTime": "2026-03-28T10:00:00Z",
      "path": "C:\\Documents\\document.txt"
    }
  ],
  "message": "扫描可恢复文件成功"
}
```

#### POST /api/recovery/recover/:id
**描述**: 恢复指定文件

**路径参数**:
- `id`: 文件ID

**请求体**: 无

**响应数据**:
```typescript
{
  fileId: string;           // 恢复的文件ID
  message: string;          // 成功消息
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "fileId": "1",
    "message": "文件恢复成功"
  },
  "message": "文件恢复成功"
}
```

---

### 3.7 系统优化

#### GET /api/optimization/startup
**描述**: 获取启动项列表

**请求参数**: 无

**响应数据**: `StartupItem[]`

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "name": "App1",
      "enabled": true,
      "path": "C:\\Program Files\\App1\\app1.exe"
    }
  ],
  "message": "获取启动项成功"
}
```

#### POST /api/optimization/startup/toggle
**描述**: 启用/禁用启动项

**请求体**:
```typescript
{
  id: string;               // 启动项ID
  enabled: boolean;         // 目标状态
}
```

**请求示例**:
```json
{
  "id": "1",
  "enabled": false
}
```

**响应数据**:
```typescript
{
  id: string;               // 启动项ID
  enabled: boolean;         // 更新后的状态
  message: string;          // 成功消息
}
```

#### POST /api/optimization/registry
**描述**: 清理注册表

**请求体**: 无

**响应数据**:
```typescript
{
  itemsCleaned: number;     // 清理的注册表项数
  spaceSaved: number;       // 节省的空间
  message: string;          // 成功消息
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "itemsCleaned": 50,
    "spaceSaved": 100000000,
    "message": "注册表清理成功"
  },
  "message": "注册表清理成功"
}
```

---

### 3.8 清理历史

#### GET /api/history
**描述**: 获取清理历史记录

**请求参数**: 无

**响应数据**: `CleanHistory[]`

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "timestamp": "2026-03-29T10:00:00Z",
      "disk": "C:",
      "cleanType": "快速清理",
      "spaceSaved": 2500000000,
      "filesDeleted": 100
    }
  ],
  "message": "获取清理历史成功"
}
```

---

### 3.9 清理执行

#### POST /api/clean/execute
**描述**: 执行清理操作

**请求体**:
```typescript
{
  files?: string[];         // 要清理的文件路径列表（可选）
  type?: 'quick' | 'deep';  // 清理类型（可选）
}
```

**请求示例**:
```json
{
  "files": ["C:\\Temp\\temp1.txt", "C:\\Temp\\temp2.txt"],
  "type": "quick"
}
```

**响应数据**:
```typescript
{
  spaceSaved: number;       // 节省的空间
  filesDeleted: number;     // 删除的文件数
  message: string;          // 成功消息
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "spaceSaved": 2500000000,
    "filesDeleted": 2,
    "message": "清理执行成功"
  },
  "message": "清理执行成功"
}
```

#### POST /api/clean/auto
**描述**: 设置自动清理

**请求体**:
```typescript
{
  enabled: boolean;         // 是否启用
  schedule?: string;        // 定时规则（cron格式，可选）
  cleanLevel?: string;      // 清理级别（可选）
}
```

**请求示例**:
```json
{
  "enabled": true,
  "schedule": "0 2 * * 0",
  "cleanLevel": "standard"
}
```

**响应数据**:
```typescript
{
  settings: object;         // 自动清理设置
  message: string;          // 成功消息
}
```

---

### 3.10 文件夹归类

#### GET /api/folder/categorize
**描述**: 智能文件夹归类

**请求参数**: 无

**响应数据**: `FolderCategorization`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "name": "文档",
        "extensions": [".txt", ".doc", ".pdf"],
        "path": "C:\\Documents",
        "files": 150,
        "size": 5000000000
      }
    ],
    "suggestions": ["将所有文档文件移动到 Documents 文件夹"]
  },
  "message": "智能文件夹归类成功"
}
```

---

### 3.11 AI 服务

#### GET /api/ai/analyze-file
**描述**: 分析单个文件

**查询参数**:
- `path`: 文件路径（可选，如未提供则使用默认示例）

**响应数据**: `string` - 文件分析结果

**响应示例**:
```json
{
  "success": true,
  "data": "文件类型: .txt, 大小: 1024 bytes, 最后修改时间: 2026-03-29 10:00:00",
  "message": "文件分析成功"
}
```

#### GET /api/ai/categorize-files
**描述**: 批量分类文件

**查询参数**:
- `paths`: 文件路径列表，逗号分隔（可选）

**响应数据**: `string[]` - 分类结果列表

**响应示例**:
```json
{
  "success": true,
  "data": [
    "C:\\example.txt -> 文档",
    "C:\\image.jpg -> 图片",
    "C:\\video.mp4 -> 视频"
  ],
  "message": "文件分类成功"
}
```

#### GET /api/ai/generate-filename
**描述**: 生成优化的文件名

**查询参数**:
- `path`: 原文件路径（可选）

**响应数据**: `string` - 新文件名

**响应示例**:
```json
{
  "success": true,
  "data": "old_file_optimized.txt",
  "message": "文件名生成成功"
}
```

#### GET /api/ai/cleaning-suggestions
**描述**: 获取清理建议

**查询参数**:
- `disk`: 磁盘路径，如 "C:\\"（可选）

**响应数据**: `string` - 清理建议

**响应示例**:
```json
{
  "success": true,
  "data": "建议清理临时文件、浏览器缓存和系统日志文件。",
  "message": "清理建议获取成功"
}
```

---

### 3.12 数据治理

#### GET /api/governance/metadata
**描述**: 获取文件元数据

**请求参数**: 无

**响应数据**:
```typescript
{
  files: FileMetadataItem[];  // 文件元数据列表
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "files": [
      {
        "id": "1",
        "path": "C:\\Documents\\file1.txt",
        "name": "file1.txt",
        "size": 1024,
        "lastModified": "2026-03-29T10:00:00Z",
        "extension": ".txt",
        "metadata": {
          "author": "User",
          "created": "2026-03-28T15:00:00Z",
          "tags": ["document", "important"],
          "description": "Important document"
        }
      }
    ]
  },
  "message": "文件元数据获取成功"
}
```

#### GET /api/governance/duplicates
**描述**: 检测重复文件

**请求参数**: 无

**响应数据**: `DuplicateFiles`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "duplicateGroups": [
      {
        "groupId": "1",
        "files": [
          { "id": "1", "path": "C:\\Documents\\file1.txt", "size": 1024, "lastModified": "2026-03-29T10:00:00Z" },
          { "id": "2", "path": "C:\\Backup\\file1.txt", "size": 1024, "lastModified": "2026-03-28T15:00:00Z" }
        ],
        "size": 1024
      }
    ],
    "totalSize": 6144
  },
  "message": "重复文件检测成功"
}
```

#### GET /api/governance/versions
**描述**: 获取文件版本信息

**请求参数**: 无

**响应数据**:
```typescript
{
  files: FileVersionItem[];  // 文件版本列表
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "files": [
      {
        "id": "1",
        "path": "C:\\Documents\\file1.txt",
        "name": "file1.txt",
        "currentVersion": "3",
        "versions": [
          { "version": "1", "size": 512, "created": "2026-03-27T10:00:00Z", "description": "Initial version" },
          { "version": "2", "size": 768, "created": "2026-03-28T15:00:00Z", "description": "Updated content" },
          { "version": "3", "size": 1024, "created": "2026-03-29T10:00:00Z", "description": "Final version" }
        ]
      }
    ]
  },
  "message": "文件版本管理成功"
}
```

---

### 3.13 应用程序管理

#### GET /api/apps/scan
**描述**: 扫描系统中的应用程序，识别损坏、未完全卸载和沉睡的应用

**请求参数**: 无

**响应数据**: `ApplicationScanResult`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "applications": [
      {
        "id": "app_001",
        "name": "OldSoftware",
        "displayName": "旧版软件",
        "version": "1.0.0",
        "publisher": "Unknown",
        "installDate": "2025-01-15T10:00:00Z",
        "installLocation": "C:\\Program Files\\OldSoftware",
        "installSource": "C:\\Downloads\\oldsoftware.exe",
        "uninstallString": "C:\\Program Files\\OldSoftware\\uninstall.exe",
        "size": 524288000,
        "lastUsedTime": "2025-06-01T08:00:00Z",
        "usageCount": 5,
        "status": "dormant",
        "statusReason": "超过6个月未使用",
        "recommendation": "remove",
        "recommendationReason": "长时间未使用，建议卸载以释放空间",
        "confidence": 85,
        "residualFiles": [
          {
            "path": "C:\\Users\\User\\AppData\\Local\\OldSoftware\\config.ini",
            "size": 10240,
            "type": "config",
            "lastModified": "2025-06-01T08:00:00Z"
          }
        ]
      },
      {
        "id": "app_002",
        "name": "BrokenApp",
        "displayName": "损坏的应用",
        "version": "2.5.0",
        "publisher": "SomeCompany",
        "installDate": "2025-03-20T14:00:00Z",
        "installLocation": "C:\\Program Files\\BrokenApp",
        "size": 104857600,
        "status": "broken",
        "statusReason": "主程序文件缺失或损坏",
        "recommendation": "remove",
        "recommendationReason": "应用已损坏，无法正常运行",
        "confidence": 95
      },
      {
        "id": "app_003",
        "name": "IncompleteUninstall",
        "displayName": "未完全卸载的应用",
        "version": "1.2.0",
        "publisher": "AnotherCompany",
        "installDate": "2025-02-10T09:00:00Z",
        "installLocation": "C:\\Program Files\\IncompleteUninstall",
        "size": 26214400,
        "status": "incomplete",
        "statusReason": "卸载程序不完整，残留文件和注册表项",
        "recommendation": "review",
        "recommendationReason": "检测到残留文件，建议清理",
        "confidence": 75,
        "residualFiles": [
          {
            "path": "C:\\Program Files\\IncompleteUninstall\\残留文件.dll",
            "size": 2097152,
            "type": "executable",
            "lastModified": "2025-08-15T16:00:00Z"
          }
        ],
        "registryEntries": [
          {
            "key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\IncompleteUninstall",
            "value": "InstallPath",
            "type": "REG_SZ"
          }
        ]
      }
    ],
    "totalSize": 655360000,
    "brokenApps": [
      {
        "id": "app_002",
        "name": "BrokenApp",
        "status": "broken",
        "recommendation": "remove"
      }
    ],
    "incompleteApps": [
      {
        "id": "app_003",
        "name": "IncompleteUninstall",
        "status": "incomplete",
        "recommendation": "review"
      }
    ],
    "dormantApps": [
      {
        "id": "app_001",
        "name": "OldSoftware",
        "status": "dormant",
        "recommendation": "remove"
      }
    ],
    "recommendations": [
      {
        "appId": "app_001",
        "appName": "旧版软件",
        "action": "remove",
        "reason": "超过6个月未使用，占用500MB空间",
        "spaceSaved": 524288000,
        "risk": "low"
      },
      {
        "appId": "app_002",
        "appName": "损坏的应用",
        "action": "remove",
        "reason": "应用已损坏无法运行，占用100MB空间",
        "spaceSaved": 104857600,
        "risk": "low"
      },
      {
        "appId": "app_003",
        "appName": "未完全卸载的应用",
        "action": "review",
        "reason": "检测到残留文件和注册表项，建议手动检查",
        "spaceSaved": 26214400,
        "risk": "medium"
      }
    ]
  },
  "message": "应用程序扫描成功"
}
```

#### GET /api/apps/:id/details
**描述**: 获取指定应用程序的详细信息

**路径参数**:
- `id`: 应用ID

**响应数据**: `Application`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": "app_001",
    "name": "OldSoftware",
    "displayName": "旧版软件",
    "version": "1.0.0",
    "publisher": "Unknown",
    "installDate": "2025-01-15T10:00:00Z",
    "installLocation": "C:\\Program Files\\OldSoftware",
    "size": 524288000,
    "lastUsedTime": "2025-06-01T08:00:00Z",
    "usageCount": 5,
    "status": "dormant",
    "statusReason": "超过6个月未使用",
    "recommendation": "remove",
    "recommendationReason": "长时间未使用，建议卸载以释放空间",
    "confidence": 85,
    "residualFiles": [...],
    "registryEntries": [...]
  },
  "message": "获取应用详情成功"
}
```

#### POST /api/apps/:id/uninstall
**描述**: 卸载指定的应用程序

**路径参数**:
- `id`: 应用ID

**请求体**:
```typescript
{
  removeResidual: boolean;  // 是否同时删除残留文件
  createBackup: boolean;    // 是否创建备份
}
```

**请求示例**:
```json
{
  "removeResidual": true,
  "createBackup": false
}
```

**响应数据**:
```typescript
{
  appId: string;            // 卸载的应用ID
  appName: string;          // 应用名称
  spaceSaved: number;       // 释放的空间
  filesRemoved: number;     // 删除的文件数
  registryEntriesRemoved: number;  // 删除的注册表项数
  message: string;          // 成功消息
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "appId": "app_001",
    "appName": "旧版软件",
    "spaceSaved": 524288000,
    "filesRemoved": 45,
    "registryEntriesRemoved": 12,
    "message": "应用卸载成功"
  },
  "message": "应用卸载成功"
}
```

#### POST /api/apps/clean-residual
**描述**: 清理应用程序的残留文件和注册表项

**请求体**:
```typescript
{
  appId: string;            // 应用ID
  files: string[];          // 要删除的文件路径列表
  registryKeys: string[];   // 要删除的注册表键列表
}
```

**请求示例**:
```json
{
  "appId": "app_003",
  "files": [
    "C:\\Program Files\\IncompleteUninstall\\残留文件.dll",
    "C:\\Users\\User\\AppData\\Local\\IncompleteUninstall"
  ],
  "registryKeys": [
    "HKEY_LOCAL_MACHINE\\SOFTWARE\\IncompleteUninstall"
  ]
}
```

**响应数据**:
```typescript
{
  appId: string;            // 应用ID
  filesRemoved: number;     // 删除的文件数
  registryEntriesRemoved: number;  // 删除的注册表项数
  spaceSaved: number;       // 释放的空间
  message: string;          // 成功消息
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "appId": "app_003",
    "filesRemoved": 3,
    "registryEntriesRemoved": 5,
    "spaceSaved": 26214400,
    "message": "残留文件清理成功"
  },
  "message": "残留文件清理成功"
}
```

#### GET /api/apps/recommendations
**描述**: 获取应用程序清理建议汇总

**请求参数**: 无

**响应数据**:
```typescript
{
  totalApps: number;                    // 总应用数
  brokenCount: number;                  // 损坏应用数
  incompleteCount: number;              // 未完全卸载数
  dormantCount: number;                 // 沉睡应用数
  totalRecommendations: number;         // 总建议数
  totalSpaceSaved: number;              // 预计可释放总空间
  highPriority: AppRecommendation[];    // 高优先级建议
  mediumPriority: AppRecommendation[];  // 中优先级建议
  lowPriority: AppRecommendation[];     // 低优先级建议
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "totalApps": 45,
    "brokenCount": 2,
    "incompleteCount": 3,
    "dormantCount": 8,
    "totalRecommendations": 13,
    "totalSpaceSaved": 2147483648,
    "highPriority": [
      {
        "appId": "app_002",
        "appName": "损坏的应用",
        "action": "remove",
        "reason": "应用已损坏无法运行",
        "spaceSaved": 104857600,
        "risk": "low"
      }
    ],
    "mediumPriority": [...],
    "lowPriority": [...]
  },
  "message": "获取清理建议成功"
}
```

---

## 4. 前端调用规范

### 4.1 API 服务封装

```typescript
// src/services/api.ts

const API_BASE_URL = 'http://localhost:5009';

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
  timestamp: string;
}

async function request<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}

// 磁盘管理
export const diskApi = {
  getDisks: () => request<Disk[]>('/api/disk'),
};

// 用户设置
export const settingsApi = {
  getSettings: () => request<Settings>('/api/settings'),
  saveSettings: (settings: Settings) => 
    request<Settings>('/api/settings', {
      method: 'POST',
      body: JSON.stringify(settings),
    }),
};

// 扫描功能
export const scanApi = {
  quickScan: () => request<ScanResult>('/api/scan/quick'),
  deepScan: () => request<ScanResult>('/api/scan/deep'),
  analyze: () => request<Analysis>('/api/scan/analysis'),
};

// 空间管理
export const spaceApi = {
  getUsage: () => request<SpaceUsage>('/api/space/usage'),
};

// 文件恢复
export const recoveryApi = {
  scanRecoverable: () => request<RecoverableFile[]>('/api/recovery/scan'),
  recoverFile: (id: string) => 
    request<{ fileId: string; message: string }>(`/api/recovery/recover/${id}`, {
      method: 'POST',
    }),
};

// 系统优化
export const optimizationApi = {
  getStartupItems: () => request<StartupItem[]>('/api/optimization/startup'),
  toggleStartup: (id: string, enabled: boolean) => 
    request<{ id: string; enabled: boolean; message: string }>(
      '/api/optimization/startup/toggle',
      {
        method: 'POST',
        body: JSON.stringify({ id, enabled }),
      }
    ),
  cleanRegistry: () => 
    request<{ itemsCleaned: number; spaceSaved: number; message: string }>(
      '/api/optimization/registry',
      { method: 'POST' }
    ),
};

// 清理历史
export const historyApi = {
  getHistory: () => request<CleanHistory[]>('/api/history'),
};

// 清理执行
export const cleanApi = {
  execute: (files?: string[], type?: 'quick' | 'deep') => 
    request<{ spaceSaved: number; filesDeleted: number; message: string }>(
      '/api/clean/execute',
      {
        method: 'POST',
        body: JSON.stringify({ files, type }),
      }
    ),
  setAuto: (settings: { enabled: boolean; schedule?: string; cleanLevel?: string }) => 
    request('/api/clean/auto', {
      method: 'POST',
      body: JSON.stringify(settings),
    }),
};

// 文件夹归类
export const folderApi = {
  categorize: () => request<FolderCategorization>('/api/folder/categorize'),
};

// AI 服务
export const aiApi = {
  analyzeFile: (path?: string) => 
    request<string>(`/api/ai/analyze-file${path ? `?path=${encodeURIComponent(path)}` : ''}`),
  categorizeFiles: (paths?: string[]) => 
    request<string[]>(`/api/ai/categorize-files${paths ? `?paths=${paths.join(',')}` : ''}`),
  generateFileName: (path?: string) => 
    request<string>(`/api/ai/generate-filename${path ? `?path=${encodeURIComponent(path)}` : ''}`),
  getCleaningSuggestions: (disk?: string) => 
    request<string>(`/api/ai/cleaning-suggestions${disk ? `?disk=${encodeURIComponent(disk)}` : ''}`),
};

// 数据治理
export const governanceApi = {
  getMetadata: () => request<{ files: FileMetadataItem[] }>('/api/governance/metadata'),
  getDuplicates: () => request<DuplicateFiles>('/api/governance/duplicates'),
  getVersions: () => request<{ files: FileVersionItem[] }>('/api/governance/versions'),
};

// 应用程序管理
export const appsApi = {
  scanApps: () => request<ApplicationScanResult>('/api/apps/scan'),
  getAppDetails: (id: string) => request<Application>(`/api/apps/${id}/details`),
  uninstallApp: (id: string, removeResidual: boolean = true, createBackup: boolean = false) => 
    request<{ 
      appId: string; 
      appName: string; 
      spaceSaved: number; 
      filesRemoved: number; 
      registryEntriesRemoved: number; 
      message: string;
    }>(`/api/apps/${id}/uninstall`, {
      method: 'POST',
      body: JSON.stringify({ removeResidual, createBackup }),
    }),
  cleanResidual: (appId: string, files: string[], registryKeys: string[]) => 
    request<{
      appId: string;
      filesRemoved: number;
      registryEntriesRemoved: number;
      spaceSaved: number;
      message: string;
    }>('/api/apps/clean-residual', {
      method: 'POST',
      body: JSON.stringify({ appId, files, registryKeys }),
    }),
  getRecommendations: () => request<{
    totalApps: number;
    brokenCount: number;
    incompleteCount: number;
    dormantCount: number;
    totalRecommendations: number;
    totalSpaceSaved: number;
    highPriority: AppRecommendation[];
    mediumPriority: AppRecommendation[];
    lowPriority: AppRecommendation[];
  }>('/api/apps/recommendations'),
};
```

### 4.2 错误处理规范

```typescript
// 统一错误处理
async function handleApiCall<T>(
  apiCall: () => Promise<ApiResponse<T>>
): Promise<T | null> {
  try {
    const response = await apiCall();
    if (response.success) {
      return response.data;
    } else {
      console.error('API Error:', response.message);
      // 可以在这里添加 toast 通知
      return null;
    }
  } catch (error) {
    console.error('Network Error:', error);
    // 可以在这里添加 toast 通知
    return null;
  }
}

// 使用示例
const disks = await handleApiCall(() => diskApi.getDisks());
```

### 4.3 加载状态管理

```typescript
// 在组件中使用
const [loading, setLoading] = useState(false);
const [data, setData] = useState<Disk[]>([]);

const loadData = async () => {
  setLoading(true);
  try {
    const result = await handleApiCall(() => diskApi.getDisks());
    if (result) {
      setData(result);
    }
  } finally {
    setLoading(false);
  }
};
```

---

## 5. 版本控制与更新流程

### 5.1 文档版本规则
- **主版本号**: 不兼容的API更改
- **次版本号**: 向下兼容的功能添加
- **修订号**: 问题修复

### 5.2 更新流程
1. **后端修改** → 更新 `api.md` 文档
2. **文档审核** → 确保前后端理解一致
3. **前端修改** → 根据新文档调整前端代码
4. **联调测试** → 验证接口一致性

### 5.3 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v1.1.0 | 2026-04-01 | 添加应用程序管理功能：识别损坏/未完全卸载/沉睡应用，提供智能清理建议 | AI Assistant |
| v1.0.0 | 2026-04-01 | 初始版本，包含所有基础API | AI Assistant |

---

## 6. 附录

### 6.1 开发环境配置

#### 后端启动
```bash
node node-server.js
# 服务运行在 http://localhost:5009
```

#### 前端启动
```bash
npm run dev
# 服务运行在 http://localhost:5173
```

### 6.2 测试工具

#### 使用 curl 测试API
```bash
# 测试接口
curl http://localhost:5009/api/test

# 获取磁盘信息
curl http://localhost:5009/api/disk

# 保存设置
curl -X POST http://localhost:5009/api/settings \
  -H "Content-Type: application/json" \
  -d '{"language":"zh-CN","theme":"dark"}'
```

#### 使用 Postman/Insomnia
1. 导入本文档作为参考
2. 创建 Collection
3. 设置环境变量 `baseUrl = http://localhost:5009`

### 6.3 常见问题

**Q: 跨域问题如何解决？**  
A: 后端已配置CORS，允许前端访问。开发环境使用Vite代理。

**Q: 如何添加新的API接口？**  
A: 1. 在本文档中添加接口定义 2. 后端实现 3. 前端调用 4. 更新变更记录

**Q: 数据模型变更如何处理？**  
A: 1. 更新本文档数据模型章节 2. 同步更新前后端代码 3. 进行兼容性测试

---

**文档维护**: 前后端开发人员共同维护  
**审核周期**: 每次API变更后更新  
**沟通渠道**: 通过本文档进行技术对齐
