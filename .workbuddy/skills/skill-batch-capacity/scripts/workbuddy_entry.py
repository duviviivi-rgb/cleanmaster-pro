#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 技能入口脚本
功能: 处理 WorkBuddy 传入的参数，调用批容量计算功能
"""

import os
import sys
import json
from batch_capacity import BatchCapacityGenerator
from _batch_capacity_calc import BatchCapacityCalculator, ConcealedWorksAnalyzer, ReportGenerator

def main():
    """WorkBuddy 技能入口函数"""
    try:
        # 读取 WorkBuddy 传入的参数
        if len(sys.argv) > 1:
            # 从命令行参数读取 JSON 数据
            try:
                input_data = json.loads(sys.argv[1])
            except json.JSONDecodeError:
                # 如果解析失败，尝试使用示例数据
                print("[INFO] 命令行参数解析失败，使用示例数据")
                input_data = {
                    "files": ["C:\\Users\\vivia\\Desktop\\东方肝胆医院医疗净化工程交付资料V4\\图纸"],
                    "inspection_items": ["风管安装", "给排水管道安装"],
                    "output_format": "markdown"
                }
        else:
            # 从标准输入读取 JSON 数据
            try:
                input_data = json.loads(sys.stdin.read())
            except json.JSONDecodeError:
                # 如果解析失败，尝试使用示例数据
                print("[INFO] 标准输入解析失败，使用示例数据")
                input_data = {
                    "files": ["C:\\Users\\vivia\\Desktop\\东方肝胆医院医疗净化工程交付资料V4\\图纸"],
                    "inspection_items": ["风管安装", "给排水管道安装"],
                    "output_format": "markdown"
                }
        
        # 解析参数
        files = input_data.get("files", [])
        inspection_items = input_data.get("inspection_items", [])
        output_format = input_data.get("output_format", "markdown")
        
        if not files:
            # 如果没有提供文件，使用示例文件路径
            print(json.dumps({
                "status": "error",
                "message": "请提供图纸文件路径"
            }))
            return
        
        # 使用新的批容量计算模块
        calculator = BatchCapacityCalculator()
        analyzer = ConcealedWorksAnalyzer()
        generator = ReportGenerator()
        
        # 计算检验批容量
        data, capacity_list = calculator.calculate_batch_capacity(files)
        
        # 分析隐蔽工程
        concealed_works = analyzer.analyze_concealed_works(data)
        
        # 生成报告
        report = generator.generate_report(data, capacity_list, concealed_works, output_format)
        
        # 保存报告
        output_file = generator.save_report(report, output_format)
        
        # 返回结果
        result = {
            "status": "success",
            "message": "检验批容量和隐蔽工程报告生成成功",
            "report": report,
            "output_file": output_file,
            "statistics": {
                "total_drawings": len(data["drawings"]),
                "total_materials": sum(len(drawing["materials"]) for drawing in data["drawings"]),
                "total_concealed": len(concealed_works)
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

if __name__ == "__main__":
    main()
