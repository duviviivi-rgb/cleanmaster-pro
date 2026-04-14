# 检验批容量与隐蔽工程报告生成系统

## 项目简介

本系统用于解析图纸文件，提取材料信息，生成检验批容量和隐蔽工程报告。系统支持DWG、DXF、PDF等格式的图纸文件，能够智能识别材料名称、型号、数量等信息，并按楼层组织材料和报告。

## 技术栈

### 前端技术
- **框架**：Vue.js 3.0+
- **桌面容器**：Electron 16.0+
- **UI组件库**：Element Plus 2.0+
- **数据可视化**：ECharts 5.0+
- **HTTP客户端**：Axios 0.27+
- **路由管理**：Vue Router 4.0+
- **状态管理**：Pinia 2.0+

### 后端技术
- **语言**：Python 3.9+
- **Web框架**：Flask 2.0+
- **文件解析**：ezdxf 1.0+ (DWG/DXF)、PyPDF2 2.0+ (PDF)
- **数据存储**：SQLite 3.35+
- **数据处理**：NumPy 1.20+、Pandas 1.3+

## 功能特性

- **文件上传与解析**：支持批量上传图纸文件，自动解析文件内容
- **材料信息提取**：智能识别材料名称、型号、数量等信息
- **材料编辑**：手动编辑和修正提取的材料信息
- **报告生成**：生成检验批容量和隐蔽工程报告，支持HTML、Markdown、Excel等格式
- **配置管理**：管理用户配置和偏好设置，支持自定义提取规则和报告模板
- **历史记录**：保存历史处理结果，方便查询和对比，支持重新处理历史文件

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
# 启动Vue开发服务器
npm run dev

# 启动Electron开发模式
npm run electron:dev
```

### 构建打包

```bash
# 构建Vue应用
npm run build

# 打包Electron应用
npm run electron:build
```

## 项目结构

```
├── src/
│   ├── views/              # 页面组件
│   │   ├── HomeView.vue         # 首页
│   │   ├── FileProcessView.vue  # 文件处理页面
│   │   ├── MaterialEditView.vue # 材料编辑页面
│   │   ├── ReportPreviewView.vue # 报告预览页面
│   │   ├── ConfigView.vue       # 配置管理页面
│   │   └── HistoryView.vue      # 历史记录页面
│   ├── store/              # 状态管理
│   │   ├── index.ts             # Pinia配置
│   │   ├── file.ts              # 文件状态管理
│   │   └── material.ts           # 材料状态管理
│   ├── router/             # 路由配置
│   │   └── index.ts             # Vue Router配置
│   ├── main.ts             # 应用入口
│   └── App.vue             # 根组件
├── electron-main.js        # Electron主进程
├── preload.js              # Electron预加载脚本
├── package.json            # 项目配置和依赖
├── tsconfig.json           # TypeScript配置
├── vite.config.ts          # Vite配置
└── index.html              # HTML入口文件
```

## 使用说明

1. **文件上传**：在文件处理页面上传DWG、DXF、PDF等格式的图纸文件
2. **文件解析**：点击"解析文件"按钮，系统会自动解析文件内容并提取材料信息
3. **材料编辑**：在材料编辑页面查看和编辑提取的材料信息
4. **报告生成**：在报告预览页面生成和导出检验批容量和隐蔽工程报告
5. **配置管理**：在配置页面调整提取规则、自定义报告模板、设置输出格式和路径
6. **历史记录**：在历史记录页面查看和管理历史处理结果

## 注意事项

- 系统支持的文件格式：DWG、DXF、PDF
- 建议上传的文件大小不超过10MB，以确保解析速度
- 对于大型项目，建议分批上传文件，以避免内存占用过高
- 生成的报告默认保存在配置的输出路径中

## 联系方式

如有问题或建议，请联系开发团队。
