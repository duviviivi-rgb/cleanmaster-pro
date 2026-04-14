#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能: skill-batch-capacity
功能: 读取指定楼层的图纸，提取隐蔽工程项目信息
作者: OpenClaw
版本: 1.0.0
"""

import os
import re
import json
from _batch_capacity_calc import BatchCapacityCalculator, ConcealedWorksAnalyzer, ReportGenerator

def main():
    """主函数"""
    try:
        # 定义需要处理的楼层
        target_floors = ["三层", "四层", "三层夹层"]
        
        # 图纸目录
        drawings_dir = r"C:\Users\vivia\Desktop\东方肝胆医院医疗净化工程交付资料V4\图纸"
        
        # 初始化模块
        calculator = BatchCapacityCalculator()
        analyzer = ConcealedWorksAnalyzer()
        generator = ReportGenerator()
        
        # 计算检验批容量
        print("[INFO] 开始处理图纸...")
        data, capacity_list = calculator.calculate_batch_capacity([drawings_dir])
        
        # 分析隐蔽工程
        print("[INFO] 开始分析隐蔽工程...")
        concealed_works = analyzer.analyze_concealed_works(data)
        
        # 过滤指定楼层的隐蔽工程
        print("[INFO] 过滤指定楼层的隐蔽工程...")
        floor_concealed_works = filter_by_floor(concealed_works, target_floors)
        
        # 生成报告
        print("[INFO] 生成隐蔽工程报告...")
        report = generate_floor_report(floor_concealed_works, target_floors)
        
        # 保存报告
        output_file = generator.save_report(report, "markdown")
        
        # 返回结果
        result = {
            "status": "success",
            "message": "隐蔽工程报告生成成功",
            "report": report,
            "output_file": output_file,
            "statistics": {
                "total_concealed_works": len(floor_concealed_works)
            }
        }
        
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        # 错误处理
        error_result = {
            "status": "error",
            "message": f"处理失败: {str(e)}"
        }
        print(json.dumps(error_result, ensure_ascii=False))

def filter_by_floor(concealed_works, target_floors):
    """根据楼层过滤隐蔽工程"""
    filtered_works = []
    
    for work in concealed_works:
        # 检查图纸名称是否包含目标楼层
        drawing_name = work["drawing_name"]
        if any(floor in drawing_name for floor in target_floors):
            filtered_works.append(work)
        # 检查材料位置是否包含目标楼层
        position = work.get("position", "")
        if any(floor in position for floor in target_floors):
            filtered_works.append(work)
    
    # 去重
    unique_works = []
    seen = set()
    for work in filtered_works:
        key = (work["drawing_number"], work["material_name"], work["material_model"])
        if key not in seen:
            seen.add(key)
            unique_works.append(work)
    
    print(f"[INFO] 共过滤出 {len(unique_works)} 项隐蔽工程")
    return unique_works

def generate_floor_report(concealed_works, target_floors):
    """生成楼层隐蔽工程报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"# 医疗净化工程隐蔽工程项目报告\n\n"
    report += f"## 项目信息\n"
    report += f"- 项目名称: 东方肝胆医院医疗净化工程\n"
    report += f"- 目标楼层: {', '.join(target_floors)}\n"
    report += f"- 生成时间: {now}\n\n"
    
    # 隐蔽工程部分
    report += f"## 隐蔽工程项目\n\n"
    
    if concealed_works:
        report += "| 图纸名称 | 分部分项 | 图纸图号 | 材料名称 | 材料型号 | 隐蔽检查内容 |\n"
        report += "|---------|----------|---------|---------|---------|------------|\n"
        
        for work in concealed_works:
            # 获取分部分项信息
            category = work.get("category", "其他")
            division_info = division_mapping.get(category, {"分部": "其他工程", "分项": {}})
            inspection_item = get_inspection_item(work["material_name"])
            sub_division = division_info['分项'].get(inspection_item, "其他分项")
            division_subdivision = f"{division_info['分部']}/{sub_division}"
            
            # 检查内容
            inspection_text = "<br>".join(work["inspection_items"])
            
            report += f"| {work['drawing_name']} | {division_subdivision} | {work['drawing_number']} | {work['material_name']} | {work['material_model']} | {inspection_text} |\n"
    else:
        report += "- 未检测到指定楼层的隐蔽工程\n"
    
    # 统计信息
    report += f"\n## 统计信息\n"
    report += f"- 总隐蔽工程项数: {len(concealed_works)}\n"
    
    return report

