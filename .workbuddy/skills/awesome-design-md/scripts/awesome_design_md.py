#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
awesome-design-md skill
提供Markdown格式的设计文档和规范
"""

import json
import sys
from datetime import datetime

def generate_component_doc(name, description, details):
    """生成组件设计文档"""
    props = details.get('props', [])
    events = details.get('events', [])
    variants = details.get('variants', [])
    
    doc = f"""# {name}

## 组件描述
{description}

## 属性 (Props)
| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
"""
    
    for prop in props:
        if isinstance(prop, dict):
            prop_name = prop.get('name', '未知')
            prop_type = prop.get('type', 'any')
            prop_default = prop.get('default', '-')
            prop_desc = prop.get('description', '')
        else:
            prop_name = prop
            prop_type = 'any'
            prop_default = '-'
            prop_desc = ''
        doc += f"| {prop_name} | {prop_type} | {prop_default} | {prop_desc} |\n"
    
    doc += "\n## 事件 (Events)\n| 事件名 | 参数 | 说明 |\n|--------|------|------|\n"
    
    for event in events:
        if isinstance(event, dict):
            event_name = event.get('name', '未知')
            event_params = event.get('params', '-')
            event_desc = event.get('description', '')
        else:
            event_name = event
            event_params = '-'
            event_desc = ''
        doc += f"| {event_name} | {event_params} | {event_desc} |\n"
    
    doc += "\n## 变体 (Variants)\n| 变体名 | 说明 |\n|--------|------|\n"
    
    for variant in variants:
        if isinstance(variant, dict):
            variant_name = variant.get('name', '未知')
            variant_desc = variant.get('description', '')
        else:
            variant_name = variant
            variant_desc = ''
        doc += f"| {variant_name} | {variant_desc} |\n"
    
    doc += f"\n## 设计规范\n- 遵循项目的设计系统\n- 响应式设计支持\n- 可访问性考虑\n\n## 实现建议\n- 使用 Vue 3 Composition API\n- 组件命名使用 PascalCase\n- 样式使用 scoped CSS\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return doc

def generate_page_doc(name, description, details):
    """生成页面设计文档"""
    sections = details.get('sections', [])
    components = details.get('components', [])
    
    doc = f"""# {name}

## 页面描述
{description}

## 页面结构
| 区域 | 组件 | 功能 |
|------|------|------|
"""
    
    for section in sections:
        if isinstance(section, dict):
            section_name = section.get('name', '未知')
            section_component = section.get('component', '-')
            section_func = section.get('function', '')
        else:
            section_name = section
            section_component = '-'
            section_func = ''
        doc += f"| {section_name} | {section_component} | {section_func} |\n"
    
    doc += "\n## 使用的组件\n| 组件名 | 版本 | 用途 |\n|--------|------|------|\n"
    
    for component in components:
        if isinstance(component, dict):
            comp_name = component.get('name', '未知')
            comp_version = component.get('version', 'latest')
            comp_purpose = component.get('purpose', '')
        else:
            comp_name = component
            comp_version = 'latest'
            comp_purpose = ''
        doc += f"| {comp_name} | {comp_version} | {comp_purpose} |\n"
    
    doc += f"\n## 页面流程\n1. 页面加载\n2. 数据获取\n3. 渲染内容\n4. 用户交互\n5. 数据提交\n\n## 设计规范\n- 页面布局遵循响应式设计\n- 导航结构清晰\n- 表单验证完善\n- 错误处理友好\n\n## 性能优化\n- 懒加载非关键资源\n- 缓存静态资源\n- 减少HTTP请求\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return doc

def generate_api_doc(name, description, details):
    """生成API设计文档"""
    endpoints = details.get('endpoints', [])
    methods = details.get('methods', [])
    authentication = details.get('authentication', 'None')
    
    doc = f"""# {name}

## API描述
{description}

## 认证方式
{authentication}

## 接口列表
| 端点 | 方法 | 功能 | 请求体 | 响应 |
|------|------|------|--------|------|
"""
    
    for endpoint in endpoints:
        for method in methods:
            doc += f"| {endpoint} | {method} | 描述 | JSON | JSON |\n"
    
    doc += "\n## 请求示例\n```json\n{\n  \"key\": \"value\"\n}\n```\n\n## 响应示例\n### 成功\n```json\n{\n  \"success\": true,\n  \"data\": {}\n}\n```\n\n### 失败\n```json\n{\n  \"success\": false,\n  \"error\": \"错误信息\"\n}\n```\n\n## 错误码\n| 代码 | 描述 |\n|------|------|\n| 400 | 请求参数错误 |\n| 401 | 未授权 |\n| 403 | 禁止访问 |\n| 404 | 资源不存在 |\n| 500 | 服务器内部错误 |\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return doc

def generate_architecture_doc(name, description, details):
    """生成架构设计文档"""
    modules = details.get('modules', [])
    technologies = details.get('technologies', [])
    
    doc = f"""# {name}

