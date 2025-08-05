#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户认证系统核心模块
整合了配置管理、数据库管理和认证控制功能
"""

import sys
import os
import configparser
import hashlib
import re
from datetime import datetime

try:
    import psycopg2
    from psycopg2 import OperationalError, ProgrammingError
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QMessageBox, QTabWidget, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load()
    
    def load(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config.read_file(f)
                print(f"✅ 成功加载配置文件: {self.config_file}")
            else:
                print("📝 配置文件不存在，创建默认配置")
                self.create_default_config()
        except Exception as e:
            print(f"⚠️ 加载配置文件失败: {e}")
            print("📝 使用默认配置")
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置"""
        self.config['database'] = {
            'host': 'localhost',
            'port': '5432',
            'database': 'user_auth_system',
            'user': 'postgres',
            'password': 'your_password_here'
        }
        
        self.config['application'] = {
            'window_width': '450',
            'window_height': '550',
            'remember_login': 'true',
            'auto_login': 'false'
        }
        
        self.config['ui'] = {
            'theme': 'dark_blue',
            'language': 'zh_CN'
        }
        
        self.save()
    
    def save(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            print(f"✅ 配置文件已保存: {self.config_file}")
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
    
    def get_database_config(self):
        """获取数据库配置"""
        if 'database' not in self.config:
            self.create_default_config()
        
        return {
            'host': self.config.get('database', 'host', fallback='localhost'),
            'port': self.config.get('database', 'port', fallback='5432'),
            'database': self.config.get('database', 'database', fallback='user_auth_system'),
            'user': self.config.get('database', 'user', fallback='postgres'),
            'password': self.config.get('database', 'password', fallback='yuhaibo123')
        }


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, host, database, user, password, port=5432):
        self.host = str(host)
        self.database = str(database)
        self.user = str(user)
        self.password = str(password)
        self.port = int(port)
        self.connection = None
    
    def connect(self):
        """连接数据库"""
        if not PSYCOPG2_AVAILABLE:
            print("❌ psycopg2 未安装")
            return False
            
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                client_encoding='utf8',
                connect_timeout=10
            )
            
            self.connection.set_client_encoding('UTF8')
            print("✅ 数据库连接成功")
            return True
            
        except OperationalError as e:
            print(f"❌ 数据库连接错误: {e}")
            return False
        except Exception as e:
            print(f"❌ 数据库连接异常: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("✅ 数据库连接已断开")
    
    def execute_query(self, query, params=None):
        """执行查询"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            try:
                result = cursor.fetchall()
            except psycopg2.ProgrammingError:
                result = []
            
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ 查询执行错误: {e}")
            return []
    
    def execute_non_query(self, query, params=None):
        """执行非查询操作"""
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"❌ 非查询执行错误: {e}")
            return False
    
    def create_tables(self):
        """创建数据表"""
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );
        """
        
        success = self.execute_non_query(users_table)
        if success:
            print("✅ 数据表创建成功")
        else:
            print("❌ 数据表创建失败")
        return success


class AuthController:
    """认证控制器"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def hash_password(self, password):
        """密码哈希"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def validate_username(self, username):
        """验证用户名"""
        if not username or len(username) < 3 or len(username) > 50:
            return False, "用户名长度必须在3-50个字符之间"
        
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
            return False, "用户名只能包含字母、数字、下划线和中文"
        
        # 检查是否为保留用户名
        if username.lower() == 'admin':
            return False, "admin 是系统保留用户名，请选择其他用户名"
        
        return True, ""
    
    def validate_password(self, password):
        """验证密码"""
        if not password or len(password) < 6:
            return False, "密码长度至少6位"
        
        return True, ""
    
    def validate_email(self, email):
        """验证邮箱"""
        if not email:
            return True, ""  # 邮箱是可选的
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "邮箱格式不正确"
        
        return True, ""
    
    def register(self, username, password, confirm_password, email=None):
        """用户注册"""
        # 验证用户名
        valid, message = self.validate_username(username)
        if not valid:
            return False, message
        
        # 验证密码
        valid, message = self.validate_password(password)
        if not valid:
            return False, message
        
        # 确认密码
        if password != confirm_password:
            return False, "两次输入的密码不一致"
        
        # 验证邮箱
        if email:
            valid, message = self.validate_email(email)
            if not valid:
                return False, message
        
        # 检查用户名是否已存在
        query = "SELECT id FROM users WHERE username = %s"
        result = self.db_manager.execute_query(query, (username,))
        if result:
            return False, "用户名已存在"
        
        # 创建用户
        password_hash = self.hash_password(password)
        query = """
        INSERT INTO users (username, password_hash, email, created_at) 
        VALUES (%s, %s, %s, %s)
        """
        
        success = self.db_manager.execute_non_query(
            query, (username, password_hash, email, datetime.now())
        )
        
        if success:
            return True, "🎉 注册成功！请使用新账户登录。"
        else:
            return False, "❌ 注册失败，请稍后重试"
    
    def login(self, username, password):
        """用户登录"""
        if not username or not password:
            return False, "请输入用户名和密码", None
        
        # 查询用户
        query = """
        SELECT id, username, password_hash, email, display_name, avatar_path, is_admin, created_at, last_login 
        FROM users WHERE username = %s
        """
        result = self.db_manager.execute_query(query, (username,))
        
        if not result:
            return False, "用户名不存在", None
        
        user_data = result[0]
        stored_password_hash = user_data[2]
        
        # 验证密码
        if self.hash_password(password) != stored_password_hash:
            return False, "密码错误", None
        
        # 更新最后登录时间
        update_query = "UPDATE users SET last_login = %s WHERE username = %s"
        self.db_manager.execute_non_query(update_query, (datetime.now(), username))
        
        # 构建用户信息
        user = {
            'id': user_data[0],
            'username': user_data[1],
            'email': user_data[3],
            'display_name': user_data[4],
            'avatar_path': user_data[5],
            'is_admin': user_data[6],
            'created_at': user_data[7],
            'last_login': datetime.now()
        }
        
        return True, f"🎉 欢迎回来，{username}！", user


class LoginWindow(QWidget):
    """登录窗口"""
    
    def __init__(self, db_manager, config):
        super().__init__()
        self.db_manager = db_manager
        self.config = config
        self.auth_controller = AuthController(db_manager)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("🎨 网站推荐系统 - 用户登录")
        # 设置响应式布局，支持最小和最大尺寸
        self.setMinimumSize(800, 500)
        self.setMaximumSize(1200, 800)
        self.resize(1000, 650)
        self.center_window()
        
        # 主布局 - 水平分割，支持响应式
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 左侧欢迎区域 - 使用比例而非固定宽度
        welcome_widget = self.create_welcome_section()
        welcome_widget.setMinimumWidth(350)
        welcome_widget.setMaximumWidth(500)
        
        # 右侧表单区域 - 使用比例而非固定宽度
        form_widget = self.create_form_section()
        form_widget.setMinimumWidth(450)
        form_widget.setMaximumWidth(700)
        
        # 添加到布局，设置拉伸比例
        main_layout.addWidget(welcome_widget, 2)  # 左侧占2份
        main_layout.addWidget(form_widget, 3)     # 右侧占3份
        
        self.setLayout(main_layout)
        
        # 现代化样式
        self.setStyleSheet("""
            QWidget {
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
            }
            
            #welcome_section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4facfe, stop:0.5 #00f2fe, stop:1 #43e97b);
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;
            }
            
            #form_section {
                background-color: white;
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
            
            #welcome_title {
                color: white;
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            
            #welcome_subtitle {
                color: rgba(255, 255, 255, 0.9);
                font-size: 18px;
                line-height: 1.6;
            }
            
            #form_title {
                color: #333;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 40px;
            }
            
            QLineEdit {
                padding: 1.2em 1em;
                border: 2px solid #e1e5e9;
                border-radius: 0.6em;
                font-size: 1em;
                background-color: white;
                color: #333;
                margin-bottom: 1.2em;
                min-height: 1.5em;
            }
            
            QLineEdit:focus {
                border-color: #4facfe;
                outline: none;
            }
            
            QLineEdit::placeholder {
                color: #999;
            }
            
            QPushButton {
                padding: 1.2em 1.5em;
                border: none;
                border-radius: 0.6em;
                font-size: 1.1em;
                font-weight: bold;
                color: white;
                background-color: #333;
                margin-top: 1em;
                min-height: 1.8em;
            }
            
            QPushButton:hover {
                background-color: #555;
            }
            
            QPushButton:pressed {
                background-color: #222;
            }
            
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            
            QTabBar::tab {
                background: transparent;
                color: #666;
                padding: 15px 25px;
                margin-right: 15px;
                border: none;
                font-size: 18px;
                font-weight: bold;
            }
            
            QTabBar::tab:selected {
                color: #333;
                border-bottom: 3px solid #4facfe;
            }
            
            QTabBar::tab:hover {
                color: #4facfe;
            }
            
            QLabel {
                color: #333;
                font-size: 16px;
                margin-bottom: 8px;
                font-weight: bold;
            }
            
            #close_btn {
                background: transparent;
                color: #666;
                font-size: 24px;
                padding: 8px;
                border: none;
                border-radius: 20px;
                width: 40px;
                height: 40px;
            }
            
            #close_btn:hover {
                background-color: rgba(0, 0, 0, 0.1);
                color: #333;
            }
            
            #status_label {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-top: 20px;
            }
        """)
    
    def create_welcome_section(self):
        """创建左侧欢迎区域"""
        welcome_widget = QWidget()
        welcome_widget.setObjectName("welcome_section")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 100, 60, 100)
        layout.setSpacing(40)
        
        # 欢迎标题
        title_label = QLabel("网站推荐系统")
        title_label.setObjectName("welcome_title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # 欢迎副标题
        subtitle_label = QLabel("发现精彩网站\n开启数字世界之旅")
        subtitle_label.setObjectName("welcome_subtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        subtitle_label.setWordWrap(True)
        
        # 数据库状态指示
        db_connected = self.db_manager.connection is not None
        db_status = "✅ 数据库已连接" if db_connected else "⚠️ 数据库未连接"
        status_label = QLabel(db_status)
        status_label.setObjectName("status_label")
        status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addStretch()
        layout.addWidget(status_label)
        
        welcome_widget.setLayout(layout)
        return welcome_widget
    
    def create_form_section(self):
        """创建右侧表单区域"""
        form_widget = QWidget()
        form_widget.setObjectName("form_section")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)
        
        # 顶部关闭按钮
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        close_btn = QPushButton("×")
        close_btn.setObjectName("close_btn")
        close_btn.clicked.connect(self.close)
        top_layout.addWidget(close_btn)
        
        # 功能选项卡
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # 登录选项卡
        login_tab = self.create_login_tab()
        self.tab_widget.addTab(login_tab, "登录")
        
        # 注册选项卡
        register_tab = self.create_register_tab()
        self.tab_widget.addTab(register_tab, "注册")
        
        layout.addLayout(top_layout)
        layout.addWidget(self.tab_widget)
        layout.addStretch()
        
        form_widget.setLayout(layout)
        return form_widget
    
    def create_login_tab(self):
        """创建登录选项卡"""
        login_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(0, 30, 0, 30)
        
        # 用户名输入
        username_label = QLabel("账号：")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        
        # 密码输入
        password_label = QLabel("密码：")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 登录按钮
        login_button = QPushButton("登录")
        login_button.clicked.connect(self.handle_login)
        
        # 回车键登录
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # 添加到布局
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addStretch()
        
        login_widget.setLayout(layout)
        return login_widget
    
    def create_register_tab(self):
        """创建注册选项卡"""
        register_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 30, 0, 30)
        
        # 用户名输入
        username_label = QLabel("账号：")
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("3-50个字符，支持中文、字母、数字、下划线")
        
        # 邮箱输入
        email_label = QLabel("邮箱：")
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("请输入邮箱地址（可选）")
        
        # 密码输入
        password_label = QLabel("密码：")
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("至少6位字符")
        self.reg_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 确认密码输入
        confirm_password_label = QLabel("确认密码：")
        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setPlaceholderText("请再次输入密码")
        self.reg_confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 注册按钮
        register_button = QPushButton("注册")
        register_button.clicked.connect(self.handle_register)
        
        # 添加到布局
        layout.addWidget(username_label)
        layout.addWidget(self.reg_username_input)
        layout.addWidget(email_label)
        layout.addWidget(self.reg_email_input)
        layout.addWidget(password_label)
        layout.addWidget(self.reg_password_input)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.reg_confirm_password_input)
        layout.addWidget(register_button)
        layout.addStretch()
        
        register_widget.setLayout(layout)
        return register_widget
    
    def center_window(self):
        """窗口居中显示"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def handle_login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_message("输入错误", "请输入用户名和密码", QMessageBox.Icon.Warning)
            return
        
        # 执行登录
        success, message, user = self.auth_controller.login(username, password)
        
        if success:
            print(f"🎉 用户 {user['username']} 登录成功！")
            print(f"📧 邮箱: {user.get('email', '未设置')}")
            print(f"📅 注册时间: {user['created_at']}")
            
            # 隐藏登录窗口
            self.hide()
            
            # 打开主窗口
            self.open_main_window(user)
        else:
            self.show_message("登录失败", message, QMessageBox.Icon.Critical)
    
    def open_main_window(self, user_info):
        """打开主窗口"""
        try:
            from src.ui.main_window import MainWindow
            
            self.main_window = MainWindow(user_info)
            self.main_window.logout_requested.connect(self.handle_logout_from_main)
            self.main_window.show()
            
            print("🏠 主窗口已打开")
            
        except ImportError as e:
            print(f"❌ 导入主窗口失败: {e}")
            self.show_message("错误", "无法打开主窗口，请检查main_window.py文件", QMessageBox.Icon.Critical)
            self.show()
        except Exception as e:
            print(f"❌ 打开主窗口失败: {e}")
            self.show_message("错误", f"打开主窗口时发生错误: {str(e)}", QMessageBox.Icon.Critical)
            self.show()
    
    def handle_logout_from_main(self):
        """处理从主窗口发出的登出请求"""
        print("🔄 用户请求登出，返回登录界面")
        
        # 关闭主窗口
        if hasattr(self, 'main_window'):
            try:
                self.main_window.hide()
                self.main_window.close()
                self.main_window.deleteLater()
                delattr(self, 'main_window')
            except Exception as e:
                print(f"⚠️ 关闭主窗口时出现问题: {e}")
        
        # 清空登录表单
        self.username_input.clear()
        self.password_input.clear()
        
        # 重新显示登录窗口
        self.show()
        self.raise_()
        self.activateWindow()
    
    def handle_register(self):
        """处理注册"""
        username = self.reg_username_input.text().strip()
        email = self.reg_email_input.text().strip()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()
        
        # 执行注册
        success, message = self.auth_controller.register(
            username, password, confirm_password, email if email else None
        )
        
        if success:
            self.show_message("注册成功", message, QMessageBox.Icon.Information)
            # 清空注册表单
            self.reg_username_input.clear()
            self.reg_email_input.clear()
            self.reg_password_input.clear()
            self.reg_confirm_password_input.clear()
            # 切换到登录选项卡
            self.tab_widget.setCurrentIndex(0)
            print(f"🎉 新用户 {username} 注册成功！")
        else:
            self.show_message("注册失败", message, QMessageBox.Icon.Critical)
    
    def show_message(self, title, message, icon):
        """显示消息框"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        
        # 设置消息框样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
                color: white;
                font-family: 'Microsoft YaHei';
            }
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        msg_box.exec()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        event.accept()