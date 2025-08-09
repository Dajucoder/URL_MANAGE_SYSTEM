# 🌐 现代化网站推荐系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🚀 发现精彩网站，开启数字世界之旅

一个基于 PyQt6 构建的现代化网站推荐和管理系统，采用 2025 年最新的 UI/UX 设计标准，提供流体设计、微交互和响应式布局的用户体验。

## ✨ 主要特性

### 🎨 现代化界面设计
- **流体设计**: 柔和的渐变背景和圆角设计
- **微交互**: 丰富的悬停和焦点动画效果  
- **响应式布局**: 支持桌面、平板、移动端适配
- **无障碍设计**: 高对比度和键盘导航支持

### 🔐 完整的用户系统
- 用户注册和登录
- 密码强度检查
- 账户安全保护
- 登录历史记录

### 🗄️ 数据库支持
- PostgreSQL 数据库集成
- 自动数据表创建
- 数据备份和恢复
- 离线模式支持

### ⚙️ 灵活的配置系统
- 命令行参数配置
- 配置文件管理
- 主题切换支持
- 多语言界面

## 🔧 系统要求

### 基础要求
- **操作系统**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 或更高版本
- **内存**: 最少 4GB RAM
- **存储**: 至少 500MB 可用空间

### 可选要求
- **PostgreSQL**: 12.0+ (用于数据持久化)
- **Git**: 用于版本控制和更新

## 📦 安装步骤

### 步骤 1: 克隆项目
```bash
git clone https://github.com/yourusername/URL_MANAGE_SYSTEM.git
cd URL_MANAGE_SYSTEM
```

### 步骤 2: 创建虚拟环境
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3: 安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 4: 配置数据库（可选）
```bash
# 安装 PostgreSQL（如需要）
# Windows: 下载官方安装包
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql

# 创建数据库
sudo -u postgres createdb user_auth_system
```

### 步骤 5: 创建配置文件
```bash
# 复制配置模板
cp config.ini.example config.ini

# 编辑配置文件（填入实际数据库信息）
# Windows: notepad config.ini
# macOS/Linux: nano config.ini
```

### 步骤 6: 启动应用
```bash
python modern_app.py
```

## 🚀 使用方法

### 基础启动
```bash
# 使用默认配置启动
python modern_app.py

# 显示帮助信息
python modern_app.py --help

# 显示版本信息
python modern_app.py --version
```

### 数据库配置示例
```bash
# 连接到本地数据库
python modern_app.py --db-host localhost --db-port 5432 --db-name myapp

# 连接到远程数据库
python modern_app.py \
  --db-host 192.168.1.100 \
  --db-port 5432 \
  --db-name website_system \
  --db-user admin \
  --db-password yourpassword
```

### 界面定制示例
```bash
# 设置窗口大小和深色主题
python modern_app.py --window-size 1400x900 --theme dark

# 全屏启动
python modern_app.py --fullscreen

# 大字体模式
python modern_app.py --font-size 14

# 调试模式
python modern_app.py --debug
```

### 开发和测试示例
```bash
# 开发模式（调试 + 详细日志）
python modern_app.py --debug --theme light

# 快速测试（跳过启动画面）
python modern_app.py --no-splash --debug

# 自动登录测试
python modern_app.py --auto-login testuser --debug
```

## 📋 命令行参数详解

### 基本选项
| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--version` | - | 显示版本信息 | `python modern_app.py --version` |
| `--config` | `-c` | 指定配置文件路径 | `python modern_app.py -c custom.ini` |
| `--debug` | - | 启用调试模式 | `python modern_app.py --debug` |

### 数据库配置
| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--db-host` | 数据库主机地址 | localhost | `--db-host 192.168.1.100` |
| `--db-port` | 数据库端口 | 5432 | `--db-port 5433` |
| `--db-name` | 数据库名称 | user_auth_system | `--db-name myapp_db` |
| `--db-user` | 数据库用户名 | postgres | `--db-user myuser` |
| `--db-password` | 数据库密码 | - | `--db-password mypassword` |

### 界面配置
| 参数 | 说明 | 可选值 | 示例 |
|------|------|--------|------|
| `--window-size` | 窗口大小 | 宽度x高度 | `--window-size 1200x800` |
| `--theme` | 界面主题 | light/dark/auto | `--theme dark` |
| `--font-size` | 字体大小 | 数字 | `--font-size 12` |
| `--language` | 界面语言 | zh-CN/en-US | `--language zh-CN` |

### 功能选项
| 参数 | 说明 | 示例 |
|------|------|------|
| `--auto-login` | 自动登录用户名 | `--auto-login admin` |
| `--fullscreen` | 全屏模式启动 | `--fullscreen` |
| `--no-splash` | 跳过启动画面 | `--no-splash` |

## ⚙️ 配置文件

