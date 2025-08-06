# 🌐 网站推荐系统

一个功能丰富的网站推荐系统，基于PyQt6开发，提供用户认证、网站管理、主题切换、数据统计等功能。

## ✨ 主要功能

### 🔐 用户认证系统
- **安全登录**: 支持用户名密码登录，带有失败次数限制和账户锁定机制
- **用户注册**: 支持新用户注册，包含邮箱验证和密码强度检查
- **密码安全**: bcrypt加密存储，支持密码强度实时检测
- **登录历史**: 完整记录用户登录历史和统计信息
- **会话管理**: 安全的用户会话管理和自动登出

### 🎨 主题管理系统
- **多主题支持**: 内置5种精美主题
  - 🎨 默认主题 (渐变蓝紫)
  - 🌊 深蓝主题 (专业深蓝)
  - 💜 紫色渐变 (优雅紫色)
  - 🌿 自然绿色 (清新绿色)
  - 🌅 日落橙色 (温暖橙色)
- **实时切换**: 主题切换即时生效，无需重启应用
- **配置持久化**: 主题选择自动保存，下次启动时恢复
- **完整样式**: 支持背景、文字、按钮、卡片等全套UI样式

### 📊 数据统计分析
- **访问统计**: 详细记录网站访问次数和访问频率
- **分类偏好**: 智能分析用户最喜欢的网站分类
- **活动趋势**: 可视化显示最近7天的使用活动趋势
- **会话时间**: 精确统计用户使用时长和在线时间
- **数据可视化**: 进度条和图表直观展示统计数据
- **多维度分析**: 支持按时间、分类、网站等多维度统计

### 🌐 网站管理
- **精选推荐**: 展示高质量网站推荐，支持评分系统
- **智能分类**: 按技术、工具、学习等分类浏览网站
- **快速搜索**: 支持关键词搜索，快速找到目标网站
- **热门排行**: 基于用户访问数据的热门网站推荐
- **响应式布局**: 自适应窗口大小的网站卡片布局
- **一键访问**: 点击即可在浏览器中打开目标网站

### 👤 用户管理
- **个人资料**: 完整的个人信息管理和编辑功能
- **头像系统**: 支持自定义用户头像上传和管理
- **权限管理**: 区分普通用户和管理员权限
- **管理员面板**: 管理员可访问系统管理和用户管理功能
- **用户网站**: 个人网站收藏和管理功能

## 🚀 快速开始

### 环境要求
- Python 3.8+
- PostgreSQL 12+
- Windows/Linux/macOS

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd website-recommendation-system
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置数据库**
   - 安装PostgreSQL数据库
   - 创建数据库 `user_auth_system`
   - 修改 `config.ini` 中的数据库连接信息

4. **启动系统**
```bash
python app.py
```

### 🚀 命令行启动参数

系统支持多种启动参数来自定义运行方式：

```bash
# 基本启动
python app.py

# 选择主题启动
python app.py --theme default          # 默认渐变主题
python app.py --theme dark_blue        # 深蓝专业主题
python app.py --theme purple_gradient  # 紫色渐变主题
python app.py --theme green_nature     # 自然绿色主题
python app.py --theme sunset_orange    # 日落橙色主题

# 调试和性能选项
python app.py --debug                  # 启用调试模式，显示详细日志
python app.py --no-animation          # 禁用启动动画，提升性能

# 数据管理选项
python app.py --backup                # 启动时自动备份数据
python app.py --reset-config          # 重置所有配置到默认值
python app.py --portable              # 便携模式，数据保存在程序目录

# 系统选项
python app.py --skip-update-check     # 跳过启动时的更新检查
python app.py --language zh_CN        # 设置界面语言 (zh_CN/en_US)

# 组合使用多个参数
python app.py --theme dark_blue --debug --no-animation
python app.py --portable --backup --skip-update-check
```

### 🔑 默认管理员账户

系统首次启动时会自动创建管理员账户：
- **用户名**: `admin`
- **密码**: `admin123`
- **权限**: 管理员权限，可访问所有功能

> ⚠️ **安全提示**: 首次登录后请及时修改管理员密码！
# 🌐 网站推荐系统

一个功能丰富的网站推荐系统，基于PyQt6开发，提供用户认证、网站管理、主题切换、数据统计等功能。

## ✨ 主要功能

### 🔐 用户认证系统
- **安全登录**: 支持用户名密码登录，带有失败次数限制
- **账户锁定**: 多次登录失败自动锁定账户，防止暴力破解
- **密码强度检查**: 实时检测密码强度，提供安全建议
- **登录历史**: 记录用户登录历史和统计信息
- **用户注册**: 支持新用户注册，邮箱验证

### 🎨 主题管理系统
- **多主题支持**: 内置4种精美主题
  - 🌊 深蓝主题 (默认)
  - 💜 紫色渐变
  - 🌿 自然绿色
  - 🌅 日落橙色
