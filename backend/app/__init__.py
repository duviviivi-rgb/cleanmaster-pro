from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 导入路由
from app.routes import disk, scan, clean, space, app as app_route, governance, history, optimization, recovery

if __name__ == '__main__':
    app.run(debug=True)