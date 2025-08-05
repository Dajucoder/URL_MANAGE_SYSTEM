#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
增强版数据库初始化脚本
支持用户头像、管理员功能、自定义网站等
"""

import sys
import os
import configparser
import hashlib
from datetime import datetime

try:
    import psycopg2
    from psycopg2 import OperationalError
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("❌ psycopg2 未安装，请运行: pip install psycopg2-binary")
    sys.exit(1)

def load_config():
    """加载配置文件"""
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    
    if os.path.exists(config_file):
        config.read(config_file, encoding='utf-8')
    else:
        print(f"❌ 配置文件 {config_file} 不存在")
        sys.exit(1)
    
    return {
        'host': config.get('database', 'host', fallback='localhost'),
        'port': config.get('database', 'port', fallback='5432'),
        'database': config.get('database', 'database', fallback='user_auth_system'),
        'user': config.get('database', 'user', fallback='postgres'),
        'password': config.get('database', 'password', fallback='yuhaibo123')
    }

def create_connection(db_config):
    """创建数据库连接"""
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            port=int(db_config['port']),
            client_encoding='utf8'
        )
        connection.set_client_encoding('UTF8')
        return connection
    except OperationalError as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

def create_enhanced_tables(connection):
    """创建增强版数据表"""
    
    # 用户表（增强版）
    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        display_name VARCHAR(100),
        avatar_path VARCHAR(255) DEFAULT 'default_avatar.png',
        is_admin BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # 用户自定义网站表
    user_websites_table = """
    CREATE TABLE IF NOT EXISTS user_websites (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        name VARCHAR(200) NOT NULL,
        url VARCHAR(500) NOT NULL,
        description TEXT,
        category VARCHAR(100),
        rating INTEGER DEFAULT 5 CHECK (rating >= 1 AND rating <= 5),
        is_private BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # 系统日志表（管理员功能）
    system_logs_table = """
    CREATE TABLE IF NOT EXISTS system_logs (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        action VARCHAR(100) NOT NULL,
        details TEXT,
        ip_address VARCHAR(45),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # 网站访问统计表
    website_stats_table = """
    CREATE TABLE IF NOT EXISTS website_stats (
        id SERIAL PRIMARY KEY,
        website_name VARCHAR(200) NOT NULL,
        website_url VARCHAR(500) NOT NULL,
        user_id INTEGER REFERENCES users(id),
        visit_count INTEGER DEFAULT 1,
        last_visited TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    tables = [
        ("用户表", users_table),
        ("用户自定义网站表", user_websites_table),
        ("系统日志表", system_logs_table),
        ("网站访问统计表", website_stats_table)
    ]
    
    cursor = connection.cursor()
    
    for table_name, table_sql in tables:
        try:
            cursor.execute(table_sql)
            print(f"✅ {table_name} 创建成功")
        except Exception as e:
            print(f"❌ {table_name} 创建失败: {e}")
            return False
    
    connection.commit()
    cursor.close()
    return True

def create_admin_user(connection):
    """创建默认管理员账户"""
    admin_username = "admin"
    admin_password = "admin123"  # 默认管理员密码
    admin_email = "admin@system.local"
    
    # 检查管理员是否已存在
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (admin_username,))
    
    if cursor.fetchone():
        print("ℹ️ 管理员账户已存在")
        cursor.close()
        return
    
    # 创建管理员账户
    password_hash = hashlib.sha256(admin_password.encode('utf-8')).hexdigest()
    
    insert_sql = """
    INSERT INTO users (username, password_hash, email, display_name, is_admin, created_at) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    try:
        cursor.execute(insert_sql, (
            admin_username,
            password_hash,
            admin_email,
            "系统管理员",
            True,
            datetime.now()
        ))
        connection.commit()
        print("✅ 默认管理员账户创建成功")
        print(f"   用户名: {admin_username}")
        print(f"   密码: {admin_password}")
        print("   ⚠️ 请及时修改默认密码！")
    except Exception as e:
        print(f"❌ 管理员账户创建失败: {e}")
    
    cursor.close()

def create_default_avatars_folder():
    """创建默认头像文件夹"""
    avatars_dir = "assets/avatars"
    
    if not os.path.exists(avatars_dir):
        os.makedirs(avatars_dir, exist_ok=True)
        print(f"✅ 头像文件夹创建成功: {avatars_dir}")
    
    # 创建默认头像说明文件
    readme_content = """# 用户头像文件夹

## 文件说明
- `default_avatar.png` - 默认用户头像
- `admin_avatar.png` - 管理员默认头像
- 用户上传的头像将保存在此文件夹中

## 支持格式
- PNG, JPG, JPEG, GIF
- 建议尺寸: 128x128 像素
- 最大文件大小: 2MB

## 命名规则
- 用户头像: `user_{user_id}_{timestamp}.{ext}`
- 系统头像: `{name}_avatar.{ext}`
"""
    
    readme_path = os.path.join(avatars_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return avatars_dir

def main():
    """主函数"""
    print("🚀 启动增强版数据库初始化...")
    print("=" * 60)
    
    # 加载配置
    print("📋 加载数据库配置...")
    db_config = load_config()
    print(f"   数据库: {db_config['database']}")
    print(f"   主机: {db_config['host']}:{db_config['port']}")
    
    # 连接数据库
    print("🔗 连接数据库...")
    connection = create_connection(db_config)
    if not connection:
        print("❌ 数据库初始化失败")
        return 1
    
    print("✅ 数据库连接成功")
    
    # 创建数据表
    print("📊 创建数据表...")
    if not create_enhanced_tables(connection):
        print("❌ 数据表创建失败")
        connection.close()
        return 1
    
    # 创建管理员账户
    print("👑 创建管理员账户...")
    create_admin_user(connection)
    
    # 创建头像文件夹
    print("🖼️ 创建头像文件夹...")
    avatars_dir = create_default_avatars_folder()
    
    # 关闭连接
    connection.close()
    
    print("=" * 60)
    print("🎉 增强版数据库初始化完成！")
    print()
    print("📋 新增功能:")
    print("   ✅ 用户头像系统")
    print("   ✅ 管理员功能")
    print("   ✅ 用户自定义网站")
    print("   ✅ 系统日志记录")
    print("   ✅ 网站访问统计")
    print()
    print("👑 管理员账户信息:")
    print("   用户名: admin")
    print("   密码: admin123")
    print("   ⚠️ 请及时修改默认密码！")
    print()
    print("🖼️ 头像文件夹:")
    print(f"   路径: {avatars_dir}")
    print("   请将默认头像文件放入此文件夹")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())