- **实时切换**: 主题切换即时生效，无需重启
- **设置持久化**: 主题选择自动保存

### 📊 数据统计分析
- **访问统计**: 记录网站访问次数和频率
- **分类偏好**: 分析用户最喜欢的网站分类
- **活动趋势**: 显示最近7天的使用活动
- **会话时间**: 统计用户使用时长
- **可视化展示**: 进度条和图表展示统计数据

### 🌐 网站管理
- **网站推荐**: 展示精选网站推荐
- **分类浏览**: 按分类查看网站
- **搜索功能**: 快速搜索感兴趣的网站
- **热门推荐**: 显示评分最高的网站
- **个人收藏**: 管理个人网站收藏

### 👤 用户管理
- **个人信息**: 查看和编辑个人资料
- **头像管理**: 支持自定义用户头像
- **管理员面板**: 管理员用户可访问系统管理功能

## 🚀 快速开始

### 环境要求
- Python 3.8+
- PostgreSQL 12+
- Windows/Linux/macOS

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd website-recommendation-system
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置数据库**
   - 安装PostgreSQL数据库
   - 创建数据库 `user_auth_system`
   - 修改 `config.ini` 中的数据库连接信息

4. **启动应用**
```bash
python app.py
```

### 命令行参数

系统支持多种启动参数来自定义运行方式：

```bash
# 基本启动
python app.py

# 选择主题 (default, dark_blue, purple_gradient, green_nature, sunset_orange)
python app.py --theme dark_blue

# 启用调试模式
python app.py --debug

# 禁用启动动画（提高性能）
python app.py --no-animation

# 启动时备份数据
python app.py --backup

# 跳过更新检查
python app.py --skip-update-check

# 选择语言 (zh_CN, en_US, auto)
python app.py --language en_US

# 便携模式（数据保存在程序目录）
python app.py --portable

# 重置所有配置到默认值
python app.py --reset-config

# 组合使用多个参数
python app.py --theme dark_blue --debug --no-animation
```

## 📁 项目结构

```
website-recommendation-system/
├── app.py                          # 主启动文件 (命令行启动)
├── config.ini                      # 系统配置文件
├── requirements.txt                 # Python依赖包列表
├── README.md                       # 项目说明文档
├── PROJECT_SUMMARY.md              # 项目总结文档
├── src/                            # 源代码目录
│   ├── core/                       # 核心功能模块
│   │   ├── auth_system.py          # 用户认证系统核心
│   │   └── managers.py             # 主题和统计管理器
│   ├── data/                       # 数据管理模块
│   │   └── website_data.py         # 网站数据和分类管理
│   └── ui/                         # 用户界面模块
│       ├── main_window.py          # 主窗口界面
│       ├── profile_window.py       # 个人信息管理窗口
│       ├── admin_window.py         # 管理员面板窗口
│       └── user_websites_window.py # 用户网站管理窗口
├── config/                         # 配置文件目录
│   ├── theme_config.json           # 主题配置文件
│   └── statistics.json             # 统计数据文件
├── assets/                         # 静态资源文件
│   └── avatars/                    # 用户头像存储
└── docs/                           # 项目文档目录
    ├── API.md                      # API接口文档
    ├── DATABASE.md                 # 数据库设计文档
    ├── DEVELOPMENT.md              # 开发指南文档
    └── CHANGELOG.md                # 版本更新日志
```

## ⚙️ 配置说明

### 数据库配置 (config.ini)
```ini
[database]
host = localhost
port = 5432
database = user_auth_system
user = postgres
password = your_password_here

[application]
window_width = 1200
window_height = 800
remember_login = true
auto_login = false
max_login_attempts = 5
session_timeout = 3600

[ui]
theme = dark_blue
language = zh_CN
animation_enabled = true
```

### 主题配置文件 (config/theme_config.json)
```json
{
  "current_theme": "dark_blue",
  "last_updated": "2024-01-01T12:00:00"
}
```

### 统计数据文件 (config/statistics.json)
```json
{
  "total_visits": 0,
  "favorite_categories": {},
  "daily_activity": {},
  "website_clicks": {},
  "session_time": 0,
  "last_login": null,
  "login_count": 0,
  "search_count": 0,
  "website_visits": {},
  "user_preferences": {},
  "system_performance": {
    "avg_response_time": 0,
    "error_count": 0,
    "uptime": 0
  }
}
```

## 🔧 核心功能详解

### 安全管理器 (SecurityManager)
- **失败尝试记录**: 记录每个用户的登录失败次数
- **账户锁定机制**: 超过最大尝试次数自动锁定
- **密码强度检查**: 检查密码复杂度并提供建议
- **登录历史管理**: 记录成功和失败的登录尝试

