@echo off
echo 🚀 准备上传网站推荐系统到 GitHub...
echo.

echo 📋 检查 Git 状态...
git status
echo.

echo 📝 添加所有修改的文件...
git add .
echo.

echo 💾 提交更改...
git commit -m "🎨 v2.1.0: 主题系统重构和关键错误修复

✨ 新功能:
- 重构主题管理系统，支持5种精美主题
- 完善统计数据分析功能
- 优化响应式界面布局

🐛 修复问题:
- 解决主题属性缺失导致的 'text_color' 运行时错误
- 修复 ThemeManager 和 StatisticsManager 导入冲突
- 解决依赖安装编码问题

🔧 技术改进:
- 统一核心管理器架构
- 优化启动流程和性能
- 增强安全认证机制
- 完善项目文档

📚 文档更新:
- 更新 README.md 完整使用指南
- 添加详细的命令行参数说明
- 完善项目结构和配置说明"

echo.
echo 🌐 推送到 GitHub...
git push origin main

echo.
echo ✅ 上传完成！
echo 📖 请查看 GitHub 仓库确认所有文件已正确上传
echo.
pause