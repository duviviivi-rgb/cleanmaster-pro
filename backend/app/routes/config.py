from flask import Blueprint, request, jsonify
import json
import os

bp = Blueprint('config', __name__, url_prefix='/api')

# 配置文件路径
CONFIG_FILE = os.path.join(os.getcwd(), 'config.json')

# 默认配置
DEFAULT_CONFIG = {
    "user_preferences": {
        "default_output_format": "html",
        "default_template": "standard",
        "output_path": os.path.join(os.getcwd(), 'reports'),
        "auto_save": True,
        "show_preview": True
    },
    "extraction_rules": {
        "material_keywords": [
            '钢管', '管道', '电缆', '风管', '阀门', '设备',
            '钢板', '型材', '管件', '配件', '支架', '法兰',
            '螺栓', '螺母', '垫片', '密封件', '保温材料', '防火材料'
        ],
        "model_patterns": [
            r'DN\d+',  # 公称直径
            r'\d+mm',  # 毫米单位
            r'\d+x\d+',  # 尺寸
            r'YJV-\d+x\d+',  # 电缆型号
            r'\w+-\w+',  # 通用型号格式
            r'\d+\.\d+'  # 小数
        ],
        "quantity_patterns": [
            r'\d+\s*m',  # 米
            r'\d+\s*m²',  # 平方米
            r'\d+\s*个',  # 个
            r'\d+\s*套',  # 套
            r'\d+\s*件',  # 件
            r'\d+\s*根',  # 根
            r'\d+\s*条',  # 条
            r'\d+\s*只'  # 只
        ]
    },
    "report_templates": [
        {
            "id": 1,
            "name": "标准模板",
            "description": "包含所有材料信息的标准报告模板"
        },
        {
            "id": 2,
            "name": "简洁模板",
            "description": "只包含关键信息的简洁报告模板"
        },
        {
            "id": 3,
            "name": "详细模板",
            "description": "包含详细材料信息和检查内容的报告模板"
        }
    ]
}

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return DEFAULT_CONFIG
    else:
        # 保存默认配置
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    """保存配置"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置文件失败: {e}")
        return False

@bp.route('/config', methods=['GET'])
def get_config():
    """获取配置信息"""
    try:
        data = request.json
        key = data.get('key', '')
        
        config = load_config()
        
        if key:
            # 获取指定配置
            value = config.get(key, {})
            return jsonify({
                "success": True,
                "data": value
            })
        else:
            # 获取所有配置
            return jsonify({
                "success": True,
                "data": config
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@bp.route('/config', methods=['POST'])
def set_config():
    """设置配置信息"""
    try:
        data = request.json
        key = data.get('key', '')
        value = data.get('value', {})
        
        if not key:
            return jsonify({
                "success": False,
                "error": "请提供配置键"
            })
        
        config = load_config()
        config[key] = value
        
        if save_config(config):
            return jsonify({
                "success": True
            })
        else:
            return jsonify({
                "success": False,
                "error": "保存配置失败"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
