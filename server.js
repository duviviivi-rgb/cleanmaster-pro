const express = require('express');
const cors = require('cors');

const app = express();
const port = 5000;

// 配置CORS
app.use(cors({
  origin: 'http://localhost:3000', // 允许前端访问的地址
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// 解析JSON请求体
app.use(express.json());

// 测试接口
app.get('/api/test', (req, res) => {
  res.json({
    message: 'Hello from CleanMaster Pro backend!',
    status: 'success',
    timestamp: new Date().toISOString()
  });
});

// 磁盘信息接口
app.get('/api/disk', (req, res) => {
  // 模拟磁盘信息数据
  const mockDisks = [
    {
      letter: 'C:',
      name: '系统盘',
      totalSpace: 135000000000,
      usedSpace: 100000000000,
      freeSpace: 35000000000,
      percentage: 74,
    },
    {
      letter: 'D:',
      name: '数据盘',
      totalSpace: 500000000000,
      usedSpace: 150000000000,
      freeSpace: 350000000000,
      percentage: 30,
    },
    {
      letter: 'E:',
      name: '娱乐盘',
      totalSpace: 250000000000,
      usedSpace: 50000000000,
      freeSpace: 200000000000,
      percentage: 20,
    },
  ];
  
  res.json(mockDisks);
});

// 设置接口
app.get('/api/settings', (req, res) => {
  // 模拟设置数据
  const mockSettings = {
    language: 'zh-CN',
    theme: 'light',
    autoStart: false,
    defaultCleanLevel: 'standard',
    historyRetention: 30,
  };
  
  res.json(mockSettings);
});

// 保存设置接口
app.post('/api/settings', (req, res) => {
  const newSettings = req.body;
  console.log('保存设置:', newSettings);
  
  res.json({
    success: true,
    message: '设置保存成功',
    settings: newSettings
  });
});

// 快速扫描接口
app.get('/api/scan/quick', (req, res) => {
  const disk = req.query.disk || 'C:';
  
  // 模拟扫描结果
  const scanResult = {
    totalSpace: 135000000000,
    usedSpace: 100000000000,
    cleanableSpace: 2500000000,
    fileTypes: [
      { type: '临时文件', size: 1000000000, percentage: 40 },
      { type: '浏览器缓存', size: 750000000, percentage: 30 },
      { type: '系统日志', size: 500000000, percentage: 20 },
      { type: '其他', size: 250000000, percentage: 10 }
    ]
  };
  
  res.json(scanResult);
});

// 启动服务器
app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});