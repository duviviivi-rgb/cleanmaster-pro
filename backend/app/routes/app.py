from flask import Blueprint, request, jsonify
import time

bp = Blueprint('app', __name__, url_prefix='/api')

@bp.route('/app/scan', methods=['POST'])
def scan_apps():
    """扫描应用程序"""
    try:
        # 模拟扫描应用过程
        time.sleep(2)  # 模拟扫描延迟
        
        # 模拟应用列表
        apps = [
            {"id": "1", "name": "Google Chrome", "version": "123.0.6312.105", "publisher": "Google LLC", "installDate": "2026-03-15", "size": 1500000000, "status": "healthy", "recommendation": "keep"},
            {"id": "2", "name": "Discord", "version": "0.0.306", "publisher": "Discord Inc.", "installDate": "2026-02-20", "size": 800000000, "status": "healthy", "recommendation": "keep"},
            {"id": "3", "name": "Steam", "version": "1669807911", "publisher": "Valve Corporation", "installDate": "2026-01-10", "size": 2000000000, "status": "healthy", "recommendation": "keep"},
            {"id": "4", "name": "Microsoft Office", "version": "2021", "publisher": "Microsoft Corporation", "installDate": "2025-12-01", "size": 3000000000, "status": "healthy", "recommendation": "keep"},
            {"id": "5", "name": "Old App", "version": "1.0.0", "publisher": "Unknown", "installDate": "2025-06-15", "size": 500000000, "status": "dormant", "recommendation": "remove"},
            {"id": "6", "name": "Broken App", "version": "2.0.0", "publisher": "Unknown", "installDate": "2025-08-20", "size": 300000000, "status": "broken", "recommendation": "remove"},
        ]
        
        return jsonify({
            "success": True,
            "data": apps
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/app/uninstall', methods=['POST'])
def uninstall_app():
    """卸载应用程序"""
    try:
        data = request.json
        app_ids = data.get('app_ids', [])
        
        # 模拟卸载过程
        time.sleep(3)  # 模拟卸载延迟
        
        # 模拟卸载结果
        uninstall_result = {
            "apps_uninstalled": len(app_ids),
            "space_freed": 800000000,
            "duration": 60,
            "uninstalled_apps": app_ids
        }
        
        return jsonify({
            "success": True,
            "data": uninstall_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/app/detail/<app_id>', methods=['GET'])
def get_app_detail(app_id):
    """获取应用详细信息"""
    try:
        # 模拟应用详细信息
        app_detail = {
            "id": app_id,
            "name": "Google Chrome",
            "version": "123.0.6312.105",
            "publisher": "Google LLC",
            "installDate": "2026-03-15",
            "size": 1500000000,
            "status": "healthy",
            "recommendation": "keep",
            "location": "C:\\Program Files\\Google\\Chrome\\Application",
            "startup": True,
            "permissions": ["Internet Access", "File System Access", "Camera Access"],
            "related_files": ["C:\\Users\\User\\AppData\\Local\\Google\\Chrome"],
            "update_date": "2026-04-10"
        }
        
        return jsonify({
            "success": True,
            "data": app_detail
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
