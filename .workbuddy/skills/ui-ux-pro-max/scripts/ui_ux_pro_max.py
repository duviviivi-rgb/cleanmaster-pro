#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ui-ux-pro-max skill
提供专业的UI/UX设计服务
"""

import json
import sys
from datetime import datetime

def generate_ui_design(project_name, description, details):
    """生成UI设计方案"""
    platform = details.get('platform', 'desktop')
    target_audience = details.get('target_audience', '用户')
    style = details.get('style', 'modern')
    pages = details.get('pages', [])
    
    design = f"""# {project_name} - UI设计方案

## 项目描述
{description}

## 设计目标
- 提供直观易用的用户界面
- 符合目标用户的使用习惯
- 保持视觉一致性和美观性
- 支持响应式设计

## 设计风格
- 风格: {style}
- 目标受众: {target_audience}
- 平台: {platform}

## 页面设计
"""
    
    for page in pages:
        design += f"### {page}\n"
        design += "- 布局: 简洁明了的布局，突出核心功能\n"
        design += "- 色彩: 专业的色彩方案，符合行业特点\n"
        design += "- 字体: 清晰易读的字体选择\n"
        design += "- 交互: 流畅的交互体验\n"
        design += "- 响应式: 适配不同屏幕尺寸\n\n"
    
    design += "## 色彩方案\n"
    design += "| 颜色 | 十六进制 | 用途 |\n"
    design += "|------|----------|------|\n"
    design += "| 主色 | #1890ff | 主要按钮、强调元素 |\n"
    design += "| 辅助色 | #52c41a | 成功状态、提示信息 |\n"
    design += "| 警告色 | #faad14 | 警告状态 |\n"
    design += "| 错误色 | #f5222d | 错误状态 |\n"
    design += "| 中性色 | #f0f2f5 | 背景色 |\n"
    design += "| 文本色 | #333333 | 主要文本 |\n"
    
    design += "\n## 排版系统\n"
    design += "| 元素 | 字号 | 字重 | 行高 |\n"
    design += "|------|------|------|------|\n"
    design += "| 标题1 | 24px | 600 | 1.4 |\n"
    design += "| 标题2 | 20px | 500 | 1.4 |\n"
    design += "| 标题3 | 16px | 500 | 1.4 |\n"
    design += "| 正文 | 14px | 400 | 1.5 |\n"
    design += "| 说明 | 12px | 400 | 1.4 |\n"
    
    design += f"\n## 组件库\n- 按钮组件\n- 表单组件\n- 卡片组件\n- 表格组件\n- 导航组件\n- 对话框组件\n\n## 设计工具\n- Figma\n- Sketch\n- Adobe XD\n\n## 交付物\n- UI设计稿\n- 交互原型\n- 设计规范文档\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return design

def generate_ux_analysis(project_name, description, details):
    """生成UX分析报告"""
    current_issues = details.get('current_issues', [])
    user_goals = details.get('user_goals', [])
    
    analysis = f"""# {project_name} - UX分析报告

## 项目描述
{description}

