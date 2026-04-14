# CleanMaster Pro Frontend

前端项目使用 React + TypeScript + Vite + Tailwind CSS 构建，提供智能磁盘清理与数据治理工具的用户界面。

## 项目结构

```
frontend/react/
├── src/
│   ├── components/         # 组件
│   │   ├── Navbar.tsx      # 导航栏
│   │   └── Sidebar.tsx     # 侧边栏
│   ├── pages/              # 页面
│   │   ├── HomePage.tsx    # 首页
│   │   ├── ScanPage.tsx    # 扫描页面
│   │   ├── CleanPage.tsx   # 清理页面
│   │   ├── SpacePage.tsx   # 空间管理页面
│   │   ├── RecoveryPage.tsx # 文件恢复页面
│   │   ├── OptimizationPage.tsx # 系统优化页面
│   │   ├── AppPage.tsx     # 应用管理页面
│   │   ├── GovernancePage.tsx # 数据治理页面
│   │   ├── HistoryPage.tsx # 清理历史页面
│   │   └── SettingsPage.tsx # 设置页面
│   ├── services/           # 服务
│   │   ├── api.ts          # API服务
│   │   └── types.ts        # 类型定义
│   ├── App.tsx             # 应用主组件
│   ├── index.css           # 全局样式
│   └── main.tsx            # 应用入口
├── index.html              # HTML模板
├── package.json            # 项目配置
├── tailwind.config.js      # Tailwind CSS配置
├── postcss.config.js       # PostCSS配置
├── tsconfig.json           # TypeScript配置
├── tsconfig.node.json      # TypeScript Node配置
└── vite.config.ts          # Vite配置
```

## 安装依赖

```bash
npm install
```

## 启动开发服务器

```bash
npm run dev
```

开发服务器将运行在 http://localhost:3000/ 或其他可用端口。

## 构建生产版本

```bash
npm run build
```

构建后的文件将输出到 `dist` 目录。

## 技术栈

- React 18.2.0
- TypeScript 5.2.2
- Vite 5.2.0
- Tailwind CSS 4.0.0-alpha.13
- React Router DOM 6.22.3
- Axios 1.6.7
- Chart.js 4.4.8
