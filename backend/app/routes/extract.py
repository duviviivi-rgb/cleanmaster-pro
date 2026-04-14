from flask import Blueprint, request, jsonify
import re

bp = Blueprint('extract', __name__, url_prefix='/api')

# 材料关键词列表
MATERIAL_KEYWORDS = [
    '钢管', '管道', '电缆', '风管', '阀门', '设备',
    '钢板', '型材', '管件', '配件', '支架', '法兰',
    '螺栓', '螺母', '垫片', '密封件', '保温材料', '防火材料'
]

# 型号模式
MODEL_PATTERNS = [
    r'DN\d+',  # 公称直径
    r'\d+mm',  # 毫米单位
    r'\d+x\d+',  # 尺寸
    r'YJV-\d+x\d+',  # 电缆型号
    r'\w+-\w+',  # 通用型号格式
    r'\d+\.\d+'  # 小数
]

# 数量模式
QUANTITY_PATTERNS = [
    r'\d+\s*m',  # 米
    r'\d+\s*m²',  # 平方米
    r'\d+\s*个',  # 个
    r'\d+\s*套',  # 套
    r'\d+\s*件',  # 件
    r'\d+\s*根',  # 根
    r'\d+\s*条',  # 条
    r'\d+\s*只'  # 只
]

def extract_material_name(text):
    """提取材料名称"""
    for keyword in MATERIAL_KEYWORDS:
        if keyword in text:
            return keyword
    return "未知材料"

def extract_model(text):
    """提取型号"""
    for pattern in MODEL_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return ""

def extract_quantity(text):
    """提取数量"""
    for pattern in QUANTITY_PATTERNS:
        match = re.search(pattern, text)
        if match:
            # 提取数字部分
            num_match = re.search(r'\d+', match.group())
            if num_match:
                return float(num_match.group())
    return 1

def extract_unit(text):
    """提取单位"""
    units = ['m', 'm²', '个', '套', '件', '根', '条', '只', 'kg', 't']
    for unit in units:
        if unit in text:
            return unit
    return "个"

def extract_floor(text):
    """提取楼层"""
    floor_patterns = [
        r'一层', r'二层', r'三层', r'四层', r'五层',
        r'地下一层', r'地下二层',
        r'3层', r'4层', r'5层',
        r'三层夹层', r'四层夹层'
    ]
    for pattern in floor_patterns:
        if pattern in text:
            return pattern
    return "未知楼层"

def extract_drawing_number(text):
    """提取图纸号"""
    pattern = r'[\u4e00-\u9fa5]+-\d+'
    match = re.search(pattern, text)
    if match:
        return match.group()
    return ""

def extract_drawing_name(text):
    """提取图纸名称"""
    # 简单返回文本作为图纸名称
    return text[:50] if len(text) > 50 else text

@bp.route('/extract', methods=['POST'])
def extract_materials():
    """从图纸文字中提取材料信息"""
    try:
        data = request.json
        texts = data.get('texts', [])
        notes = data.get('notes', [])
        
        if not texts:
            return jsonify({
                "success": False,
                "error": "请提供文字内容"
            })
        
        materials = []
        for text in texts:
            if not text or len(text.strip()) < 5:
                continue
            
            material = {
                "name": extract_material_name(text),
                "model": extract_model(text),
                "quantity": extract_quantity(text),
                "unit": extract_unit(text),
                "position": "图中未知区域",
                "floor": extract_floor(text),
                "drawing_number": extract_drawing_number(text),
                "drawing_name": extract_drawing_name(text),
                "category": "建筑给排水和水暖",
                "inspection_batch": "给排水管道安装",
                "standard": "GB50242-2002, GB50268-2008"
            }
            
            materials.append(material)
        
        return jsonify({
            "success": True,
            "data": materials
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
