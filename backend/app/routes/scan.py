from flask import Blueprint, request, jsonify
import time

bp = Blueprint('scan', __name__, url_prefix='/api')

@bp.route('/scan/start', methods=['POST'])
def start_scan():
    """开始扫描"""
    try:
        data = request.json
        disk = data.get('disk', 'C:')
        scan_type = data.get('scan_type', 'quick')  # quick, deep, intelligent
        
        # 模拟扫描过程
        time.sleep(2)  # 模拟扫描延迟
        
        # 模拟扫描结果
        scan_result = {
            "disk": disk,
            "scan_type": scan_type,
            "duration": 120,
            "files_scanned": 15000,
            "junk_files": [
                {"path": "C:\\Windows\\Temp", "size": 5000000000, "type": "临时文件"},
                {"path": "C:\\Users\\User\\AppData\\Local\\Temp", "size": 3000000000, "type": "临时文件"},
                {"path": "C:\\Users\\User\\Downloads", "size": 10000000000, "type": "下载文件"},
                {"path": "C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache", "size": 2000000000, "type": "浏览器缓存"},
                {"path": "C:\\Users\\User\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\*.default\\cache", "size": 1500000000, "type": "浏览器缓存"}
            ],
            "total_junk_size": 21500000000
        }
        
        return jsonify({
            "success": True,
            "data": scan_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/scan/status', methods=['GET'])
def get_scan_status():
    """获取扫描状态"""
    try:
        # 模拟扫描状态
        status = {
            "is_scanning": False,
            "progress": 100,
            "current_file": "完成",
            "estimated_time": 0
        }
        
        return jsonify({
            "success": True,
            "data": status
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/scan/stop', methods=['POST'])
def stop_scan():
    """停止扫描"""
    try:
        # 模拟停止扫描
        time.sleep(1)
        
        return jsonify({
            "success": True,
            "message": "扫描已停止"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
