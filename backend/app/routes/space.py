from flask import Blueprint, request, jsonify

bp = Blueprint('space', __name__, url_prefix='/api')

@bp.route('/space/analyze', methods=['POST'])
def analyze_space():
    """分析空间使用情况"""
    try:
        data = request.json
        disk = data.get('disk', 'C:')
        
        # 模拟空间分析结果
        analysis_result = {
            "disk": disk,
            "totalSpace": 1000000000000,
            "usedSpace": 600000000000,
            "freeSpace": 400000000000,
            "spaceUsage": [
                {"category": "系统文件", "size": 200000000000, "percentage": 20},
                {"category": "应用程序", "size": 150000000000, "percentage": 15},
                {"category": "文档", "size": 50000000000, "percentage": 5},
                {"category": "图片", "size": 100000000000, "percentage": 10},
                {"category": "视频", "size": 200000000000, "percentage": 20},
                {"category": "其他", "size": 100000000000, "percentage": 10}
            ],
            "large_files": [
                {"path": "C:\\Movies\\movie1.mp4", "size": 5000000000, "last_modified": "2026-04-01"},
                {"path": "C:\\Games\\game1.exe", "size": 3000000000, "last_modified": "2026-03-15"},
                {"path": "C:\\Downloads\\software1.iso", "size": 4500000000, "last_modified": "2026-04-10"},
                {"path": "C:\\Documents\\backup1.zip", "size": 2500000000, "last_modified": "2026-03-20"},
                {"path": "C:\\Music\\album1.flac", "size": 1500000000, "last_modified": "2026-02-15"}
            ],
            "duplicate_files": [
                {
                    "group_id": "1",
                    "files": [
                        "C:\\Documents\\file1.docx",
                        "C:\\Downloads\\file1_copy.docx"
                    ],
                    "size": 2000000
                },
                {
                    "group_id": "2",
                    "files": [
                        "C:\\Pictures\\photo1.jpg",
                        "C:\\Backup\\photo1_copy.jpg"
                    ],
                    "size": 5000000
                }
            ]
        }
        
        return jsonify({
            "success": True,
            "data": analysis_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/space/large-files', methods=['GET'])
def get_large_files():
    """获取大文件列表"""
    try:
        disk = request.args.get('disk', 'C:')
        min_size = request.args.get('min_size', 1000000000)  # 默认1GB
        
        # 模拟大文件列表
        large_files = [
            {"path": "C:\\Movies\\movie1.mp4", "size": 5000000000, "last_modified": "2026-04-01"},
            {"path": "C:\\Games\\game1.exe", "size": 3000000000, "last_modified": "2026-03-15"},
            {"path": "C:\\Downloads\\software1.iso", "size": 4500000000, "last_modified": "2026-04-10"},
            {"path": "C:\\Documents\\backup1.zip", "size": 2500000000, "last_modified": "2026-03-20"},
            {"path": "C:\\Music\\album1.flac", "size": 1500000000, "last_modified": "2026-02-15"}
        ]
        
        return jsonify({
            "success": True,
            "data": large_files
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/space/duplicate-files', methods=['GET'])
def get_duplicate_files():
    """获取重复文件列表"""
    try:
        disk = request.args.get('disk', 'C:')
        
        # 模拟重复文件列表
        duplicate_files = [
            {
                "group_id": "1",
                "files": [
                    "C:\\Documents\\file1.docx",
                    "C:\\Downloads\\file1_copy.docx"
                ],
                "size": 2000000
            },
            {
                "group_id": "2",
                "files": [
                    "C:\\Pictures\\photo1.jpg",
                    "C:\\Backup\\photo1_copy.jpg"
                ],
                "size": 5000000
            },
            {
                "group_id": "3",
                "files": [
                    "C:\\Videos\\video1.mp4",
                    "C:\\Movies\\video1_copy.mp4"
                ],
                "size": 50000000
            }
        ]
        
        return jsonify({
            "success": True,
            "data": duplicate_files
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
