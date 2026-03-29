const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

const PORT = 5009;

// 日志函数
function logRequest(method, pathname, statusCode, message = '') {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${method} ${pathname} - ${statusCode} ${message}`);
}

// 错误处理函数
function handleError(res, statusCode, message, error = null) {
  logRequest(res.req?.method || 'UNKNOWN', res.req?.url || 'UNKNOWN', statusCode, `Error: ${message}`);
  
  res.statusCode = statusCode;
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({
    success: false,
    message: message,
    error: error ? error.message : null,
    timestamp: new Date().toISOString()
  }));
}

// 成功响应函数
function sendSuccess(res, data, message = 'Success') {
  logRequest(res.req?.method || 'UNKNOWN', res.req?.url || 'UNKNOWN', 200, message);
  
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({
    success: true,
    data: data,
    message: message,
    timestamp: new Date().toISOString()
  }));
}

// 模拟数据
const mockData = {
  disks: [
    {
      letter: 'C:',
      name: '系统盘',
      totalSpace: 135000000000,
      usedSpace: 100000000000,
      freeSpace: 35000000000,
      percentage: 74
    },
    {
      letter: 'D:',
      name: '数据盘',
      totalSpace: 500000000000,
      usedSpace: 150000000000,
      freeSpace: 350000000000,
      percentage: 30
    },
    {
      letter: 'E:',
      name: '娱乐盘',
      totalSpace: 250000000000,
      usedSpace: 50000000000,
      freeSpace: 200000000000,
      percentage: 20
    }
  ],
  settings: {
    language: 'zh-CN',
    theme: 'light',
    autoStart: false,
    defaultCleanLevel: 'standard',
    historyRetention: 30
  },
  quickScan: {
    totalSpace: 135000000000,
    usedSpace: 100000000000,
    cleanableSpace: 2500000000,
    fileTypes: [
      { type: '临时文件', size: 1000000000, percentage: 40 },
      { type: '浏览器缓存', size: 750000000, percentage: 30 },
      { type: '系统日志', size: 500000000, percentage: 20 },
      { type: '其他', size: 250000000, percentage: 10 }
    ]
  },
  deepScan: {
    totalSpace: 135000000000,
    usedSpace: 100000000000,
    cleanableSpace: 5000000000,
    fileTypes: [
      { type: '临时文件', size: 2000000000, percentage: 40 },
      { type: '浏览器缓存', size: 1500000000, percentage: 30 },
      { type: '系统日志', size: 1000000000, percentage: 20 },
      { type: '其他', size: 500000000, percentage: 10 }
    ],
    files: [
      { path: 'C:\\Temp\\temp1.txt', size: 1000000, lastModified: '2026-03-28T10:00:00Z', type: '临时文件' },
      { path: 'C:\\Temp\\temp2.txt', size: 2000000, lastModified: '2026-03-27T15:00:00Z', type: '临时文件' },
      { path: 'C:\\Cache\\cache1.dat', size: 1500000, lastModified: '2026-03-26T09:00:00Z', type: '浏览器缓存' },
      { path: 'C:\\Logs\\log1.log', size: 800000, lastModified: '2026-03-25T14:00:00Z', type: '系统日志' }
    ]
  },
  analysis: {
    usageFrequency: [
      { range: '1天内', percentage: 10 },
      { range: '1-7天', percentage: 20 },
      { range: '7-30天', percentage: 30 },
      { range: '30天以上', percentage: 40 }
    ],
    suggestions: [
      '清理临时文件',
      '清理浏览器缓存',
      '清理系统日志',
      '卸载不常用的应用程序'
    ],
    estimatedSpaceSaved: 5000000000
  },
  spaceUsage: {
    totalSpace: 135000000000,
    usedSpace: 100000000000,
    freeSpace: 35000000000,
    fileTypes: [
      { type: '文档', size: 10000000000, percentage: 10 },
      { type: '图片', size: 5000000000, percentage: 5 },
      { type: '视频', size: 20000000000, percentage: 20 },
      { type: '应用程序', size: 30000000000, percentage: 30 },
      { type: '其他', size: 35000000000, percentage: 35 }
    ],
    largeFiles: [
      { path: 'C:\\Program Files\\App1\\app1.exe', size: 5000000000 },
      { path: 'C:\\Videos\\movie.mp4', size: 4000000000 },
      { path: 'C:\\Program Files\\App2\\app2.exe', size: 3000000000 }
    ]
  },
  recoverableFiles: [
    { id: '1', name: 'document.txt', size: 1000000, deletedTime: '2026-03-28T10:00:00Z', path: 'C:\\Documents\\document.txt' },
    { id: '2', name: 'image.jpg', size: 2000000, deletedTime: '2026-03-27T15:00:00Z', path: 'C:\\Pictures\\image.jpg' },
    { id: '3', name: 'file.pdf', size: 3000000, deletedTime: '2026-03-26T09:00:00Z', path: 'C:\\Documents\\file.pdf' }
  ],
  startupItems: [
    { id: '1', name: 'App1', enabled: true, path: 'C:\\Program Files\\App1\\app1.exe' },
    { id: '2', name: 'App2', enabled: false, path: 'C:\\Program Files\\App2\\app2.exe' },
    { id: '3', name: 'App3', enabled: true, path: 'C:\\Program Files\\App3\\app3.exe' }
  ],
  cleanHistory: [
    { id: '1', timestamp: '2026-03-29T10:00:00Z', disk: 'C:', cleanType: '快速清理', spaceSaved: 2500000000, filesDeleted: 100 },
    { id: '2', timestamp: '2026-03-28T15:00:00Z', disk: 'C:', cleanType: '深度清理', spaceSaved: 5000000000, filesDeleted: 200 },
    { id: '3', timestamp: '2026-03-27T09:00:00Z', disk: 'D:', cleanType: '快速清理', spaceSaved: 1000000000, filesDeleted: 50 }
  ]
};

// 创建HTTP服务器
const server = http.createServer((req, res) => {
  // 保存请求信息到响应对象，用于日志记录
  res.req = req;
  
  // 解析URL
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  
  // 处理CORS
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // 处理OPTIONS请求
  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    res.end();
    return;
  }
  
  // 处理GET请求
  if (req.method === 'GET') {
    try {
      // 测试接口
      if (pathname === '/api/test') {
        sendSuccess(res, {
          message: 'Hello from CleanMaster Pro backend!',
          status: 'success',
          timestamp: new Date().toISOString()
        }, '测试接口调用成功');
        return;
      }
      
      // 磁盘信息接口
      else if (pathname === '/api/disk') {
        sendSuccess(res, mockData.disks, '获取磁盘信息成功');
        return;
      }
      
      // 设置接口
      else if (pathname === '/api/settings') {
        sendSuccess(res, mockData.settings, '获取用户设置成功');
        return;
      }
      
      // 快速扫描接口
      else if (pathname === '/api/scan/quick') {
        sendSuccess(res, mockData.quickScan, '快速扫描成功');
        return;
      }
      
      // 深度扫描接口
      else if (pathname === '/api/scan/deep') {
        sendSuccess(res, mockData.deepScan, '深度扫描成功');
        return;
      }
      
      // 智能分析接口
      else if (pathname === '/api/scan/analysis') {
        sendSuccess(res, mockData.analysis, '智能分析成功');
        return;
      }
      
      // 空间使用情况接口
      else if (pathname === '/api/space/usage') {
        sendSuccess(res, mockData.spaceUsage, '获取空间使用情况成功');
        return;
      }
      
      // 可恢复文件扫描接口
      else if (pathname === '/api/recovery/scan') {
        sendSuccess(res, mockData.recoverableFiles, '扫描可恢复文件成功');
        return;
      }
      
      // 启动项管理接口
      else if (pathname === '/api/optimization/startup') {
        sendSuccess(res, mockData.startupItems, '获取启动项成功');
        return;
      }
      
      // 清理历史接口
      else if (pathname === '/api/history') {
        sendSuccess(res, mockData.cleanHistory, '获取清理历史成功');
        return;
      }
      
      // 根路径返回HTML页面
      else if (pathname === '/') {
        res.setHeader('Content-Type', 'text/html');
        res.statusCode = 200;
        const html = `
        <!DOCTYPE html>
        <html lang="zh-CN">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>CleanMaster Pro 后端服务</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f5f5f5;
              }
              h1 {
                color: #333;
              }
              p {
                color: #666;
              }
              .endpoint {
                background-color: #fff;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
              }
              .method {
                font-weight: bold;
                margin-right: 10px;
              }
              .get {
                color: #28a745;
              }
              .post {
                color: #007bff;
              }
            </style>
          </head>
          <body>
            <h1>CleanMaster Pro 后端服务</h1>
            <p>服务运行在 http://localhost:${PORT}</p>
            <h2>可用的API接口:</h2>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/test</span> - 测试接口
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/disk</span> - 获取磁盘信息
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/settings</span> - 获取用户设置
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/scan/quick</span> - 快速扫描
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/scan/deep</span> - 深度扫描
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/scan/analysis</span> - 智能分析
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/space/usage</span> - 空间使用情况
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/recovery/scan</span> - 扫描可恢复文件
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/optimization/startup</span> - 获取启动项
            </div>
            <div class="endpoint">
              <span class="method get">GET</span>
              <span>/api/history</span> - 获取清理历史
            </div>
            <div class="endpoint">
              <span class="method post">POST</span>
              <span>/api/settings</span> - 保存用户设置
            </div>
            <div class="endpoint">
              <span class="method post">POST</span>
              <span>/api/clean/execute</span> - 执行清理
            </div>
            <div class="endpoint">
              <span class="method post">POST</span>
              <span>/api/clean/auto</span> - 设置自动清理
            </div>
            <div class="endpoint">
              <span class="method post">POST</span>
              <span>/api/recovery/recover/:id</span> - 恢复文件
            </div>
            <div class="endpoint">
              <span class="method post">POST</span>
              <span>/api/optimization/startup/toggle</span> - 启用/禁用启动项
            </div>
            <div class="endpoint">
              <span class="method post">POST</span>
              <span>/api/optimization/registry</span> - 清理注册表
            </div>
          </body>
        </html>
        `;
        res.end(html);
        return;
      }
      
      // 404 处理
      handleError(res, 404, '接口不存在');
    } catch (error) {
      handleError(res, 500, '服务器内部错误', error);
    }
  }
  
  // 处理POST请求
  else if (req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        // 保存设置接口
        if (pathname === '/api/settings') {
          const settings = JSON.parse(body);
          sendSuccess(res, {
            settings: settings,
            message: '设置保存成功'
          }, '设置保存成功');
          return;
        }
        
        // 执行清理接口
        else if (pathname === '/api/clean/execute') {
          const data = JSON.parse(body);
          sendSuccess(res, {
            spaceSaved: 2500000000,
            filesDeleted: data.files ? data.files.length : 0,
            message: '清理执行成功'
          }, '清理执行成功');
          return;
        }
        
        // 设置自动清理接口
        else if (pathname === '/api/clean/auto') {
          const settings = JSON.parse(body);
          sendSuccess(res, {
            settings: settings,
            message: '自动清理设置成功'
          }, '自动清理设置成功');
          return;
        }
        
        // 恢复文件接口
        else if (pathname.match(/^\/api\/recovery\/recover\/\w+$/)) {
          const fileId = pathname.split('/').pop();
          sendSuccess(res, {
            fileId: fileId,
            message: '文件恢复成功'
          }, '文件恢复成功');
          return;
        }
        
        // 启用/禁用启动项接口
        else if (pathname === '/api/optimization/startup/toggle') {
          const data = JSON.parse(body);
          sendSuccess(res, {
            id: data.id,
            enabled: data.enabled,
            message: '启动项状态更新成功'
          }, '启动项状态更新成功');
          return;
        }
        
        // 清理注册表接口
        else if (pathname === '/api/optimization/registry') {
          sendSuccess(res, {
            itemsCleaned: 50,
            spaceSaved: 100000000,
            message: '注册表清理成功'
          }, '注册表清理成功');
          return;
        }
        
        // 404 处理
        handleError(res, 404, '接口不存在');
      } catch (error) {
        handleError(res, 500, '服务器内部错误', error);
      }
    });
    return;
  }
  
  // 405 方法不允许
  handleError(res, 405, '请求方法不允许');
});

// 启动服务器
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
  console.log(`API Documentation: http://localhost:${PORT}/`);
});
