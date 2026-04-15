from backend.app import app

# Vercel 无服务器函数入口点
def handler(event, context):
    # 导入必要的模块
    from flask import Flask, request as flask_request
    import werkzeug
    
    # 构建 Flask 环境
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    headers = event.get('headers', {})
    body = event.get('body', '')
    
    environ = werkzeug.datastructures.EnvironBuilder(
        path=path,
        method=method,
        headers=list(headers.items()),
        data=body,
        environ_base={
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': body,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': True,
        }
    ).get_environ()
    
    # 处理请求
    response = app(environ, lambda status, headers: [status, headers])
    
    # 构建响应
    return {
        'statusCode': int(response[0].split()[0]),
        'headers': dict(response[1]),
        'body': response[2][0].decode('utf-8') if response[2] else ''
    }
