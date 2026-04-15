from flask import Blueprint, jsonify, request

# 创建蓝图
history_bp = Blueprint('history', __name__)

# 模拟清理历史数据
clean_history = [
    { 'id': '1', 'timestamp': '2026-04-10 14:30', 'disk': 'C:', 'cleanType': '快速扫描', 'spaceSaved': 25000000000, 'filesDeleted': 3200, 'duration': 60 },
    { 'id': '2', 'timestamp': '2026-04-09 09:15', 'disk': 'C:', 'cleanType': '深度扫描', 'spaceSaved': 42000000000, 'filesDeleted': 5800, 'duration': 120 },
    { 'id': '3', 'timestamp': '2026-04-08 18:45', 'disk': 'D:', 'cleanType': '智能分析', 'spaceSaved': 31000000000, 'filesDeleted': 4500, 'duration': 90 },
    { 'id': '4', 'timestamp': '2026-04-07 12:00', 'disk': 'C:', 'cleanType': '快速扫描', 'spaceSaved': 18000000000, 'filesDeleted': 2500, 'duration': 45 },
    { 'id': '5', 'timestamp': '2026-04-06 10:30', 'disk': 'E:', 'cleanType': '深度扫描', 'spaceSaved': 56000000000, 'filesDeleted': 7200, 'duration': 150 },
]

# 模拟分析数据
analysis = {
    'totalSpaceSaved': 172000000000,
    'averageCleanTime': 93,
    'mostCleanedType': '深度扫描',
    'totalCleanings': 5,
    'weeklyTrend': [15, 22, 18, 25, 30, 28, 22]
}

@history_bp.route('/api/history', methods=['GET'])
def get_history():
    """获取清理历史"""
    return jsonify({'success': True, 'data': clean_history})

@history_bp.route('/api/history/analysis', methods=['GET'])
def get_history_analysis():
    """获取历史分析"""
    return jsonify({'success': True, 'data': analysis})

@history_bp.route('/api/history/delete/<history_id>', methods=['DELETE'])
def delete_history(history_id):
    """删除历史记录"""
    # 这里可以添加实际的历史记录删除逻辑
    
    return jsonify({'success': True, 'message': '历史记录删除成功'})

@history_bp.route('/api/history/clear', methods=['POST'])
def clear_history():
    """清空历史记录"""
    # 这里可以添加实际的历史记录清空逻辑
    
    return jsonify({'success': True, 'message': '历史记录已清空'})

# 注册蓝图
from app import app
app.register_blueprint(history_bp)