## 用户目标
"""
    
    for goal in user_goals:
        analysis += f"- {goal}\n"
    
    analysis += "\n## 当前问题\n"
    
    for issue in current_issues:
        analysis += f"- {issue}\n"
    
    analysis += "\n## 用户旅程分析\n"
    analysis += "| 阶段 | 用户行为 | 痛点 | 机会点 |\n"
    analysis += "|------|----------|------|--------|\n"
    analysis += "| 发现 | 寻找工具 | 信息不足 | 优化搜索引擎优化 |\n"
    analysis += "| 学习 | 了解功能 | 文档复杂 | 提供视频教程 |\n"
    analysis += "| 使用 | 执行任务 | 操作复杂 | 简化界面流程 |\n"
    analysis += "| 完成 | 达成目标 | 结果不满意 | 提高准确性 |\n"
    analysis += "| 反馈 | 提供反馈 | 渠道不畅 | 建立反馈机制 |\n"
    
    analysis += "\n## 可用性测试发现\n"
    analysis += "1. **导航问题**: 用户难以找到特定功能\n"
    analysis += "2. **表单填写**: 表单验证不明确，导致用户错误\n"
    analysis += "3. **加载时间**: 大型文件上传速度慢\n"
    analysis += "4. **错误处理**: 错误提示不够友好\n"
    analysis += "5. **移动端适配**: 在移动设备上体验不佳\n"
    
    analysis += "\n## 改进建议\n"
    analysis += "1. **简化导航**: 重新设计导航结构，突出核心功能\n"
    analysis += "2. **优化表单**: 提供实时验证和清晰的错误提示\n"
    analysis += "3. **性能优化**: 实现文件分块上传和进度显示\n"
    analysis += "4. **增强反馈**: 提供更友好的错误提示和操作确认\n"
    analysis += "5. **响应式设计**: 优化移动端界面布局\n"
    
    analysis += "\n## 优先级排序\n"
    analysis += "| 优先级 | 改进项 | 预期效果 |\n"
    analysis += "|--------|--------|----------|\n"
    analysis += "| 高 | 简化导航 | 提高用户找到功能的效率 |\n"
    analysis += "| 高 | 优化表单 | 减少用户输入错误 |\n"
    analysis += "| 中 | 性能优化 | 提升文件处理速度 |\n"
    analysis += "| 中 | 增强反馈 | 改善用户体验 |\n"
    analysis += "| 低 | 响应式设计 | 支持更多设备 |\n"
    
    analysis += f"\n## 结论\n通过UX分析，我们发现了多个影响用户体验的问题，并提出了相应的改进建议。实施这些建议将显著提升用户满意度和产品可用性。\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return analysis

def generate_interaction_design(project_name, description, details):
    """生成交互设计方案"""
    user_flows = details.get('user_flows', [])
    interactions = details.get('interactions', [])
    
    design = f"""# {project_name} - 交互设计方案

## 项目描述
{description}

## 设计原则
- **直观性**: 操作符合用户预期
- **一致性**: 交互模式保持一致
- **反馈性**: 提供及时的操作反馈
- **容错性**: 允许用户犯错并轻松恢复
- **效率性**: 减少操作步骤，提高效率

## 用户流程
"""
    
    for flow in user_flows:
        design += f"### {flow.get('name', '流程')}\n"
        design += "步骤:\n"
        for step in flow.get('steps', []):
            design += f"- {step}\n"
        design += "\n"
    
    design += "## 交互模式\n"
    design += "| 交互元素 | 行为 | 反馈 |\n"
    design += "|----------|------|------|\n"
    design += "| 按钮 | 点击 | 视觉反馈 + 执行操作 |\n"
    design += "| 表单 | 输入 | 实时验证 + 错误提示 |\n"
    design += "| 下拉菜单 | 点击展开 | 显示选项列表 |\n"
    design += "| 对话框 | 打开/关闭 | 淡入淡出动画 |\n"
    design += "| 加载状态 | 执行操作 | 加载动画 |\n"
    
    design += "\n## 微交互设计\n"
    design += "1. **按钮悬停**: 轻微放大和颜色变化\n"
    design += "2. **表单输入**: 输入时边框颜色变化\n"
    design += "3. **加载状态**: 平滑的加载动画\n"
    design += "4. **成功提示**: 短暂的成功动画\n"
    design += "5. **错误提示**: 红色闪烁效果\n"
    
    design += "\n## 导航设计\n"
    design += "- **主导航**: 顶部导航栏，包含核心功能\n"
    design += "- **侧边栏**: 详细功能分类\n"
    design += "- **面包屑**: 显示当前位置\n"
    design += "- **分页**: 内容分页导航\n"
    
    design += "\n## 响应式交互\n"
    design += "| 设备 | 交互调整 |\n"
    design += "|------|----------|\n"
    design += "| 桌面 | 鼠标悬停效果，键盘快捷键 |\n"
    design += "| 平板 | 触摸友好的按钮尺寸 |\n"
    design += "| 手机 | 简化导航，手势操作 |\n"
    
    design += f"\n## 交付物\n- 交互流程图\n- 交互原型\n- 微交互动效设计\n- 响应式交互规范\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return design

def generate_design_system(project_name, description, details):
    """生成设计系统"""
    components = details.get('components', [])
    guidelines = details.get('guidelines', [])
    
    system = f"""# {project_name} - 设计系统

