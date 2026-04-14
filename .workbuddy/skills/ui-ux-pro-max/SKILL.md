{
  "name": "ui-ux-pro-max",
  "description": "提供专业的UI/UX设计服务，包括用户界面设计、用户体验分析、交互设计和设计系统构建",
  "version": "1.0.0",
  "tags": ["ui", "ux", "design", "user-experience", "interface", "interaction"],
  "author": "OpenClaw Team",
  "maintainer": "OpenClaw Team",
  "license": "MIT",
  "requirements": [],
  "entry": "scripts/ui_ux_pro_max.py",
  "parameters": {
    "type": "object",
    "properties": {
      "service_type": {
        "type": "string",
        "description": "设计服务类型",
        "enum": ["ui-design", "ux-analysis", "interaction-design", "design-system", "user-research"]
      },
      "project_name": {
        "type": "string",
        "description": "项目名称"
      },
      "description": {
        "type": "string",
        "description": "项目描述"
      },
      "details": {
        "type": "object",
        "description": "项目详细信息"
      }
    },
    "required": ["service_type", "project_name"]
  },
  "examples": [
    {
      "name": "UI设计服务",
      "input": {
        "service_type": "ui-design",
        "project_name": "医疗净化工程管理系统",
        "description": "为医疗净化工程管理系统设计用户界面",
        "details": {
          "platform": "desktop",
          "target_audience": "工程管理人员",
          "style": "professional",
          "pages": ["登录页", "仪表盘", "文件管理", "材料列表", "报告生成"]
        }
      },
      "output": "医疗净化工程管理系统的UI设计方案"
    },
    {
      "name": "UX分析服务",
      "input": {
        "service_type": "ux-analysis",
        "project_name": "图纸解析工具",
        "description": "分析图纸解析工具的用户体验",
        "details": {
          "current_issues": ["文件上传慢", "界面复杂", "操作流程不清晰"],
          "user_goals": ["快速上传文件", "准确提取材料", "方便生成报告"]
        }
      },
      "output": "图纸解析工具的UX分析报告"
    }
  ]
}