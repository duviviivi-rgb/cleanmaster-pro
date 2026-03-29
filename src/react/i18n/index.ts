// 国际化支持

// 语言类型
export type Language = 'zh-CN' | 'en-US';

// 翻译类型
interface Translations {
  [key: string]: string | Translations;
}

// 中文翻译
const zhCN: Translations = {
  // 导航
  navigation: {
    quickScan: '快速扫描',
    deepClean: '深度清理',
    intelligentAnalysis: '智能分析',
    spaceVisualization: '空间可视化',
    autoClean: '自动清理',
    fileRecovery: '文件恢复',
    systemOptimization: '系统优化',
    settings: '设置',
  },
  // 快速扫描
  quickScan: {
    title: '快速扫描',
    description: '扫描C盘，识别可清理的文件类型',
    scanContent: '扫描内容',
    tempFiles: '临时文件',
    browserCache: '浏览器缓存',
    systemLogs: '系统日志',
    recycleBin: '回收站文件',
    startScan: '开始扫描',
    cleanableSpace: '可清理空间',
    usedSpace: '已使用',
    totalSpace: '总空间',
    fileTypeDistribution: '文件类型分布',
  },
  // 深度清理
  deepClean: {
    title: '深度清理',
    description: '深度扫描C盘，识别更多可清理文件',
    scanContent: '扫描内容',
    tempFiles: '临时文件',
    browserCache: '浏览器缓存',
    systemLogs: '系统日志',
    recycleBin: '回收站文件',
    systemUpdateFiles: '系统更新文件',
    oldWindowsFiles: '旧版本Windows文件',
    appCache: '应用程序缓存',
    startDeepScan: '开始深度扫描',
  },
  // 智能分析
  intelligentAnalysis: {
    title: '智能分析',
    description: '分析用户使用习惯，提供个性化清理建议',
    startAnalysis: '开始分析',
    usageFrequencyAnalysis: '文件使用频率分析',
    recent30Days: '最近30天使用的文件',
    days3090: '30-90天未使用的文件',
    over90Days: '90天以上未使用的文件',
    personalizedSuggestions: '个性化清理建议',
  },
  // 空间可视化
  spaceVisualization: {
    title: '空间可视化',
    description: '直观展示磁盘空间使用情况和内容分类',
    visualizationType: '可视化方式',
    treeMap: '树形图',
    pieChart: '饼图',
    barChart: '柱状图',
    heatMap: '热力图',
    visualization3D: '3D可视化',
  },
  // 自动清理
  autoClean: {
    title: '自动清理',
    description: '设置定期自动清理任务',
    enableAutoClean: '启用自动清理',
    cleanFrequency: '清理频率',
    daily: '每天',
    weekly: '每周',
    monthly: '每月',
    cleanTime: '清理时间',
    cleanContent: '清理内容',
    saveSettings: '保存设置',
  },
  // 文件恢复
  fileRecovery: {
    title: '文件恢复',
    description: '恢复误删除的文件',
    scanRecoverableFiles: '扫描可恢复文件',
    recoverableFiles: '可恢复文件',
    fileName: '文件名称',
    size: '大小',
    deletedTime: '删除时间',
    action: '操作',
    recover: '恢复',
  },
  // 系统优化
  systemOptimization: {
    title: '系统优化',
    description: '优化系统设置，提升性能',
    startupManagement: '启动项管理',
    manageStartupItems: '管理启动项',
    serviceOptimization: '服务优化',
    optimizeServices: '优化服务',
    registryCleaning: '注册表清理',
    cleanRegistry: '清理注册表',
  },
  // 设置
  settings: {
    title: '设置',
    basicSettings: '基本设置',
    language: '语言',
    theme: '主题',
    light: '浅色',
    dark: '深色',
    autoStart: '启动时自动运行',
    cleanSettings: '清理设置',
    defaultCleanLevel: '默认清理级别',
    standard: '标准',
    deep: '深度',
    custom: '自定义',
    advancedSettings: '高级设置',
    historyRetention: '清理历史保留时间',
    days: '天',
    forever: '永久',
    saveSettings: '保存设置',
  },
  // 右侧信息栏
  sidebar: {
    diskInfo: '磁盘信息',
    cleaningSuggestions: '清理建议',
    systemStatus: '系统状态',
    cpuUsage: 'CPU使用率',
    memoryUsage: '内存使用率',
    bootTime: '系统启动时间',
  },
  // 底部
  footer: {
    version: 'CleanMaster Pro v1.0.0',
    help: '帮助',
    about: '关于',
  },
  // 通用
  common: {
    success: '成功',
    error: '错误',
    warning: '警告',
    info: '信息',
    confirm: '确认',
    cancel: '取消',
    loading: '加载中...',
    noData: '暂无数据',
  },
};