## 项目描述
{description}

## 设计系统目标
- 确保设计一致性
- 提高设计和开发效率
- 简化维护和更新
- 建立品牌识别

## 设计原则
"""
    
    for guideline in guidelines:
        system += f"- {guideline}\n"
    
    system += "\n## 色彩系统\n"
    system += "| 颜色 | 十六进制 | RGB | 用途 |\n"
    system += "|------|----------|-----|------|\n"
    system += "| 主色 | #1890ff | 24, 144, 255 | 主要按钮、品牌标识 |\n"
    system += "| 主色浅色 | #e6f7ff | 230, 247, 255 | 背景色、高亮 |\n"
    system += "| 辅助色 | #52c41a | 82, 196, 26 | 成功状态 |\n"
    system += "| 警告色 | #faad14 | 250, 173, 20 | 警告状态 |\n"
    system += "| 错误色 | #f5222d | 245, 34, 45 | 错误状态 |\n"
    system += "| 中性色1 | #fafafa | 250, 250, 250 | 页面背景 |\n"
    system += "| 中性色2 | #f0f0f0 | 240, 240, 240 | 分割线 |\n"
    system += "| 中性色3 | #8c8c8c | 140, 140, 140 | 次要文本 |\n"
    system += "| 中性色4 | #262626 | 38, 38, 38 | 主要文本 |\n"
    
    system += "\n## 排版系统\n"
    system += "| 字体 | 字号 | 字重 | 行高 | 用途 |\n"
    system += "|------|------|------|------|------|\n"
    system += "| 标题 | 24px | 600 | 1.2 | H1 |\n"
    system += "| 标题 | 20px | 500 | 1.3 | H2 |\n"
    system += "| 标题 | 16px | 500 | 1.4 | H3 |\n"
    system += "| 正文 | 14px | 400 | 1.5 | 普通文本 |\n"
    system += "| 说明 | 12px | 400 | 1.4 | 辅助文本 |\n"
    
    system += "\n## 组件库\n"
    
    for component in components:
        system += f"### {component}\n"
        system += "- 用途: 描述组件的使用场景\n"
        system += "- 变体: 不同状态和样式\n"
        system += "- 交互: 组件的交互行为\n"
        system += "- 代码: 组件的实现代码\n"
        system += "\n"
    
    system += "## 布局系统\n"
    system += "| 断点 | 宽度 | 列数 | 间距 |\n"
    system += "|------|------|------|------|\n"
    system += "| xs | < 576px | 12 | 16px |\n"
    system += "| sm | 576px | 12 | 16px |\n"
    system += "| md | 768px | 12 | 20px |\n"
    system += "| lg | 992px | 12 | 24px |\n"
    system += "| xl | 1200px | 12 | 28px |\n"
    
    system += "\n## 图标系统\n"
    system += "- 使用Font Awesome或Material Icons\n"
    system += "- 统一的图标风格\n"
    system += "- 适当的图标尺寸\n"
    
    system += f"\n## 交付物\n- 设计系统文档\n- 组件库\n- 设计规范\n- 代码实现\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return system

def generate_user_research(project_name, description, details):
    """生成用户研究报告"""
    research_methods = details.get('methods', [])
    participants = details.get('participants', [])
    
    research = f"""# {project_name} - 用户研究报告

## 项目描述
{description}

## 研究目标
- 了解用户需求和痛点
- 识别用户行为模式
- 评估当前产品的用户体验
- 为设计决策提供依据