## 架构描述
{description}

## 系统模块
| 模块名 | 职责 | 技术栈 |
|--------|------|--------|
"""
    
    for module in modules:
        if isinstance(module, dict):
            module_name = module.get('name', '未知')
            module_responsibility = module.get('responsibility', '')
            module_tech = module.get('technology', '-')
        else:
            module_name = module
            module_responsibility = ''
            module_tech = '-'
        doc += f"| {module_name} | {module_responsibility} | {module_tech} |\n"
    
    doc += "\n## 技术栈\n| 类别 | 技术 | 版本 |\n|------|------|------|\n"
    
    for tech in technologies:
        if isinstance(tech, dict):
            tech_category = tech.get('category', '未知')
            tech_name = tech.get('name', '未知')
            tech_version = tech.get('version', 'latest')
        else:
            tech_category = '未知'
            tech_name = tech
            tech_version = 'latest'
        doc += f"| {tech_category} | {tech_name} | {tech_version} |\n"
    
    doc += "\n## 系统架构图\n```mermaid\ngraph TD\n    A[客户端] --> B[API网关]\n    B --> C[微服务1]\n    B --> D[微服务2]\n    C --> E[数据库]\n    D --> E\n```\n\n## 部署架构\n- 容器化部署\n- 负载均衡\n- 自动缩放\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return doc

def generate_style_guide_doc(name, description, details):
    """生成样式指南文档"""
    colors = details.get('colors', [])
    typography = details.get('typography', [])
    spacing = details.get('spacing', [])
    
    doc = f"""# {name}

## 样式指南描述
{description}

## 颜色系统
| 颜色名 | 十六进制 | RGB | 用途 |
|--------|----------|-----|------|
"""
    
    for color in colors:
        if isinstance(color, dict):
            color_name = color.get('name', '未知')
            color_hex = color.get('hex', '#000000')
            color_rgb = color.get('rgb', '0, 0, 0')
            color_purpose = color.get('purpose', '')
        else:
            color_name = color
            color_hex = '#000000'
            color_rgb = '0, 0, 0'
            color_purpose = ''
        doc += f"| {color_name} | {color_hex} | {color_rgb} | {color_purpose} |\n"
    
    doc += "\n## 排版系统\n| 样式 | 字号 | 字重 | 行高 | 用途 |\n|------|------|------|------|------|\n"
    
    for typo in typography:
        if isinstance(typo, dict):
            typo_style = typo.get('style', '未知')
            typo_size = typo.get('size', '16px')
            typo_weight = typo.get('weight', '400')
            typo_line_height = typo.get('line_height', '1.5')
            typo_purpose = typo.get('purpose', '')
        else:
            typo_style = typo
            typo_size = '16px'
            typo_weight = '400'
            typo_line_height = '1.5'
            typo_purpose = ''
        doc += f"| {typo_style} | {typo_size} | {typo_weight} | {typo_line_height} | {typo_purpose} |\n"
    
    doc += "\n## 间距系统\n| 名称 | 值 | 用途 |\n|------|------|------|\n"
    
    for space in spacing:
        if isinstance(space, dict):
            space_name = space.get('name', '未知')
            space_value = space.get('value', '8px')
            space_purpose = space.get('purpose', '')
        else:
            space_name = space
            space_value = '8px'
            space_purpose = ''
        doc += f"| {space_name} | {space_value} | {space_purpose} |\n"
    
    doc += f"\n## 组件样式\n- 按钮样式\n- 表单元素样式\n- 卡片样式\n- 导航样式\n\n## 响应式断点\n| 断点 | 宽度 | 设备 |\n|------|------|------|\n| sm | 576px | 手机 |\n| md | 768px | 平板 |\n| lg | 992px | 笔记本 |\n| xl | 1200px | 桌面 |\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return doc

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "缺少参数"
        }))
        return
    
    try:
        input_data = json.loads(sys.argv[1])
        template_type = input_data.get('template_type')
        name = input_data.get('name')
        description = input_data.get('description', '')
        details = input_data.get('details', {})
        
        if not template_type or not name:
            print(json.dumps({
                "success": False,
                "error": "缺少必要参数"
            }))
            return
        
        if template_type == 'component':
            doc = generate_component_doc(name, description, details)
        elif template_type == 'page':
            doc = generate_page_doc(name, description, details)
        elif template_type == 'api':
            doc = generate_api_doc(name, description, details)
        elif template_type == 'architecture':
            doc = generate_architecture_doc(name, description, details)
        elif template_type == 'style-guide':
            doc = generate_style_guide_doc(name, description, details)
        else:
            print(json.dumps({
                "success": False,
                "error": "不支持的模板类型"
            }))
            return
        
        print(json.dumps({
            "success": True,
            "data": {
                "content": doc,
                "format": "markdown",
                "template_type": template_type,
                "name": name
            }
        }))
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))

if __name__ == "__main__":
    main()
