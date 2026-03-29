# CleanMaster Pro 后端服务

## 项目简介

这是 CleanMaster Pro 的后端服务，基于 Node.js + Express 构建，提供磁盘清理、空间分析等功能的 API 接口。

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动服务

```bash
# 启动服务器
node simple-server.js
```

服务将运行在 http://localhost:5000

## API 接口

### 测试接口

- **GET /api/test** - 测试接口，返回成功消息

### 磁盘信息接口

- **GET /api/disk** - 获取磁盘信息列表

### 设置接口

- **GET /api/settings** - 获取用户设置
- **POST /api/settings** - 保存用户设置

### 扫描接口

- **GET /api/scan/quick** - 快速扫描指定磁盘
  - 参数：`disk` - 磁盘盘符，默认 C:

## 技术栈

- Node.js
- Express
- CORS

## 项目结构

```
├── server.js          # 主服务器文件
├── package.json       # 项目配置和依赖
└── README.md          # 项目说明
```