## 研究方法
"""
    
    for method in research_methods:
        research += f"- {method}\n"
    
    research += "\n## 参与者
"
    
    for participant in participants:
        research += f"- {participant}\n"
    
    research += "\n## 研究发现\n"
    research += "### 用户需求\n"
    research += "1. **功能需求**: 用户需要快速上传和处理文件\n"
    research += "2. **性能需求**: 系统响应速度要快，特别是处理大型文件时\n"
    research += "3. **可靠性**: 系统要稳定，避免崩溃和数据丢失\n"
    research += "4. **易用性**: 界面要简单直观，易于学习和使用\n"
    research += "5. **支持**: 提供及时有效的技术支持\n"
    
    research += "\n### 用户痛点\n"
    research += "1. **文件上传**: 大型文件上传速度慢，容易失败\n"
    research += "2. **操作复杂**: 某些功能操作步骤过多，不够直观\n"
    research += "3. **错误处理**: 错误提示不够清晰，难以理解\n"
    research += "4. **学习成本**: 新用户需要较长时间才能掌握系统使用\n"
    research += "5. **兼容性**: 在不同设备和浏览器上的表现不一致\n"
    
    research += "\n### 用户行为模式\n"
    research += "1. **使用频率**: 大多数用户每天使用系统多次\n"
    research += "2. **主要任务**: 文件上传、材料提取、报告生成\n"
    research += "3. **使用环境**: 主要在办公室环境使用，部分用户在现场使用移动设备\n"
    research += "4. **技术水平**: 用户技术水平参差不齐，从初级到高级都有\n"
    
    research += "\n## 用户画像\n"
    research += "### 用户画像1: 工程管理人员\n"
    research += "- **年龄**: 30-45岁\n"
    research += "- **职业**: 工程经理、技术负责人\n"
    research += "- **技术水平**: 中等\n"
    research += "- **使用场景**: 查看报告、管理项目\n"
    research += "- **需求**: 快速获取项目信息，生成专业报告\n"
    
    research += "\n### 用户画像2: 技术人员\n"
    research += "- **年龄**: 25-35岁\n"
    research += "- **职业**: 工程师、技术员\n"
    research += "- **技术水平**: 较高\n"
    research += "- **使用场景**: 上传图纸、提取材料、生成报告\n"
    research += "- **需求**: 高效处理文件，准确提取信息\n"
    
    research += "\n## 建议\n"
    research += "1. **优化文件上传**: 实现分块上传和断点续传\n"
    research += "2. **简化操作流程**: 减少操作步骤，提供批量处理功能\n"
    research += "3. **改善错误处理**: 提供清晰友好的错误提示\n"
    research += "4. **增强用户引导**: 添加新手教程和操作提示\n"
    research += "5. **提高兼容性**: 优化在不同设备和浏览器上的表现\n"
    
    research += f"\n## 结论\n通过用户研究，我们深入了解了用户的需求、痛点和行为模式，为产品设计和改进提供了有力的依据。实施这些建议将显著提升用户满意度和产品价值。\n\n## 生成时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return research

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
        service_type = input_data.get('service_type')
        project_name = input_data.get('project_name')
        description = input_data.get('description', '')
        details = input_data.get('details', {})
        
        if not service_type or not project_name:
            print(json.dumps({
                "success": False,
                "error": "缺少必要参数"
            }))
            return
        
        if service_type == 'ui-design':
            result = generate_ui_design(project_name, description, details)
        elif service_type == 'ux-analysis':
            result = generate_ux_analysis(project_name, description, details)
        elif service_type == 'interaction-design':
            result = generate_interaction_design(project_name, description, details)
        elif service_type == 'design-system':
            result = generate_design_system(project_name, description, details)
        elif service_type == 'user-research':
            result = generate_user_research(project_name, description, details)
        else:
            print(json.dumps({
                "success": False,
                "error": "不支持的服务类型"
            }))
            return
        
        print(json.dumps({
            "success": True,
            "data": {
                "content": result,
                "service_type": service_type,
                "project_name": project_name
            }
        }))
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))

if __name__ == "__main__":
    main()
