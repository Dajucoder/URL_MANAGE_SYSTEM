# 贡献指南

感谢您对网站推荐系统项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告问题
- 在提交问题前，请先搜索现有的 Issues
- 使用清晰的标题描述问题
- 提供详细的重现步骤
- 包含系统环境信息（操作系统、Python版本等）

### 提交代码
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范
- 遵循 PEP 8 Python 代码风格
- 添加适当的注释和文档字符串
- 确保代码通过现有测试
- 为新功能添加测试用例

### 提交信息规范
使用以下格式：
```
类型(范围): 简短描述

详细描述（可选）

相关 Issue: #123
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/Dajucoder/URL_MANAGE_SYSTEM.git
cd URL_MANAGE_SYSTEM
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置数据库
```bash
cp config.ini.example config.ini
# 编辑 config.ini 填入数据库配置
```

5. 初始化数据库
```bash
python scripts/init_database_enhanced.py
```

## 联系方式

如有疑问，请通过以下方式联系：
- 创建 Issue
- 发送邮件至项目维护者

再次感谢您的贡献！