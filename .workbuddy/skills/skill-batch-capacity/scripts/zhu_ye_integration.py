#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
筑业资料上海版集成脚本
功能：将 skill_batch_capacity 技能的输出转换为筑业资料上海版支持的格式
作者：OpenClaw
版本：1.0.0
"""

import json
import pandas as pd
import sys
import os


def parse_report(report):
    """解析技能生成的报告，提取检验批容量数据"""
    capacity_data = {}
    materials_data = []
    
    lines = report.split('\n')
    in_capacity_section = False
    in_materials_section = False
    current_category = None
    current_drawing = None
    
    for line in lines:
        line = line.strip()
        
        # 检测检验批容量部分
        if line == '## 检验批容量':
            in_capacity_section = True
            in_materials_section = False
        elif in_capacity_section and line.startswith('- '):
            parts = line.split(': ')
            if len(parts) == 2:
                item = parts[0].strip('- ')
                quantity = parts[1]
                capacity_data[item] = quantity
        elif in_capacity_section and line.startswith('## '):
            in_capacity_section = False
        
        # 检测材料清单部分
        elif line == '## 材料清单':
            in_materials_section = True
            in_capacity_section = False
        elif in_materials_section and line.startswith('### 分类: '):
            current_category = line.replace('### 分类: ', '')
        elif in_materials_section and line.startswith('#### 图纸: '):
            # 提取图纸名称和图号
            drawing_info = line.replace('#### 图纸: ', '')
            if ' (图号: ' in drawing_info:
                drawing_name, drawing_number = drawing_info.split(' (图号: ')
                drawing_number = drawing_number.rstrip(')')
            else:
                drawing_name = drawing_info
                drawing_number = ''
            current_drawing = drawing_name
        elif in_materials_section and line.startswith('| 材料名称 |'):
            # 跳过表头
            pass
        elif in_materials_section and line.startswith('|---------|'):
            # 跳过分隔线
            pass
        elif in_materials_section and line.startswith('| '):
            # 提取材料信息
            parts = line.strip('|').split('|')
            if len(parts) >= 4:
                material_name = parts[0].strip()
                model = parts[1].strip()
                quantity = parts[2].strip()
                position = parts[3].strip()
                
                materials_data.append({
                    '分类': current_category,
                    '图纸名称': current_drawing,
                    '图号': drawing_number,
                    '材料名称': material_name,
                    '型号': model,
                    '数量': quantity,
                    '位置': position
                })
    
    return capacity_data, materials_data


def convert_to_zhu_ye(json_file, output_excel):
    """将技能输出的 JSON 转换为筑业资料格式"""
    try:
        # 读取 JSON 文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 解析报告
        report = data.get('report', '')
        if not report:
            print("[FAIL] 报告内容为空")
            return False
        
        # 提取检验批容量和材料数据
        capacity_data, materials_data = parse_report(report)
        
        # 转换检验批容量为筑业资料格式
        zhu_ye_capacity = []
        for item, quantity in capacity_data.items():
            # 提取单位
            unit = ''.join([c for c in quantity if not c.isdigit() and c != '.'])
            if not unit:
                unit = '个'  # 默认单位
            
            zhu_ye_capacity.append({
                '检验批项目': item,
                '容量': quantity,
                '单位': unit,
                '备注': ''
            })
        
        # 创建 Excel 文件
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            # 写入检验批容量工作表
            df_capacity = pd.DataFrame(zhu_ye_capacity)
            df_capacity.to_excel(writer, sheet_name='检验批容量', index=False)
            
            # 写入材料清单工作表
            if materials_data:
                df_materials = pd.DataFrame(materials_data)
                df_materials.to_excel(writer, sheet_name='材料清单', index=False)
        
        print(f"[OK] 转换完成，生成筑业资料导入文件: {output_excel}")
        print("请在筑业资料上海版中导入此文件")
        return True
        
    except Exception as e:
        print(f"[FAIL] 转换失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    if len(sys.argv) < 2:
        print("使用方法: python zhu_ye_integration.py <json文件路径>")
        print("示例: python zhu_ye_integration.py batch_capacity_20260413_215424.json")
        return
    
    json_file = sys.argv[1]
    
    if not os.path.exists(json_file):
        print(f"[FAIL] 文件不存在: {json_file}")
        return
    
    # 生成输出文件名
    base_name = os.path.splitext(json_file)[0]
    output_excel = f"{base_name}_zhu_ye.xlsx"
    
    print("开始转换为筑业资料格式...")
    success = convert_to_zhu_ye(json_file, output_excel)
    
    if success:
        print("\n操作步骤:")
        print("1. 打开筑业资料上海版软件")
        print("2. 进入检验批容量管理模块")
        print("3. 选择 '导入' 功能")
        print("4. 选择生成的 Excel 文件")
        print("5. 确认导入数据")


if __name__ == "__main__":
    main()