// 英文翻译
const enUS: Translations = {
  // 导航
  navigation: {
    quickScan: 'Quick Scan',
    deepClean: 'Deep Clean',
    intelligentAnalysis: 'Intelligent Analysis',
    spaceVisualization: 'Space Visualization',
    autoClean: 'Auto Clean',
    fileRecovery: 'File Recovery',
    systemOptimization: 'System Optimization',
    settings: 'Settings',
  },
  // 快速扫描
  quickScan: {
    title: 'Quick Scan',
    description: 'Scan C drive to identify cleanable file types',
    scanContent: 'Scan Content',
    tempFiles: 'Temporary Files',
    browserCache: 'Browser Cache',
    systemLogs: 'System Logs',
    recycleBin: 'Recycle Bin Files',
    startScan: 'Start Scan',
    cleanableSpace: 'Cleanable Space',
    usedSpace: 'Used',
    totalSpace: 'Total',
    fileTypeDistribution: 'File Type Distribution',
  },
  // 深度清理
  deepClean: {
    title: 'Deep Clean',
    description: 'Deep scan C drive to identify more cleanable files',
    scanContent: 'Scan Content',
    tempFiles: 'Temporary Files',
    browserCache: 'Browser Cache',
    systemLogs: 'System Logs',
    recycleBin: 'Recycle Bin Files',
    systemUpdateFiles: 'System Update Files',
    oldWindowsFiles: 'Old Windows Files',
    appCache: 'Application Cache',
    startDeepScan: 'Start Deep Scan',
  },
  // 智能分析
  intelligentAnalysis: {
    title: 'Intelligent Analysis',
    description: 'Analyze user usage habits and provide personalized cleaning suggestions',
    startAnalysis: 'Start Analysis',
    usageFrequencyAnalysis: 'File Usage Frequency Analysis',
    recent30Days: 'Files used in the last 30 days',
    days3090: 'Files unused for 30-90 days',
    over90Days: 'Files unused for over 90 days',
    personalizedSuggestions: 'Personalized Cleaning Suggestions',
  },
  // 空间可视化
  spaceVisualization: {
    title: 'Space Visualization',
    description: 'Intuitively display disk space usage and content classification',
    visualizationType: 'Visualization Type',
    treeMap: 'Tree Map',
    pieChart: 'Pie Chart',
    barChart: 'Bar Chart',
    heatMap: 'Heat Map',
    visualization3D: '3D Visualization',
  },
  // 自动清理
  autoClean: {
    title: 'Auto Clean',
    description: 'Set up regular automatic cleaning tasks',
    enableAutoClean: 'Enable Auto Clean',
    cleanFrequency: 'Cleaning Frequency',
    daily: 'Daily',
    weekly: 'Weekly',
    monthly: 'Monthly',
    cleanTime: 'Cleaning Time',
    cleanContent: 'Cleaning Content',
    saveSettings: 'Save Settings',
  },
  // 文件恢复
  fileRecovery: {
    title: 'File Recovery',
    description: 'Recover accidentally deleted files',
    scanRecoverableFiles: 'Scan Recoverable Files',
    recoverableFiles: 'Recoverable Files',
    fileName: 'File Name',
    size: 'Size',
    deletedTime: 'Deleted Time',
    action: 'Action',
    recover: 'Recover',
  },
  // 系统优化
  systemOptimization: {
    title: 'System Optimization',
    description: 'Optimize system settings to improve performance',
    startupManagement: 'Startup Management',
    manageStartupItems: 'Manage Startup Items',
    serviceOptimization: 'Service Optimization',
    optimizeServices: 'Optimize Services',
    registryCleaning: 'Registry Cleaning',
    cleanRegistry: 'Clean Registry',
  },
  // 设置
  settings: {
    title: 'Settings',
    basicSettings: 'Basic Settings',
    language: 'Language',
    theme: 'Theme',
    light: 'Light',
    dark: 'Dark',
    autoStart: 'Auto-start on boot',
    cleanSettings: 'Cleaning Settings',
    defaultCleanLevel: 'Default Cleaning Level',
    standard: 'Standard',
    deep: 'Deep',
    custom: 'Custom',
    advancedSettings: 'Advanced Settings',
    historyRetention: 'Cleaning History Retention',
    days: 'days',
    forever: 'Forever',
    saveSettings: 'Save Settings',
  },
  // 右侧信息栏
  sidebar: {
    diskInfo: 'Disk Information',
    cleaningSuggestions: 'Cleaning Suggestions',
    systemStatus: 'System Status',
    cpuUsage: 'CPU Usage',
    memoryUsage: 'Memory Usage',
    bootTime: 'System Boot Time',
  },
  // 底部
  footer: {
    version: 'CleanMaster Pro v1.0.0',
    help: 'Help',
    about: 'About',
  },
  // 通用
  common: {
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    info: 'Info',
    confirm: 'Confirm',
    cancel: 'Cancel',
    loading: 'Loading...',
    noData: 'No data',
  },
};

// 所有语言
const translations = {
  'zh-CN': zhCN,
  'en-US': enUS,
};

// 翻译函数
export function t(key: string, language: Language = 'zh-CN'): string {
  const keys = key.split('.');
  let result: Translations | string = translations[language];

  for (const k of keys) {
    if (typeof result === 'object' && result !== null) {
      result = result[k];
    } else {
      return key; // 返回原键名作为默认值
    }
  }

  return typeof result === 'string' ? result : key;
}

// 获取支持的语言
export function getSupportedLanguages(): Array<{
  value: Language;
  label: string;
}> {
  return [
    { value: 'zh-CN', label: '简体中文' },
    { value: 'en-US', label: 'English' },
  ];
}
