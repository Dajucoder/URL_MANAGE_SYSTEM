#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
现代化网站推荐系统
支持完整的命令行参数配置和启动选项
"""

import sys
import os
import argparse
import configparser
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.auth_system import DatabaseManager, ConfigManager
from src.ui.modern_login_window import ModernLoginWindow


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='现代化网站推荐系统 - 发现精彩网站，开启数字世界之旅',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python modern_app.py                           # 使用默认配置启动
  python modern_app.py --config custom.ini      # 使用自定义配置文件
  python modern_app.py --db-host localhost      # 指定数据库主机
  python modern_app.py --db-port 5432           # 指定数据库端口
  python modern_app.py --window-size 1200x800   # 设置窗口大小
  python modern_app.py --theme dark             # 设置界面主题
  python modern_app.py --debug                  # 启用调试模式
  python modern_app.py --version                # 显示版本信息
        """
    )
    
    # 基本选项
    parser.add_argument('--version', action='version', version='现代化网站推荐系统 v2.0.0')
    parser.add_argument('--config', '-c', default='config.ini', 
                       help='配置文件路径 (默认: config.ini)')
    parser.add_argument('--debug', action='store_true', 
                       help='启用调试模式，显示详细日志')
    
    # 数据库配置
    db_group = parser.add_argument_group('数据库配置')
    db_group.add_argument('--db-host', help='数据库主机地址')
    db_group.add_argument('--db-port', type=int, help='数据库端口')
    db_group.add_argument('--db-name', help='数据库名称')
    db_group.add_argument('--db-user', help='数据库用户名')
    db_group.add_argument('--db-password', help='数据库密码')
    
    # 界面配置
    ui_group = parser.add_argument_group('界面配置')
    ui_group.add_argument('--window-size', help='窗口大小 (格式: 宽度x高度, 如: 1200x800)')
    ui_group.add_argument('--theme', choices=['light', 'dark', 'auto'], 
                         help='界面主题 (light/dark/auto)')
    ui_group.add_argument('--font-size', type=int, help='字体大小')
    ui_group.add_argument('--language', choices=['zh-CN', 'en-US'], 
                         help='界面语言')
    
    # 功能选项
    feature_group = parser.add_argument_group('功能选项')
    feature_group.add_argument('--auto-login', help='自动登录用户名')
    feature_group.add_argument('--fullscreen', action='store_true', 
                              help='全屏模式启动')
    feature_group.add_argument('--no-splash', action='store_true', 
                              help='跳过启动画面')
    
    return parser.parse_args()


def setup_application(args):
    """设置应用程序"""
    app = QApplication(sys.argv)
    app.setApplicationName("现代化网站推荐系统")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Modern Web Recommendation")
    
    # PyQt6 默认启用高DPI支持，无需手动设置
    pass
    
    # 设置全局字体
    font_size = args.font_size if args.font_size else 10
    font = QFont("Inter", font_size)
    if not font.exactMatch():
        font = QFont("SF Pro Display", font_size)
        if not font.exactMatch():
            font = QFont("Microsoft YaHei UI", font_size)
    app.setFont(font)
    
    return app


def load_config_with_args(args):
    """根据命令行参数加载配置"""
    config_manager = ConfigManager(args.config)
    
    # 如果指定了数据库参数，覆盖配置文件中的设置
    if any([args.db_host, args.db_port, args.db_name, args.db_user, args.db_password]):
        if 'database' not in config_manager.config:
            config_manager.config.add_section('database')
        
        if args.db_host:
            config_manager.config.set('database', 'host', args.db_host)
        if args.db_port:
            config_manager.config.set('database', 'port', str(args.db_port))
        if args.db_name:
            config_manager.config.set('database', 'database', args.db_name)
        if args.db_user:
            config_manager.config.set('database', 'user', args.db_user)
        if args.db_password:
            config_manager.config.set('database', 'password', args.db_password)
        
        # 保存更新的配置
        config_manager.save()
    
    # 处理界面配置
    if any([args.window_size, args.theme, args.language]):
        if 'ui' not in config_manager.config:
            config_manager.config.add_section('ui')
        
        if args.window_size:
            try:
                width, height = args.window_size.split('x')
                config_manager.config.set('ui', 'window_width', width)
                config_manager.config.set('ui', 'window_height', height)
            except ValueError:
                print(f"⚠️ 窗口大小格式错误: {args.window_size}，应为 宽度x高度")
        
        if args.theme:
            config_manager.config.set('ui', 'theme', args.theme)
        
        if args.language:
            config_manager.config.set('ui', 'language', args.language)
        
        config_manager.save()
    
    return config_manager


