# 个人电脑使用与游戏记录系统

一个轻量级、私有化的个人数据记录与分析平台，用于追踪电脑使用情况和游戏游玩记录。

## 功能特性

- 📊 **仪表盘** - 直观展示今日使用概览和趋势
- 💻 **应用记录** - 自动采集并记录应用使用情况
- 🎮 **游戏管理** - 记录游戏游玩时长和笔记
- 📈 **统计分析** - 多维度数据分析和可视化
- 📦 **数据管理** - 支持数据导入导出和备份
- 🌙 **深色模式** - 支持深色/浅色主题切换

## 技术栈

### 前端
- Vue 3 + TypeScript
- Element Plus UI 组件库
- ECharts 图表库
- Pinia 状态管理
- Vue Router 路由

### 后端
- FastAPI 框架
- SQLAlchemy ORM
- SQLite 数据库
- JWT 认证

### 客户端
- Python 数据采集
- psutil 进程监控
- pywin32 窗口管理

## 项目结构

```
├── frontend/          # 前端项目
├── backend/           # 后端项目
├── client/            # 数据采集客户端
└── README.md          # 项目说明
```

## 快速开始

### 1. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --port 8000
```

后端 API 文档: http://localhost:8000/docs

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端访问地址: http://localhost:5173

### 3. 启动数据采集（可选）

```bash
cd client

# 创建虚拟环境
python -m venv .venv
.\.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动采集
python -m collector.main
```

## 默认账户

首次使用需要注册账户，或使用以下方式创建默认账户：

```bash
cd backend
python -c "
from app.database import engine, Base
from app.models.user import User
from app.utils.security import hash_password
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)
db = Session(engine)

# 检查是否已有用户
if db.query(User).count() == 0:
    user = User(
        username='admin',
        password_hash=hash_password('admin123'),
        nickname='管理员'
    )
    db.add(user)
    db.commit()
    print('默认账户创建成功: admin / admin123')
else:
    print('已存在用户账户')
"
```

## 开发文档

详细的开发文档请参考项目根目录下的开发文档文件。

## 许可证

MIT License
