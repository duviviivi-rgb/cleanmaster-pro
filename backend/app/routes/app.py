from flask import Blueprint, jsonify, request

# 创建蓝图
app_bp = Blueprint('app', __name__)

# 模拟应用数据
applications = [
    {'id': '1', 'name': 'Google Chrome', 'version': '123.0.6312.105', 'publisher': 'Google LLC', 'installDate': '2026-03-15', 'size': 1500000000, 'status': 'healthy', 'recommendation': 'keep'},
    {'id': '2', 'name': 'Discord', 'version': '0.0.306', 'publisher': 'Discord Inc.', 'installDate': '2026-02-20', 'size': 800000000, 'status': 'healthy', 'recommendation': 'keep'},
    {'id': '3', 'name': 'Steam', 'version': '1669807911', 'publisher': 'Valve Corporation', 'installDate': '2026-01-10', 'size': 2000000000, 'status': 'healthy', 'recommendation': 'keep'},
    {'id': '4', 'name': 'Microsoft Office', 'version': '2021', 'publisher': 'Microsoft Corporation', 'installDate': '2025-12-01', 'size': 3000000000, 'status': 'healthy', 'recommendation': 'keep'},
    {'id': '5', 'name': 'Old App', 'version': '1.0.0', 'publisher': 'Unknown', 'installDate': '2025-06-15', 'size': 500000000, 'status': 'dormant', 'recommendation': 'remove'},
    {'id': '6', 'name': 'Broken App', 'version': '2.0.0', 'publisher': 'Unknown', 'installDate': '2025-08-20', 'size': 300000000, 'status': 'broken', 'recommendation': 'remove'},
]

# 模拟扫描状态
scan_status = {
    'is_scanning': False,
    'progress': 0,
    'result': None
}

@app_bp.route('/api/apps/scan', methods=['POST'])
def scan_apps():
    """扫描应用"""
    # 模拟扫描过程
    scan_status['is_scanning'] = True
    scan_status['progress'] = 0
    scan_status['result'] = None
    
    # 这里可以添加实际的应用扫描逻辑
    
    return jsonify({'success': True, 'message': '应用扫描已开始'})

@app_bp.route('/api/apps/status', methods=['GET'])
def get_app_scan_status():
    """获取应用扫描状态"""
    # 模拟扫描进度
    if scan_status['is_scanning']:
        scan_status['progress'] += 20
        if scan_status['progress'] >= 100:
            scan_status['is_scanning'] = False
            scan_status['progress'] = 100
            scan_status['result'] = applications
    
    return jsonify({
        'success': True,
        'data': {
            'is_scanning': scan_status['is_scanning'],
            'progress': scan_status['progress'],
            'result': scan_status['result']
        }
    })

@app_bp.route('/api/apps', methods=['GET'])
def get_apps():
    """获取应用列表"""
    return jsonify({'success': True, 'data': applications})

@app_bp.route('/api/apps/<app_id>', methods=['GET'])
def get_app_info(app_id):
    """获取应用详细信息"""
    app = next((a for a in applications if a['id'] == app_id), None)
    if app:
        return jsonify({'success': True, 'data': app})
    else:
        return jsonify({'success': False, 'error': 'Application not found'})

@app_bp.route('/api/apps/uninstall', methods=['POST'])
def uninstall_app():
    """卸载应用"""
    data = request.json
    app_id = data.get('app_id')
    
    # 这里可以添加实际的应用卸载逻辑
    
    return jsonify({'success': True, 'message': '应用卸载成功'})

# 注册蓝图
from app import app
app.register_blueprint(app_bp)