def print_startup_info(args):
    """打印启动信息"""
    print("🌐 现代化网站推荐系统 v2.0.0")
    print("🎨 全新流体设计界面")
    print("=" * 60)
    
    if args.debug:
        print("🔍 调试模式已启用")
        print(f"📁 配置文件: {args.config}")
        if args.db_host:
            print(f"🗄️ 数据库主机: {args.db_host}")
        if args.db_port:
            print(f"🔌 数据库端口: {args.db_port}")
        if args.window_size:
            print(f"📐 窗口大小: {args.window_size}")
        if args.theme:
            print(f"🎨 界面主题: {args.theme}")
        print("-" * 60)


def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_arguments()
        
        # 打印启动信息
        print_startup_info(args)
        
        # 创建应用程序
        app = setup_application(args)
        
        # 加载配置
        print("✅ 正在加载配置...")
        config_manager = load_config_with_args(args)
        
        # 初始化数据库管理器
        print("✅ 正在初始化数据库...")
        db_config = config_manager.get_database_config()
        
        if args.debug:
            print(f"🔍 数据库配置: {db_config['host']}:{db_config['port']}/{db_config['database']}")
        
        db_manager = DatabaseManager(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            port=int(db_config['port'])
        )
        
        # 连接数据库
        print("🔗 正在连接数据库...")
        if db_manager.connect():
            print("✅ 数据库连接成功")
            
            # 创建数据表
            if db_manager.create_tables():
                print("✅ 数据表创建成功")
            
            print("👑 管理员账户已准备就绪")
        else:
            print("⚠️ 数据库连接失败，使用离线模式")
        
        # 创建现代化登录窗口
        print("🎨 正在创建现代化登录界面...")
        login_window = ModernLoginWindow(db_manager, config_manager)
        
        # 应用窗口大小设置
        if args.window_size:
            try:
                width, height = map(int, args.window_size.split('x'))
                login_window.resize(width, height)
            except ValueError:
                if args.debug:
                    print(f"⚠️ 窗口大小设置失败: {args.window_size}")
        
        # 全屏模式
        if args.fullscreen:
            login_window.showFullScreen()
        
        # 连接登录成功信号
        def on_login_success(user_info):
            """登录成功处理"""
            print(f"🎉 用户 {user_info['username']} 登录成功！")
            login_window.hide()
            
            # 打开主窗口
            try:
                from src.ui.main_window import MainWindow
                main_window = MainWindow(user_info)
                
                # 应用窗口设置
                if args.window_size:
                    try:
                        width, height = map(int, args.window_size.split('x'))
                        main_window.resize(width, height)
                    except ValueError:
                        pass
                
                if args.fullscreen:
                    main_window.showFullScreen()
                else:
                    main_window.show()
                
                # 连接登出信号
                if hasattr(main_window, 'logout_requested'):
                    main_window.logout_requested.connect(lambda: show_login_window(login_window))
                
            except ImportError:
                print("⚠️ 主窗口模块未找到，保持登录窗口显示")
                login_window.show()
        
        def show_login_window(window):
            """显示登录窗口"""
            window.show()
            window.raise_()
            window.activateWindow()
        
        login_window.login_success.connect(on_login_success)
        
        # 自动登录处理
        if args.auto_login:
            print(f"🔄 尝试自动登录用户: {args.auto_login}")
            # 这里可以添加自动登录逻辑
        
        # 显示登录窗口
        if not args.no_splash:
            login_window.show()
        
        print("=" * 60)
        print("🚀 现代化网站推荐系统启动成功！")
        print("🎨 全新流体设计界面已加载")
        print("🔐 支持用户注册和登录功能")
        print("👑 管理员账户: admin/admin123")
        print("💡 请在界面中注册新用户或使用现有账户登录")
        if args.debug:
            print("🔍 调试模式已启用，显示详细信息")
        print("=" * 60)
        
        # 运行应用程序
        sys.exit(app.exec())
        
    except KeyboardInterrupt:
        print("\n🔌 用户中断，正在退出...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        if args.debug if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()