def get_inspection_item(material_name):
    """根据材料名称获取检验批项目"""
    material_mapping = {
        "304金属钢管": "给排水管道安装",
        "镀锌钢板风管": "风管安装",
        "防火阀": "防火阀安装",
        "消声器": "消声器安装",
        "风机盘管": "风机盘管安装",
        "冷凝水管": "冷凝水管安装",
        "保温材料": "保温工程",
        "电缆": "电气线路安装",
        "开关": "电气设备安装",
        "插座": "电气设备安装",
        "净化灯": "净化设备安装",
        "高效过滤器": "净化设备安装",
        "洁净门": "净化设备安装",
        "截止阀": "阀门安装",
        "地漏": "卫生器具安装",
        "密封胶": "净化工程密封"
    }
    
    if material_name in material_mapping:
        return material_mapping[material_name]
    
    for key, value in material_mapping.items():
        if key in material_name:
            return value
    
    keywords = {
        "风管": "风管安装",
        "防火阀": "防火阀安装",
        "消声器": "消声器安装",
        "风机": "通风机安装",
        "风口": "风口安装",
        "空调": "空调设备安装",
        "冷却塔": "冷却塔安装",
        "冷凝水": "冷凝水管安装",
        "保温": "保温工程",
        "管": "给排水管道安装",
        "阀门": "阀门安装",
        "卫生": "卫生器具安装",
        "洁具": "卫生器具安装",
        "地漏": "卫生器具安装",
        "水箱": "给水设备安装",
        "水泵": "给水设备安装",
        "电缆": "电气线路安装",
        "开关": "电气设备安装",
        "插座": "电气设备安装",
        "灯具": "电气设备安装",
        "配电柜": "电气设备安装",
        "配电箱": "电气设备安装",
        "桥架": "电气线路安装",
        "母线": "电气线路安装",
        "净化": "净化设备安装",
        "过滤器": "净化设备安装",
        "洁净": "净化设备安装",
        "传递窗": "净化设备安装",
        "风淋室": "净化设备安装",
        "FFU": "净化设备安装",
        "密封": "净化工程密封"
    }
    
    for keyword, item in keywords.items():
        if keyword in material_name:
            return item
    
    return None

# 分项分部映射
division_mapping = {
    "暖通空调": {
        "分部": "通风与空调工程",
        "分项": {
            "风管安装": "风管制作与安装",
            "防火阀安装": "防火阀、排烟阀安装",
            "消声器安装": "消声器安装",
            "风机盘管安装": "风机盘管安装",
            "冷凝水管安装": "冷凝水系统安装",
            "保温工程": "绝热工程",
            "通风机安装": "通风机安装",
            "风口安装": "风口安装",
            "空调设备安装": "空调设备安装",
            "冷却塔安装": "冷却塔安装"
        }
    },
    "给排水": {
        "分部": "给水排水及采暖工程",
        "分项": {
            "给排水管道安装": "室内给水系统安装",
            "阀门安装": "阀门安装",
            "卫生器具安装": "卫生器具安装",
            "给水设备安装": "给水设备安装"
        }
    },
    "电气": {
        "分部": "建筑电气工程",
        "分项": {
            "电气线路安装": "电气动力安装",
            "电气设备安装": "电气照明安装"
        }
    },
    "净化工程": {
        "分部": "净化工程",
        "分项": {
            "净化设备安装": "净化设备安装",
            "净化工程密封": "净化工程密封"
        }
    }
}

from datetime import datetime

if __name__ == "__main__":
    main()
