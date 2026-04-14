from flask import Blueprint, jsonify
import os

bp = Blueprint('disk', __name__, url_prefix='/api')

@bp.route('/disks', methods=['GET'])
def get_disks():
    """获取磁盘信息"""
    try:
        # 模拟磁盘数据
        disks = [
            {"letter": "C:", "name": "系统盘", "totalSpace": 1000000000000, "usedSpace": 600000000000, "healthStatus": "healthy"},
            {"letter": "D:", "name": "数据盘", "totalSpace": 2000000000000, "usedSpace": 1200000000000, "healthStatus": "healthy"},
            {"letter": "E:", "name": "娱乐盘", "totalSpace": 1500000000000, "usedSpace": 800000000000, "healthStatus": "warning"},
        ]
        
        return jsonify({
            "success": True,
            "data": disks
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/disk/<letter>', methods=['GET'])
def get_disk_detail(letter):
    """获取磁盘详细信息"""
    try:
        # 模拟磁盘详细数据
        disk_detail = {
            "letter": letter,
            "name": "系统盘" if letter == "C:" else "数据盘" if letter == "D:" else "娱乐盘",
            "totalSpace": 1000000000000 if letter == "C:" else 2000000000000 if letter == "D:" else 1500000000000,
            "usedSpace": 600000000000 if letter == "C:" else 1200000000000 if letter == "D:" else 800000000000,
            "healthStatus": "healthy" if letter in ["C:", "D:"] else "warning",
            "fileTypes": [
                {"type": "文档", "count": 120, "size": 5000000000},
                {"type": "图片", "count": 500, "size": 10000000000},
                {"type": "视频", "count": 50, "size": 20000000000},
                {"type": "音频", "count": 200, "size": 2000000000},
                {"type": "应用", "count": 30, "size": 15000000000},
                {"type": "其他", "count": 800, "size": 8000000000}
            ]
        }
        
        return jsonify({
            "success": True,
            "data": disk_detail
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
