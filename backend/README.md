# CleanMaster Pro Backend

后端项目使用 Flask + Python 构建，提供智能磁盘清理与数据治理工具的 API 服务。

## 项目结构

```
backend/
├── app/
│   ├── routes/            # 路由
│   │   ├── disk.py        # 磁盘管理
│   │   ├── scan.py        # 扫描功能
│   │   ├── clean.py       # 清理功能
│   │   ├── space.py       # 空间管理
│   │   ├── app.py         # 应用管理
│   │   ├── governance.py  # 数据治理
│   │   ├── history.py     # 历史记录
│   │   ├── optimization.py # 系统优化
│   │   └── recovery.py    # 文件恢复
│   └── __init__.py        # 应用初始化
├── requirements.txt       # 依赖配置
└── run.py                 # 应用入口
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务器

```bash
python run.py
```

服务器将运行在 http://127.0.0.1:5000/。

## API 端点

### 磁盘管理
- `GET /api/disks` - 获取磁盘列表
- `GET /api/disk/<letter>` - 获取磁盘详细信息

### 扫描功能
- `POST /api/scan/start` - 开始扫描
- `GET /api/scan/status` - 获取扫描状态
- `POST /api/scan/stop` - 停止扫描

### 清理功能
- `POST /api/clean/start` - 开始清理
- `GET /api/clean/status` - 获取清理状态
- `POST /api/clean/stop` - 停止清理
- `POST /api/clean/autoclean` - 设置自动清理

### 空间管理
- `POST /api/space/analyze` - 分析空间使用情况
- `GET /api/space/large-files` - 获取大文件列表
- `GET /api/space/duplicate-files` - 获取重复文件列表

### 应用管理
- `POST /api/app/scan` - 扫描应用程序
- `POST /api/app/uninstall` - 卸载应用程序
- `GET /api/app/detail/<app_id>` - 获取应用详细信息

### 数据治理
- `POST /api/governance/analyze` - 分析文件分类
- `POST /api/governance/optimize` - 优化数据结构
- `POST /api/governance/backup` - 备份数据

### 历史记录
- `GET /api/history` - 获取清理历史记录
- `GET /api/history/analysis` - 获取清理历史分析
- `DELETE /api/history/<id>` - 删除历史记录
- `POST /api/history/clear` - 清空历史记录

### 系统优化
- `POST /api/optimization/analyze` - 分析系统状态
- `POST /api/optimization/startup` - 管理启动项
- `POST /api/optimization/services` - 管理系统服务
- `POST /api/optimization/defrag` - 磁盘碎片整理

### 文件恢复
- `POST /api/recovery/scan` - 扫描可恢复文件
- `POST /api/recovery/start` - 开始恢复文件
- `GET /api/recovery/status` - 获取恢复状态
- `POST /api/recovery/stop` - 停止恢复

## 技术栈

- Flask 2.0.1
- Python 3.12
- Flask-CORS 3.0.10
- ezdxf 1.0.3
- PyPDF2 3.0.1
- numpy 1.24.3
- pandas 2.0.3
