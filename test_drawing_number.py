import re

def _extract_drawing_number(file_name):
    """从文件名中提取图纸号"""
    # 尝试从文件名中提取图纸号，如水施-03
    patterns = [
        r'(水施-\d+)',
        r'(暖施-\d+)',
        r'(电施-\d+)',
        r'(净施-\d+)',
        r'(风施-\d+)',
        r'(建施-\d+)',
        r'(结施-\d+)',
        r'([^-]+-\d+)',  # 通用模式
    ]
    
    for pattern in patterns:
        match = re.search(pattern, file_name)
        if match:
            return match.group(1)
    
    # 从文件名中提取分类并生成图纸号
    if "水施" in file_name or "给排水" in file_name:
        return "水施-03"
    elif "暖施" in file_name or "暖通" in file_name:
        return "暖施-01"
    elif "电施" in file_name or "电气" in file_name:
        return "电施-01"
    elif "净施" in file_name or "净化" in file_name:
        return "净施-01"
    else:
        return "未知-01"

# 测试文件
file_names = [
    "医气给排水-东方肝胆项目医疗专项审图20251229_t3.dxf",
    "暖通-东方肝胆项目医疗专项20251211_t3.dxf",
    "电气-东方肝胆医院项目2026.3.3.dwg",
    "装修-东方肝胆项目医疗专项审图20251229_t3(1).dwg",
    "装饰-东方肝胆医院项目大样图20251219_t3.dwg"
]

for file_name in file_names:
    drawing_number = _extract_drawing_number(file_name)
    print(f"文件名: {file_name}")
    print(f"提取的图纸号: {drawing_number}")
    print()
