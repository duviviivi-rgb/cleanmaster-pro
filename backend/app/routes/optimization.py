from flask import Blueprint, jsonify, request

# 创建蓝图
optimization_bp = Blueprint('optimization', __name__)

# 模拟系统状态数据
system_status = {
    'cpuUsage': 35,
    'memoryUsage': 48,
    'diskUsage': 60,
    'bootTime': '2026-04-14 08:30:00',
    'upTime': '5小时30分钟'
}

# 模拟启动项数据
startup_items = [
    { 'id': '1', 'name': 'Google Chrome', 'publisher': 'Google LLC', 'enabled': True, 'impact': 'low', 'recommendation': 'keep' },
    { 'id': '2', 'name': 'Discord', 'publisher': 'Discord Inc.', 'enabled': True, 'impact': 'low', 'recommendation': 'keep' },
    { 'id': '3', 'name': 'Steam', 'publisher': 'Valve Corporation', 'enabled': False, 'impact': 'medium', 'recommendation': 'disable' },
    { 'id': '4', 'name': 'Microsoft OneDrive', 'publisher': 'Microsoft Corporation', 'enabled': True, 'impact': 'medium', 'recommendation': 'keep' },
    { 'id': '5', 'name': 'Old App', 'publisher': 'Unknown', 'enabled': True, 'impact': 'high', 'recommendation': 'disable' },
]

# 模拟服务数据
services = [
    { 'id': '1', 'name': 'Windows Update', 'status': 'running', 'startupType': 'automatic', 'impact': 'low', 'recommendation': 'keep' },
    { 'id': '2', 'name': 'Windows Defender', 'status': 'running', 'startupType': 'automatic', 'impact': 'medium', 'recommendation': 'keep' },
    { 'id': '3', 'name': 'Print Spooler', 'status': 'stopped', 'startupType': 'manual', 'impact': 'low', 'recommendation': 'keep' },
    { 'id': '4', 'name': 'Windows Search', 'status': 'running', 'startupType': 'automatic', 'impact': 'medium', 'recommendation': 'keep' },
    { 'id': '5', 'name': 'Old Service', 'status': 'running', 'startupType': 'automatic', 'impact': 'high', 'recommendation': 'disable' },
]

@optimization_bp.route('/api/optimization/status', methods=['GET'])
def get_system_status():
    """获取系统状态"""
    return jsonify({'success': True, 'data': system_status})

@optimization_bp.route('/api/optimization/startup', methods=['GET'])
def get_startup_items():
    """获取启动项"""
    return jsonify({'success': True, 'data': startup_items})

@optimization_bp.route('/api/optimization/startup/toggle', methods=['POST'])
def toggle_startup_item():
    """切换启动项状态"""
    data = request.json
    item_id = data.get('id')
    enabled = data.get('enabled')
    
    # 这里可以添加实际的启动项状态切换逻辑
    
    return jsonify({'success': True, 'message': '启动项状态已更新'})

@optimization_bp.route('/api/optimization/services', methods=['GET'])
def get_services():
    """获取服务"""
    return jsonify({'success': True, 'data': services})

@optimization_bp.route('/api/optimization/services/toggle', methods=['POST'])
def toggle_service():
    """切换服务状态"""
    data = request.json
    service_id = data.get('id')
    status = data.get('status')
    
    # 这里可以添加实际的服务状态切换逻辑
    
    return jsonify({'success': True, 'message': '服务状态已更新'})

@optimization_bp.route('/api/optimization/defrag', methods=['POST'])
def defrag_disk():
    """磁盘碎片整理"""
    data = request.json
    disk = data.get('disk', 'C:')
    
    # 这里可以添加实际的磁盘碎片整理逻辑
    
    return jsonify({'success': True, 'message': '磁盘碎片整理已开始'})

# 注册蓝图
from app import app
app.register_blueprint(optimization_bp)