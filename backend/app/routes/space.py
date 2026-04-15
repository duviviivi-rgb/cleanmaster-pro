from flask import Blueprint, jsonify, request

# 创建蓝图
space_bp = Blueprint('space', __name__)

# 模拟空间使用数据
space_usage = {
    'totalSpace': 1000000000000,
    'usedSpace': 600000000000,
    'freeSpace': 400000000000,
    'fileTypes': [
        {'type': '文档', 'size': 50000000000, 'percentage': 8.3},
        {'type': '图片', 'size': 100000000000, 'percentage': 16.7},
        {'type': '视频', 'size': 200000000000, 'percentage': 33.3},
        {'type': '音频', 'size': 50000000000, 'percentage': 8.3},
        {'type': '应用', 'size': 150000000000, 'percentage': 25},
        {'type': '其他', 'size': 50000000000, 'percentage': 8.3}
    ],
    'largeFiles': [
        {'name': 'video1.mp4', 'path': 'C:\Videos\video1.mp4', 'size': 20000000000},
        {'name': 'game1.exe', 'path': 'C:\Games\game1.exe', 'size': 15000000000},
        {'name': 'backup.zip', 'path': 'C:\Backup\backup.zip', 'size': 10000000000},
        {'name': 'movie1.mp4', 'path': 'C:\Movies\movie1.mp4', 'size': 8000000000},
        {'name': 'software.iso', 'path': 'C:\Downloads\software.iso', 'size': 5000000000}
    ],
    'duplicateFiles': [
        {
            'groupId': '1',
            'files': ['C:\Documents\file1.docx', 'C:\Downloads\file1_copy.docx'],
            'size': 2000000
        },
        {
            'groupId': '2',
            'files': ['C:\Pictures\photo1.jpg', 'C:\Backup\photo1_copy.jpg'],
            'size': 5000000
        },
        {
            'groupId': '3',
            'files': ['C:\Videos\video1.mp4', 'C:\Movies\video1_copy.mp4'],
            'size': 50000000
        }
    ]
}

@space_bp.route('/api/space/analyze', methods=['POST'])
def analyze_space():
    """分析空间使用情况"""
    data = request.json
    disk = data.get('disk', 'C:')
    
    # 这里可以添加实际的空间分析逻辑
    
    return jsonify({'success': True, 'data': space_usage})

@space_bp.route('/api/space/large-files', methods=['GET'])
def get_large_files():
    """获取大文件"""
    return jsonify({'success': True, 'data': space_usage['largeFiles']})

@space_bp.route('/api/space/duplicate-files', methods=['GET'])
def get_duplicate_files():
    """获取重复文件"""
    return jsonify({'success': True, 'data': space_usage['duplicateFiles']})

# 注册蓝图
from app import app
app.register_blueprint(space_bp)