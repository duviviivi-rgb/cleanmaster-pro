{
  "name": "awesome-design-md",
  "description": "提供Markdown格式的设计文档和规范，帮助前后端开发团队创建一致的设计文档",
  "version": "1.0.0",
  "tags": ["design", "markdown", "documentation", "frontend", "backend"],
  "author": "OpenClaw Team",
  "maintainer": "OpenClaw Team",
  "license": "MIT",
  "requirements": [],
  "entry": "scripts/awesome_design_md.py",
  "parameters": {
    "type": "object",
    "properties": {
      "template_type": {
        "type": "string",
        "description": "文档模板类型",
        "enum": ["component", "page", "api", "architecture", "style-guide"]
      },
      "name": {
        "type": "string",
        "description": "文档名称"
      },
      "description": {
        "type": "string",
        "description": "文档描述"
      },
      "details": {
        "type": "object",
        "description": "文档详细信息"
      }
    },
    "required": ["template_type", "name"]
  },
  "examples": [
    {
      "name": "创建组件设计文档",
      "input": {
        "template_type": "component",
        "name": "Button组件",
        "description": "通用按钮组件设计",
        "details": {
          "props": ["type", "size", "disabled"],
          "events": ["click", "hover"],
          "variants": ["primary", "secondary", "danger"]
        }
      },
      "output": "Button组件的Markdown设计文档"
    },
    {
      "name": "创建API文档",
      "input": {
        "template_type": "api",
        "name": "用户认证API",
        "description": "用户登录和注册API",
        "details": {
          "endpoints": ["/api/auth/login", "/api/auth/register"],
          "methods": ["POST"],
          "authentication": "JWT"
        }
      },
      "output": "用户认证API的Markdown文档"
    }
  ]
}