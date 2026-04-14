# CleanMaster Pro

智能磁盘清理与数据治理工具，提供全面的磁盘管理、清理、优化和数据恢复功能。

## 项目结构

```
CleanMaster Pro/
├── frontend/            # 前端代码
│   └── react/           # React前端项目
├── backend/             # 后端代码
│   └── app/             # Flask应用
├── desktop/             # 桌面应用
│   └── CleanMasterPro/  # WPF桌面应用
├── docs/                # 项目文档
├── skills/              # 技能相关代码
├── data/                # 数据文件
└── config/              # 配置文件
```

## 功能特性

### 磁盘管理
- 磁盘信息获取
- 磁盘空间分析
- 磁盘健康状态检测

### 扫描功能
- 快速扫描
- 深度扫描
- 智能扫描
- 扫描状态监控

### 清理功能
- 垃圾文件清理
- 临时文件清理
- 浏览器缓存清理
- 自动清理设置

### 空间管理
- 空间使用分析
- 大文件检测
- 重复文件检测
- 空间优化建议

### 应用管理
- 应用扫描
- 应用卸载
- 应用状态分析
- 启动项管理

### 数据治理
- 文件分类分析
- 数据结构优化
- 数据备份
- 数据恢复

### 系统优化
- 系统状态分析
- 启动项管理
- 服务管理
- 磁盘碎片整理

### 历史记录
- 清理历史管理
- 历史数据分析
- 清理效果评估

## 技术栈

### 前端
- React 18.2.0
- TypeScript 5.2.2
- Vite 5.2.0
- Tailwind CSS 4.0.0-alpha.13
- React Router DOM 6.22.3
- Axios 1.6.7
- Chart.js 4.4.8

### 后端
- Flask 2.0.1
- Python 3.12
- Flask-CORS 3.0.10
- ezdxf 1.0.3
- PyPDF2 3.0.1
- numpy 1.24.3
- pandas 2.0.3

### 桌面应用
- WPF
- C#
- .NET Framework

## 启动项目

### 后端

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 前端

```bash
cd frontend/react
npm install
npm run dev
```

### 桌面应用

使用 Visual Studio 打开 `desktop/CleanMasterPro/CleanMasterPro.csproj` 文件，然后运行应用。

## 部署

### 前端部署

```bash
cd frontend/react
npm run build
```

构建后的文件将输出到 `dist` 目录，可以部署到任何静态文件服务器。

### 后端部署

可以使用 Gunicorn、uWSGI 等 WSGI 服务器部署 Flask 应用，也可以使用 Docker 容器化部署。

## 开发指南

### 代码规范
- 前端：使用 TypeScript 类型定义，遵循 React 最佳实践
- 后端：使用 PEP 8 代码规范，添加适当的文档注释

### 测试
- 前端：使用 Jest 和 React Testing Library 进行单元测试
- 后端：使用 pytest 进行单元测试

### 提交规范
- 使用语义化提交信息
- 提交前运行代码检查和测试

## 许可证

MIT License
