import http.server
import socketserver
import json

PORT = 5007

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 处理CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
        # 测试接口
        if self.path == '/api/test':
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'message': 'Hello from CleanMaster Pro backend!',
                'status': 'success',
                'timestamp': '2026-03-29T12:00:00Z'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 磁盘信息接口
        elif self.path == '/api/disk':
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = [
                {
                    'letter': 'C:',
                    'name': '系统盘',
                    'totalSpace': 135000000000,
                    'usedSpace': 100000000000,
                    'freeSpace': 35000000000,
                    'percentage': 74
                },
                {
                    'letter': 'D:',
                    'name': '数据盘',
                    'totalSpace': 500000000000,
                    'usedSpace': 150000000000,
                    'freeSpace': 350000000000,
                    'percentage': 30
                },
                {
                    'letter': 'E:',
                    'name': '娱乐盘',
                    'totalSpace': 250000000000,
                    'usedSpace': 50000000000,
                    'freeSpace': 200000000000,
                    'percentage': 20
                }
            ]
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 设置接口
        elif self.path == '/api/settings':
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'language': 'zh-CN',
                'theme': 'light',
                'autoStart': False,
                'defaultCleanLevel': 'standard',
                'historyRetention': 30
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 快速扫描接口
        elif self.path.startswith('/api/scan/quick'):
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'totalSpace': 135000000000,
                'usedSpace': 100000000000,
                'cleanableSpace': 2500000000,
                'fileTypes': [
                    {'type': '临时文件', 'size': 1000000000, 'percentage': 40},
                    {'type': '浏览器缓存', 'size': 750000000, 'percentage': 30},
                    {'type': '系统日志', 'size': 500000000, 'percentage': 20},
                    {'type': '其他', 'size': 250000000, 'percentage': 10}
                ]
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 深度扫描接口
        elif self.path.startswith('/api/scan/deep'):
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'totalSpace': 135000000000,
                'usedSpace': 100000000000,
                'cleanableSpace': 5000000000,
                'fileTypes': [
                    {'type': '临时文件', 'size': 2000000000, 'percentage': 40},
                    {'type': '浏览器缓存', 'size': 1500000000, 'percentage': 30},
                    {'type': '系统日志', 'size': 1000000000, 'percentage': 20},
                    {'type': '其他', 'size': 500000000, 'percentage': 10}
                ],
                'files': [
                    {'path': 'C:\\Temp\\temp1.txt', 'size': 1000000, 'lastModified': '2026-03-28T10:00:00Z', 'type': '临时文件'},
                    {'path': 'C:\\Temp\\temp2.txt', 'size': 2000000, 'lastModified': '2026-03-27T15:00:00Z', 'type': '临时文件'},
                    {'path': 'C:\\Cache\\cache1.dat', 'size': 1500000, 'lastModified': '2026-03-26T09:00:00Z', 'type': '浏览器缓存'},
                    {'path': 'C:\\Logs\\log1.log', 'size': 800000, 'lastModified': '2026-03-25T14:00:00Z', 'type': '系统日志'}
                ]
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 智能分析接口
        elif self.path.startswith('/api/scan/analysis'):
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'usageFrequency': [
                    {'range': '1天内', 'percentage': 10},
                    {'range': '1-7天', 'percentage': 20},
                    {'range': '7-30天', 'percentage': 30},
                    {'range': '30天以上', 'percentage': 40}
                ],
                'suggestions': [
                    '清理临时文件',
                    '清理浏览器缓存',
                    '清理系统日志',
                    '卸载不常用的应用程序'
                ],
                'estimatedSpaceSaved': 5000000000
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 空间使用情况接口
        elif self.path.startswith('/api/space/usage'):
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'totalSpace': 135000000000,
                'usedSpace': 100000000000,
                'freeSpace': 35000000000,
                'fileTypes': [
                    {'type': '文档', 'size': 10000000000, 'percentage': 10},
                    {'type': '图片', 'size': 5000000000, 'percentage': 5},
                    {'type': '视频', 'size': 20000000000, 'percentage': 20},
                    {'type': '应用程序', 'size': 30000000000, 'percentage': 30},
                    {'type': '其他', 'size': 35000000000, 'percentage': 35}
                ],
                'largeFiles': [
                    {'path': 'C:\\Program Files\\App1\\app1.exe', 'size': 5000000000},
                    {'path': 'C:\\Videos\\movie.mp4', 'size': 4000000000},
                    {'path': 'C:\\Program Files\\App2\\app2.exe', 'size': 3000000000}
                ]
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 可恢复文件扫描接口
        elif self.path == '/api/recovery/scan':
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = [
                {'id': '1', 'name': 'document.txt', 'size': 1000000, 'deletedTime': '2026-03-28T10:00:00Z', 'path': 'C:\\Documents\\document.txt'},
                {'id': '2', 'name': 'image.jpg', 'size': 2000000, 'deletedTime': '2026-03-27T15:00:00Z', 'path': 'C:\\Pictures\\image.jpg'},
                {'id': '3', 'name': 'file.pdf', 'size': 3000000, 'deletedTime': '2026-03-26T09:00:00Z', 'path': 'C:\\Documents\\file.pdf'}
            ]
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 启动项管理接口
        elif self.path == '/api/optimization/startup':
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = [
                {'id': '1', 'name': 'App1', 'enabled': True, 'path': 'C:\\Program Files\\App1\\app1.exe'},
                {'id': '2', 'name': 'App2', 'enabled': False, 'path': 'C:\\Program Files\\App2\\app2.exe'},
                {'id': '3', 'name': 'App3', 'enabled': True, 'path': 'C:\\Program Files\\App3\\app3.exe'}
            ]
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 清理历史接口
        elif self.path == '/api/history':
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = [
                {'id': '1', 'timestamp': '2026-03-29T10:00:00Z', 'disk': 'C:', 'cleanType': '快速清理', 'spaceSaved': 2500000000, 'filesDeleted': 100},
                {'id': '2', 'timestamp': '2026-03-28T15:00:00Z', 'disk': 'C:', 'cleanType': '深度清理', 'spaceSaved': 5000000000, 'filesDeleted': 200},
                {'id': '3', 'timestamp': '2026-03-27T09:00:00Z', 'disk': 'D:', 'cleanType': '快速清理', 'spaceSaved': 1000000000, 'filesDeleted': 50}
            ]
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 根路径返回HTML页面
        elif self.path == '/':
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = '''
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
                <p>服务运行在 http://localhost:5002</p>
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
              </body>
            </html>
            '''
            self.wfile.write(html.encode('utf-8'))
            return
        
        # 404 处理
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'success': False,
                'message': '接口不存在'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
    
    def do_POST(self):
        # 处理CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
        # 保存设置接口
        if self.path == '/api/settings':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            settings = json.loads(post_data.decode('utf-8'))
            
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'success': True,
                'message': '设置保存成功',
                'settings': settings
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 执行清理接口
        elif self.path == '/api/clean/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'success': True,
                'spaceSaved': 2500000000,
                'filesDeleted': len(data.get('files', []))
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 设置自动清理接口
        elif self.path == '/api/clean/auto':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            settings = json.loads(post_data.decode('utf-8'))
            
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'success': True
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 恢复文件接口
        elif self.path.startswith('/api/recovery/recover/'):
            file_id = self.path.split('/')[-1]
            
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'success': True
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 启用/禁用启动项接口
        elif self.path == '/api/optimization/startup/toggle':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'success': True
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 清理注册表接口
        elif self.path == '/api/optimization/registry':
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'success': True,
                'itemsCleaned': 50,
                'spaceSaved': 100000000
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # 404 处理
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'success': False,
                'message': '接口不存在'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

with socketserver.TCPServer(('', PORT), MyHTTPRequestHandler) as httpd:
    print(f'Server running at http://localhost:{PORT}')
    httpd.serve_forever()