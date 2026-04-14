from flask import Blueprint, request, jsonify

bp = Blueprint('history', __name__, url_prefix='/api')

@bp.route('/history', methods=['GET'])
def get_history():
    """获取清理历史记录"""
    try:
        # 模拟历史记录
        history = [
            {
                "id": "1",
                "timestamp": "2026-04-10 14:30",
                "disk": "C:",
                "cleanType": "快速扫描",
                "spaceSaved": 25000000000,
                "filesDeleted": 3200,
                "duration": 60
            },
            {
                "id": "2",
                "timestamp": "2026-04-09 09:15",
                "disk": "C:",
                "cleanType": "深度扫描",
                "spaceSaved": 42000000000,
                "filesDeleted": 5800,
                "duration": 120
            },
            {
                "id": "3",
                "timestamp": "2026-04-08 18:45",
                "disk": "D:",
                "cleanType": "智能分析",
                "spaceSaved": 31000000000,
                "filesDeleted": 4500,
                "duration": 90
            },
            {
                "id": "4",
                "timestamp": "2026-04-07 12:00",
                "disk": "C:",
                "cleanType": "快速扫描",
                "spaceSaved": 18000000000,
                "filesDeleted": 2500,
                "duration": 45
            },
            {
                "id": "5",
                "timestamp": "2026-04-06 10:30",
                "disk": "E:",
                "cleanType": "深度扫描",
                "spaceSaved": 56000000000,
                "filesDeleted": 7200,
                "duration": 150
            }
        ]
        
        return jsonify({
            "success": True,
            "data": history
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/history/analysis', methods=['GET'])
def get_history_analysis():
    """获取清理历史分析"""
    try:
        # 模拟历史分析
        analysis = {
            "totalSpaceSaved": 172000000000,
            "averageCleanTime": 93,
            "mostCleanedType": "深度扫描",
            "totalCleanings": 5,
            "mostActiveDay": "Monday",
            "spaceSavedPerMonth": {
                "January": 30000000000,
                "February": 45000000000,
                "March": 55000000000,
                "April": 42000000000
            }
        }
        
        return jsonify({
            "success": True,
            "data": analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/history/<id>', methods=['DELETE'])
def delete_history(id):
    """删除历史记录"""
    try:
        # 模拟删除历史记录
        
        return jsonify({
            "success": True,
            "message": "历史记录删除成功"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/history/clear', methods=['POST'])
def clear_history():
    """清空历史记录"""
    try:
        # 模拟清空历史记录
        
        return jsonify({
            "success": True,
            "message": "历史记录清空成功"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
