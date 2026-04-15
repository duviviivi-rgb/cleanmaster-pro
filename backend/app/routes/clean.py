from flask import Blueprint, jsonify, request

# 创建蓝图
clean_bp = Blueprint('clean', __name__)

# 模拟清理状态
clean_status = {
    'is_cleaning': False,
    'progress': 0,
    'result': None
}

@clean_bp.route('/api/clean/start', methods=['POST'])
def start_clean():
    """开始清理"""
    data = request.json
    disk = data.get('disk')
    files = data.get('files', [])
    
    # 模拟清理过程
    clean_status['is_cleaning'] = True
    clean_status['progress'] = 0
    clean_status['result'] = None
    
    # 这里可以添加实际的清理逻辑
    
    return jsonify({'success': True, 'message': '清理已开始'})

@clean_bp.route('/api/clean/status', methods=['GET'])
def get_clean_status():
    """获取清理状态"""
    # 模拟清理进度
    if clean_status['is_cleaning']:
        clean_status['progress'] += 15
        if clean_status['progress'] >= 100:
            clean_status['is_cleaning'] = False
            clean_status['progress'] = 100
            # 模拟清理结果
            clean_status['result'] = {
                'filesDeleted': 2800,
                'spaceSaved': 22000000000
            }
    
    return jsonify({
        'success': True,
        'data': {
            'is_cleaning': clean_status['is_cleaning'],
            'progress': clean_status['progress'],
            'result': clean_status['result']
        }
    })

@clean_bp.route('/api/clean/stop', methods=['POST'])
def stop_clean():
    """停止清理"""
    clean_status['is_cleaning'] = False
    clean_status['progress'] = 0
    clean_status['result'] = None
    
    return jsonify({'success': True, 'message': '清理已停止'})

@clean_bp.route('/api/clean/auto', methods=['POST'])
def set_auto_clean():
    """设置自动清理"""
    data = request.json
    enabled = data.get('enabled', False)
    schedule = data.get('schedule', 'daily')
    
    # 这里可以添加实际的自动清理设置逻辑
    
    return jsonify({'success': True, 'message': '自动清理设置已更新'})

# 注册蓝图
from app import app
app.register_blueprint(clean_bp)