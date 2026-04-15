from flask import Blueprint, jsonify

# 创建蓝图
disk_bp = Blueprint('disk', __name__)

# 模拟磁盘数据
disks = [
    {
        'letter': 'C:',
        'name': '系统盘',
        'totalSpace': 1000000000000,
        'usedSpace': 600000000000,
        'freeSpace': 400000000000,
        'healthStatus': 'healthy'
    },
    {
        'letter': 'D:',
        'name': '数据盘',
        'totalSpace': 2000000000000,
        'usedSpace': 1200000000000,
        'freeSpace': 800000000000,
        'healthStatus': 'healthy'
    },
    {
        'letter': 'E:',
        'name': '备份盘',
        'totalSpace': 1500000000000,
        'usedSpace': 1300000000000,
        'freeSpace': 200000000000,
        'healthStatus': 'warning'
    }
]

@disk_bp.route('/api/disks', methods=['GET'])
def get_disks():
    """获取所有磁盘信息"""
    return jsonify({'success': True, 'data': disks})

@disk_bp.route('/api/disks/<disk_letter>', methods=['GET'])
def get_disk_info(disk_letter):
    """获取指定磁盘信息"""
    disk = next((d for d in disks if d['letter'] == disk_letter), None)
    if disk:
        return jsonify({'success': True, 'data': disk})
    else:
        return jsonify({'success': False, 'error': 'Disk not found'})

# 注册蓝图
from app import app
app.register_blueprint(disk_bp)