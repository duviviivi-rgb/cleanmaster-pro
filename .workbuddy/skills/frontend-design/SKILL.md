## SKILL

- **name**: frontend-design
- **description**: 前端设计技能，提供前端设计指导、组件设计、布局设计等功能，协助前后端页面的开发。
- **tags**: frontend, design, ui, ux, vue, electron
- **author**: System
- **version**: 1.0.0

## TRIGGER

- **pattern**: `/frontend-design`

## PARAMETERS

- **design_type**: 设计类型，可选值：component, layout, page, style
- **framework**: 前端框架，可选值：vue, react, angular
- **target_platform**: 目标平台，可选值：web, desktop, mobile
- **requirements**: 设计要求，详细描述设计需求

## EXAMPLES

1. **组件设计**
   - Input: `/frontend-design design_type=component framework=vue target_platform=desktop requirements=设计一个文件上传组件，支持拖拽上传、文件预览和批量上传功能`
   - Output: 提供文件上传组件的设计方案，包括组件结构、样式和交互逻辑

2. **页面布局设计**
   - Input: `/frontend-design design_type=layout framework=vue target_platform=desktop requirements=设计一个检验批容量与隐蔽工程报告生成工具的首页布局，包括文件上传区域、最近处理记录和功能导航`
   - Output: 提供首页布局的设计方案，包括布局结构、组件排列和响应式设计

3. **页面设计**
   - Input: `/frontend-design design_type=page framework=vue target_platform=desktop requirements=设计一个报告预览页面，支持Markdown、HTML和Excel格式的报告预览和导出`
   - Output: 提供报告预览页面的设计方案，包括页面结构、功能模块和交互流程

4. **样式设计**
   - Input: `/frontend-design design_type=style framework=vue target_platform=desktop requirements=设计一个统一的样式系统，包括颜色、字体、按钮样式和表单样式`
   - Output: 提供样式系统的设计方案，包括设计规范和实现代码

## SCRIPTS

- **main**: scripts/frontend_design.py