### 主题管理器 (ThemeManager)
- **主题定义**: 支持背景、文字、边框等颜色自定义
- **动态切换**: 运行时切换主题无需重启
- **配置持久化**: 主题选择自动保存到配置文件

### 统计管理器 (StatisticsManager)
- **访问记录**: 记录每次网站访问
- **数据分析**: 分析用户行为模式
- **趋势统计**: 生成使用趋势报告
- **数据可视化**: 提供图表展示功能

## 🎯 使用指南

### 首次使用
1. 启动程序后会显示登录界面
2. 点击"注册"选项卡创建新账户
3. 填写用户名、密码等信息完成注册
4. 使用新账户登录系统

### 主要操作
- **浏览网站**: 在主界面选择分类或搜索网站
- **访问网站**: 点击网站卡片上的"访问网站"按钮
- **切换主题**: 点击工具栏的"🎨 主题"按钮
- **查看统计**: 点击工具栏的"📊 统计"按钮
- **个人设置**: 点击"👤 个人信息"管理个人资料

### 管理员功能
- 管理员用户可以访问"👑 管理面板"
- 可以管理系统用户和网站数据
- 查看系统整体使用统计

## 🛠️ 开发说明

### 🔧 技术栈
- **GUI框架**: PyQt6 6.4+ (现代化桌面应用界面)
- **编程语言**: Python 3.8+ (跨平台支持)
- **数据库**: PostgreSQL 12+ (关系型数据库)
- **密码加密**: bcrypt (安全的密码哈希算法)
- **配置管理**: ConfigParser + JSON (灵活的配置系统)
- **数据库连接**: psycopg2 (PostgreSQL适配器)

### 🏗️ 架构设计
- **MVC架构**: 模型-视图-控制器清晰分离
- **模块化设计**: 核心功能模块独立，便于维护和扩展
- **事件驱动**: 基于PyQt6信号槽机制的响应式编程
- **数据持久化**: 多层次数据存储（数据库+本地配置文件）
- **安全设计**: 多重安全机制保护用户数据
- **响应式UI**: 自适应窗口大小的用户界面

### 🚀 扩展开发
1. **添加新主题**: 在 `src/core/managers.py` 的 `ThemeManager.themes` 中定义新主题配色
2. **新增统计功能**: 在 `StatisticsManager` 中添加新的统计逻辑和数据分析
3. **扩展网站数据**: 修改 `src/data/website_data.py` 添加新的网站分类和推荐
4. **自定义界面**: 继承现有窗口类创建新的功能界面
5. **数据库扩展**: 在 `src/core/auth_system.py` 中添加新的数据表和字段

## 🐛 故障排除

### 常见问题

**Q: 数据库连接失败**
A: 检查PostgreSQL服务是否启动，配置文件中的数据库信息是否正确

**Q: 主题切换不生效**
A: 确保 `theme_settings.json` 文件有写入权限

**Q: 统计数据丢失**
A: 检查 `user_statistics.json` 文件是否存在且有读写权限

**Q: 界面显示异常**
A: 确保已安装正确版本的PyQt6，尝试重新安装依赖包

### 日志调试
程序运行时会在控制台输出详细日志信息，包括：
- 数据库连接状态
- 用户登录情况
- 主题切换记录
- 统计数据更新

## 📝 更新日志

### v2.1.0 (2025-01-07) - 最新版本
- 🎨 **主题系统重构**: 完全重写主题管理器，支持5种精美主题
- 🔧 **架构优化**: 重构核心管理器，统一 ThemeManager 和 StatisticsManager
- 🐛 **关键修复**: 解决主题属性缺失导致的 'text_color' 运行时错误
- 📊 **统计增强**: 完善数据统计功能，支持多维度数据分析
- 🚀 **性能提升**: 优化启动流程，提升系统响应速度
- 📱 **界面改进**: 响应式布局优化，支持窗口大小自适应
- 🔒 **安全加固**: 增强用户认证和会话管理安全性
- 📚 **文档完善**: 更新完整的项目文档和使用指南

### v2.0.0 (2024-12-XX)
- ✨ 新增主题管理系统，支持多种内置主题
- 📊 添加完整的数据统计分析功能
- 🔒 增强安全管理，支持账户锁定和密码强度检查
- 🎨 全面优化用户界面，提升用户体验
- 📱 实现响应式布局设计
- 👤 添加个人信息管理和头像系统
- 👑 实现管理员面板和权限管理

### v1.0.0 (2024-11-XX)
- 🎉 项目初始版本发布
- 👤 实现基础用户认证系统
- 🌐 开发网站推荐和管理功能
- 💾 集成 PostgreSQL 数据库支持
- 🖥️ 构建基础 PyQt6 用户界面

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)

---

⭐ 如果这个项目对您有帮助，请给它一个星标！