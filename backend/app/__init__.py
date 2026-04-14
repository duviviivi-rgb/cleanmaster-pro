from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 注册路由
from app.routes import disk, scan, clean, space, app as app_route, governance, history, optimization, recovery

app.register_blueprint(disk.bp)
app.register_blueprint(scan.bp)
app.register_blueprint(clean.bp)
app.register_blueprint(space.bp)
app.register_blueprint(app_route.bp)
app.register_blueprint(governance.bp)
app.register_blueprint(history.bp)
app.register_blueprint(optimization.bp)
app.register_blueprint(recovery.bp)
