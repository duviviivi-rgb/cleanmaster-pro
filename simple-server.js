const http = require('http');
const url = require('url');
const fs = require('fs');

const port = 5001;

// 处理CORS
const handleCors = (response) => {
  response.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
  response.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  response.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
};

// 解析JSON请求体
const parseJsonBody = (request) => {
  return new Promise((resolve, reject) => {
    let body = '';
    request.on('data', (chunk) => {
      body += chunk;
    });
    request.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(error);
      }
    });
  });
};

// 处理请求
const handleRequest = async (request, response) => {
  handleCors(response);
  
  // 处理OPTIONS请求
  if (request.method === 'OPTIONS') {
    response.writeHead(204);
    response.end();
    return;
  }
  
  const parsedUrl = url.parse(request.url, true);
  const path = parsedUrl.pathname;
  const query = parsedUrl.query;
  
  // 输出请求信息
  console.log(`收到请求: ${request.method} ${path}`);
  
  // 测试接口
  if (path === '/api/test' && request.method === 'GET') {
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({
      message: 'Hello from CleanMaster Pro backend!',
      status: 'success',
      timestamp: new Date().toISOString()
    }));
    return;
  }
  
  // 磁盘信息接口
  if (path === '/api/disk' && request.method === 'GET') {
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
    
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(mockDisks));
    return;
  }
  
  // 设置接口
  if (path === '/api/settings' && request.method === 'GET') {
    // 模拟设置数据
    const mockSettings = {
      language: 'zh-CN',
      theme: 'light',
      autoStart: false,
      defaultCleanLevel: 'standard',
      historyRetention: 30,
    };
    
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(mockSettings));
    return;
  }
  
  // 保存设置接口
  if (path === '/api/settings' && request.method === 'POST') {
    try {
      const newSettings = await parseJsonBody(request);
      console.log('保存设置:', newSettings);
      
      response.writeHead(200, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({
        success: true,
        message: '设置保存成功',
        settings: newSettings
      }));
    } catch (error) {
      response.writeHead(400, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({
        success: false,
        message: '请求体格式错误'
      }));
    }
    return;
  }
  
  // 快速扫描接口
  if (path === '/api/scan/quick' && request.method === 'GET') {
    const disk = query.disk || 'C:';
    
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
    
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(scanResult));
    return;
  }
  
  // 深度扫描接口
  if (path === '/api/scan/deep' && request.method === 'GET') {
    const disk = query.disk || 'C:';
    
    // 模拟扫描结果
    const scanResult = {
      totalSpace: 135000000000,
      usedSpace: 100000000000,
      cleanableSpace: 3500000000,
      fileTypes: [
        { type: '临时文件', size: 1500000000, percentage: 43 },
        { type: '浏览器缓存', size: 1000000000, percentage: 29 },
        { type: '系统日志', size: 500000000, percentage: 14 },
        { type: '系统更新文件', size: 300000000, percentage: 9 },
        { type: '其他', size: 200000000, percentage: 5 }
      ],
      files: [
        { path: 'C:\\Windows\\Temp\\file1.tmp', size: 100000000, lastModified: '2026-03-28T10:00:00Z', type: '临时文件' },
        { path: 'C:\\Users\\User\\AppData\\Local\\Temp\\file2.tmp', size: 200000000, lastModified: '2026-03-27T15:00:00Z', type: '临时文件' },
        { path: 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache\\file3', size: 500000000, lastModified: '2026-03-26T09:00:00Z', type: '浏览器缓存' }
      ]
    };
    
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(scanResult));
    return;
  }
  
  // 智能分析接口
  if (path === '/api/scan/analysis' && request.method === 'GET') {
    const disk = query.disk || 'C:';
    
    // 模拟分析结果
    const analysisResult = {
      usageFrequency: [
        { range: '最近30天', percentage: 65 },
        { range: '30-90天', percentage: 20 },
        { range: '90天以上', percentage: 15 }
      ],
      suggestions: [
        '清理90天以上未使用的文件，可释放约1.2 GB空间',
        '清理临时文件和浏览器缓存，可释放约800 MB空间',
        '清理系统日志文件，可释放约500 MB空间'
      ],
      estimatedSpaceSaved: 2500000000
    };
    
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(analysisResult));
    return;
  }
  
  // 空间使用情况接口
  if (path === '/api/space/usage' && request.method === 'GET') {
    const disk = query.disk || 'C:';
    
    // 模拟空间使用情况
    const spaceUsageResult = {
      totalSpace: 135000000000,
      usedSpace: 100000000000,
      freeSpace: 35000000000,
      fileTypes: [
        { type: '文档', size: 15000000000, percentage: 15 },
        { type: '图片', size: 10000000000, percentage: 10 },
        { type: '视频', size: 20000000000, percentage: 20 },
        { type: '系统文件', size: 30000000000, percentage: 30 },
        { type: '其他', size: 25000000000, percentage: 25 }
      ],
      largeFiles: [
        { path: 'C:\\Movies\\movie1.mp4', size: 5000000000 },
        { path: 'C:\\Games\\game1.exe', size: 3000000000 },
        { path: 'C:\\Program Files\\program1.exe', size: 2000000000 }
      ]
    };
    
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(spaceUsageResult));
    return;
  }
  
  // 清理执行接口
  if (path === '/api/clean/execute' && request.method === 'POST') {
    try {
      const data = await parseJsonBody(request);
      const files = data.files || [];
      const disk = data.disk || 'C:';
      
      console.log('执行清理:', { files, disk });
      
      // 模拟清理结果
      const cleanResult = {
        success: true,
        spaceSaved: 2500000000,
        filesDeleted: files.length
      };
      
      response.writeHead(200, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify(cleanResult));
    } catch (error) {
      response.writeHead(400, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({
        success: false,
        message: '请求体格式错误'
      }));
    }
    return;
  }
  
  // 自动清理设置接口
  if (path === '/api/clean/auto' && request.method === 'POST') {
    try {
      const settings = await parseJsonBody(request);
      console.log('设置自动清理:', settings);
      
      response.writeHead(200, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({
        success: true
      }));
    } catch (error) {
      response.writeHead(400, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({
        success: false,
        message: '请求体格式错误'
      }));
    }
    return;
  }
  
  // 历史记录接口
  if (path === '/api/history' && request.method === 'GET') {
    // 模拟历史记录
    const history = [
      {
        id: '1',
        timestamp: '2026-03-28T10:00:00Z',
        disk: 'C:',
        cleanType: '快速扫描',
        spaceSaved: 1500000000,
        filesDeleted: 100
      },
      {
        id: '2',
        timestamp: '2026-03-27T15:00:00Z',
        disk: 'C:',
        cleanType: '深度扫描',
        spaceSaved: 2500000000,
        filesDeleted: 200
      },
      {
        id: '3',
        timestamp: '2026-03-26T09:00:00Z',
        disk: 'D:',
        cleanType: '快速扫描',
        spaceSaved: 5000000000,
        filesDeleted: 300
      }
    ];
    
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(history));
    return;
  }
  
  // 根路径返回HTML页面
  if (path === '/' && request.method === 'GET') {
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
          <p>服务运行在 http://localhost:5001</p>
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
            <span class="method post">POST</span>
            <span>/api/settings</span> - 保存用户设置
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
            <span class="method post">POST</span>
            <span>/api/clean/execute</span> - 执行清理
          </div>
          <div class="endpoint">
            <span class="method post">POST</span>
            <span>/api/clean/auto</span> - 设置自动清理
          </div>
          <div class="endpoint">
            <span class="method get">GET</span>
            <span>/api/history</span> - 获取清理历史
          </div>
        </body>
      </html>
    `;
    response.writeHead(200, { 'Content-Type': 'text/html' });
    response.end(html);
    return;
  }
  
  // 404 处理
  response.writeHead(404, { 'Content-Type': 'application/json' });
  response.end(JSON.stringify({
    success: false,
    message: '接口不存在'
  }));
};

// 创建服务器
const server = http.createServer(handleRequest);

// 启动服务器
server.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});