系统支持通过配置文件进行设置，默认配置文件为 `config.ini`：

```ini
[database]
host = localhost
port = 5432
database = user_auth_system
user = postgres
password = your_password_here

[ui]
theme = dark
language = zh-CN
window_width = 1000
window_height = 650
font_size = 10

[application]
remember_login = true
auto_login = false
debug_mode = false
```

## 🗄️ 数据库设置

### PostgreSQL 安装和配置

1. **安装 PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # CentOS/RHEL
   sudo yum install postgresql-server postgresql-contrib
   
   # macOS
   brew install postgresql
   
   # Windows
   # 下载并安装 PostgreSQL 官方安装包
   ```

2. **创建数据库和用户**
   ```sql
   -- 连接到 PostgreSQL
   sudo -u postgres psql
   
   -- 创建数据库
   CREATE DATABASE user_auth_system;
   
   -- 创建用户
   CREATE USER webapp_user WITH PASSWORD 'your_password';
   
   -- 授权
   GRANT ALL PRIVILEGES ON DATABASE user_auth_system TO webapp_user;
   ```

3. **使用数据库启动应用**
   ```bash
   python modern_app.py \
     --db-host localhost \
     --db-name user_auth_system \
     --db-user webapp_user \
     --db-password your_password
   ```

## 🎨 界面主题

系统支持多种界面主题：

- **light**: 明亮主题，适合白天使用
- **dark**: 深色主题，适合夜间使用
- **auto**: 自动主题，根据系统设置切换

```bash
# 切换主题
python modern_app.py --theme dark
```

## 🔧 开发指南

### 项目结构
```
URL_MANAGE_SYSTEM/
├── modern_app.py              # 主启动文件
├── config.ini.example         # 配置文件模板
├── requirements.txt           # 依赖列表
├── README.md                  # 项目文档
├── src/                      # 源代码目录
│   ├── core/                 # 核心模块
│   │   ├── auth_system.py    # 认证系统
│   │   └── managers.py       # 管理器模块
│   └── ui/                   # 界面模块
│       ├── modern_login_window.py    # 现代化登录窗口
│       ├── modern_components.py     # 现代化组件
│       ├── main_window.py           # 主窗口
│       └── ...
├── assets/                   # 资源文件
├── config/                   # 配置文件目录
├── logs/                     # 日志文件
└── scripts/                  # 脚本文件
```

### 添加新功能

1. **创建新的界面组件**
   ```python
   # src/ui/my_component.py
   from PyQt6.QtWidgets import QWidget
   
   class MyComponent(QWidget):
       def __init__(self):
           super().__init__()
           self.init_ui()
   ```

2. **添加命令行参数**
   ```python
   # 在 modern_app.py 的 parse_arguments() 函数中添加
   parser.add_argument('--my-option', help='我的选项')
   ```

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   ```bash
   # 检查数据库服务状态
   sudo systemctl status postgresql
   
   # 检查连接参数
   python modern_app.py --debug --db-host localhost
   ```

2. **界面显示异常**
   ```bash
   # 重置窗口大小
   python modern_app.py --window-size 1000x650
   
   # 切换主题
   python modern_app.py --theme light
   ```

3. **依赖安装问题**
   ```bash
   # 升级pip
   python -m pip install --upgrade pip
   
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

## 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下步骤：

### 贡献流程

1. **Fork 项目**
   - 点击右上角的 "Fork" 按钮
   - 克隆你的 fork 到本地

2. **创建功能分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **进行更改**
   - 编写代码
   - 添加测试
   - 更新文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "Add some amazing feature"
   ```

5. **推送到分支**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 描述你的更改
   - 等待代码审查

### 代码规范

- 使用 Python PEP 8 代码风格
- 添加适当的注释和文档字符串
- 编写单元测试
- 确保所有测试通过

### 报告问题

如果你发现了 bug 或有功能建议：

1. 搜索现有的 [Issues](../../issues)
2. 如果没有相关问题，创建新的 [Issue](../../issues/new)
3. 提供详细的描述和复现步骤

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

特别感谢：
- PyQt6 团队提供的优秀GUI框架
- PostgreSQL 社区的数据库支持
- 所有提供反馈和建议的用户

## 📈 更新日志

### v2.0.0 (2025-01-09)
- 🎨 全新现代化界面设计
- ⚙️ 完整的命令行参数支持
- 🗄️ 优化的数据库管理
- 📱 响应式布局设计
- 🔐 增强的安全功能
- 🌍 多语言支持
- 🎯 改进的用户体验

### v1.x.x
- 基础功能实现
- 传统界面设计

---

**现代化网站推荐系统** - 让网站发现变得简单而美好 ✨

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/URL_MANAGE_SYSTEM&type=Date)](https://star-history.com/#yourusername/URL_MANAGE_SYSTEM&Date)