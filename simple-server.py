import http.server
import socketserver
import json

PORT = 5050

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 处理CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
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
        elif self.path == '/api/scan/quick':
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
                <p>服务运行在 http://localhost:5009</p>
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
        self.send_header('Access-Control-Allow-Origin', '*')
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
