#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网站推荐系统 - 主启动文件（简化版）
"""

import sys
import os
import argparse
import locale
from datetime import datetime

# 添加项目根目录和src目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

def get_system_language():
    """获取系统语言"""
    try:
        # 获取系统默认语言，使用更现代的方法
        try:
            system_locale = locale.getlocale()[0]
        except:
            # 如果getlocale失败，尝试使用环境变量
            system_locale = os.environ.get('LANG', 'zh_CN.UTF-8')
        
        if system_locale and ('zh' in system_locale.lower() or 'chinese' in system_locale.lower()):
            return 'zh_CN'
        else:
            return 'en_US'
    except:
        return 'zh_CN'  # 默认使用中文

def check_project_structure():
    """检查项目结构"""
    required_structure = {
        'src/core/auth_system.py': '用户认证系统核心',
        'src/ui/main_window.py': '主界面窗口',
        'src/data/website_data.py': '网站数据管理',
        'requirements.txt': '依赖包列表'
    }
    
    missing_files = []
    for file_path, description in required_structure.items():
        if not os.path.exists(file_path):
            missing_files.append(f"{file_path} ({description})")
    
    return missing_files

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="网站推荐系统启动参数")
    parser.add_argument("--theme", choices=["default", "dark", "light", "nature", "auto"], 
                        default="auto", help="选择界面主题")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--no-animation", action="store_true", help="禁用启动动画")
    parser.add_argument("--backup", action="store_true", help="启动时备份用户数据")
    parser.add_argument("--skip-update-check", action="store_true", help="跳过更新检查")
    parser.add_argument("--language", choices=["zh_CN", "en_US", "auto"], 
                        default="auto", help="选择界面语言")
    parser.add_argument("--portable", action="store_true", 
                        help="便携模式，数据保存在程序目录下")
    parser.add_argument("--reset-config", action="store_true", 
                        help="重置所有配置到默认值")
    
    args = parser.parse_args()
    
    # 处理自动语言选择
    if args.language == "auto":
        args.language = get_system_language()
    
    return args

def create_admin_account(db_manager):
    """创建管理员账户"""
    try:
        import hashlib
        from datetime import datetime
        
        # 检查管理员账户是否已存在
        check_query = "SELECT id FROM users WHERE username = 'admin'"
        result = db_manager.execute_query(check_query)
        
        if not result:
            # 创建管理员账户
            admin_password = "admin123"
            password_hash = hashlib.sha256(admin_password.encode('utf-8')).hexdigest()
            
            insert_query = """
            INSERT INTO users (username, password_hash, email, display_name, is_admin, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            success = db_manager.execute_non_query(insert_query, (
                'admin',
                password_hash,
                'admin@system.local',
                '系统管理员',
                True,
                datetime.now()
            ))
            
            if success:
                print("👑 管理员账户创建成功: admin/admin123")
            else:
                print("⚠️ 管理员账户创建失败")
        else:
            print("👑 管理员账户已存在")
            
    except Exception as e:
        print(f"⚠️ 创建管理员账户时出错: {e}")

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()
    
    print(f"🌐 启动网站推荐系统...")
    print("=" * 60)
    
    # 检查项目结构
    missing_files = check_project_structure()
    if missing_files:
        print("❌ 项目结构不完整，缺少以下文件:")
        for file in missing_files:
            print(f"   • {file}")
        print("\n💡 请确保项目结构完整")
        return 1
    
    print("✅ 项目结构检查通过")
    
    # 导入并启动系统
    try:
        from PyQt6.QtWidgets import QApplication
        from src.core.auth_system import ConfigManager, DatabaseManager, LoginWindow
        
        print("✅ 核心模块导入成功")
        
        # 创建应用程序
        app = QApplication(sys.argv)
        app.setApplicationName("网站推荐系统")
        app.setApplicationVersion("2.0.0")
        
        # 设置应用程序样式
        app.setStyle("Fusion")  # 使用Fusion风格，更现代化
        
        print("✅ PyQt6 应用程序初始化成功")
        
        # 创建配置管理器
        config = ConfigManager()
        db_config = config.get_database_config()
        print("✅ 配置管理器创建成功")
        
        # 创建数据库管理器
        db_manager = DatabaseManager(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            port=int(db_config['port'])
        )
        print("✅ 数据库管理器创建成功")
        
        # 尝试连接数据库
        print("🔗 正在连接数据库...")
        if db_manager.connect():
            print("✅ 数据库连接成功")
            db_manager.create_tables()
            print("📊 数据表创建完成")
            
            # 创建管理员账户（如果不存在）
            create_admin_account(db_manager)
        else:
            print("⚠️ 数据库连接失败，但继续启动...")
        
        # 创建登录窗口
        print("🎨 正在创建登录界面...")
        login_window = LoginWindow(db_manager, config)
        login_window.show()
        
        print("=" * 60)
        print("🚀 网站推荐系统启动成功！")
        print("🎨 深蓝渐变色界面已加载")
        print("🔐 支持用户注册和登录功能")
        print("👑 管理员账户: admin/admin123")
        print("💡 请在界面中注册新用户或使用现有账户登录")
        print("=" * 60)
        
        # 运行应用程序
        return app.exec()
        
    except ImportError as e:
        print(f"❌ 模块导入错误: {e}")
        print("💡 请确保已安装所有依赖: pip install -r requirements.txt")
        print("💡 或检查项目文件结构是否正确")
        return 1
    except Exception as e:
        print(f"❌ 系统启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())