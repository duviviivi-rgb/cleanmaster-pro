from flask import Blueprint, jsonify, request

# 创建蓝图
recovery_bp = Blueprint('recovery', __name__)

# 模拟可恢复文件数据
recoverable_files = [
    { 'id': '1', 'name': 'document.docx', 'path': 'C:\Documents\document.docx', 'size': 2000000, 'deletedDate': '2026-04-10 14:30', 'recoveryChance': 'high' },
    { 'id': '2', 'name': 'photo.jpg', 'path': 'C:\Pictures\photo.jpg', 'size': 5000000, 'deletedDate': '2026-04-09 09:15', 'recoveryChance': 'medium' },
    { 'id': '3', 'name': 'video.mp4', 'path': 'C:\Videos\video.mp4', 'size': 50000000, 'deletedDate': '2026-04-08 18:45', 'recoveryChance': 'low' },
    { 'id': '4', 'name': 'spreadsheet.xlsx', 'path': 'C:\Documents\spreadsheet.xlsx', 'size': 1500000, 'deletedDate': '2026-04-07 12:00', 'recoveryChance': 'high' },
    { 'id': '5', 'name': 'presentation.pptx', 'path': 'C:\Documents\presentation.pptx', 'size': 3000000, 'deletedDate': '2026-04-06 10:30', 'recoveryChance': 'medium' },
]

# 模拟扫描状态
scan_status = {
    'is_scanning': False,
    'progress': 0,
    'result': None
}

# 模拟恢复状态
recovery_status = {
    'is_recovering': False,
    'progress': 0,
    'result': None
}

@recovery_bp.route('/api/recovery/scan', methods=['POST'])
def scan_recoverable_files():
    """扫描可恢复文件"""
    data = request.json
    disk = data.get('disk', 'C:')
    
    # 模拟扫描过程
    scan_status['is_scanning'] = True
    scan_status['progress'] = 0
    scan_status['result'] = None
    
    # 这里可以添加实际的文件恢复扫描逻辑
    
    return jsonify({'success': True, 'message': '文件恢复扫描已开始'})

@recovery_bp.route('/api/recovery/scan/status', methods=['GET'])
def get_scan_status():
    """获取扫描状态"""
    # 模拟扫描进度
    if scan_status['is_scanning']:
        scan_status['progress'] += 10
        if scan_status['progress'] >= 100:
            scan_status['is_scanning'] = False
            scan_status['progress'] = 100
            scan_status['result'] = recoverable_files
    
    return jsonify({
        'success': True,
        'data': {
            'is_scanning': scan_status['is_scanning'],
            'progress': scan_status['progress'],
            'result': scan_status['result']
        }
    })

@recovery_bp.route('/api/recovery/start', methods=['POST'])
def start_recovery():
    """开始恢复文件"""
    data = request.json
    files = data.get('files', [])
    destination = data.get('destination', 'C:\Recovery')
    
    # 模拟恢复过程
    recovery_status['is_recovering'] = True
    recovery_status['progress'] = 0
    recovery_status['result'] = None
    
    # 这里可以添加实际的文件恢复逻辑
    
    return jsonify({'success': True, 'message': '文件恢复已开始'})

@recovery_bp.route('/api/recovery/status', methods=['GET'])
def get_recovery_status():
    """获取恢复状态"""
    # 模拟恢复进度
    if recovery_status['is_recovering']:
        recovery_status['progress'] += 20
        if recovery_status['progress'] >= 100:
            recovery_status['is_recovering'] = False
            recovery_status['progress'] = 100
            recovery_status['result'] = {
                'recoveredFiles': 3,
                'failedFiles': 2,
                'destination': 'C:\Recovery'
            }
    
    return jsonify({
        'success': True,
        'data': {
            'is_recovering': recovery_status['is_recovering'],
            'progress': recovery_status['progress'],
            'result': recovery_status['result']
        }
    })

@recovery_bp.route('/api/recovery/stop', methods=['POST'])
def stop_recovery():
    """停止恢复"""
    recovery_status['is_recovering'] = False
    recovery_status['progress'] = 0
    recovery_status['result'] = None
    
    return jsonify({'success': True, 'message': '文件恢复已停止'})

# 注册蓝图
from app import app
app.register_blueprint(recovery_bp)