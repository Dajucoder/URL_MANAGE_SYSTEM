#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
登录窗口模块
用户登录和注册界面
"""

import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QMessageBox, QTabWidget, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.core.auth_system import AuthController


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
        self.setWindowTitle("🌐 网站推荐系统 - 用户登录")
        self.setFixedSize(500, 600)
        self.center_window()
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # 系统标题区域
        title_container = QVBoxLayout()
        title_container.setSpacing(8)
        
        title_label = QLabel("🌐 网站推荐系统")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Microsoft YaHei", 20, QFont.Weight.Bold)
        title_label.setFont(title_font)
        
        subtitle_label = QLabel("个性化网站推荐平台")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont("Microsoft YaHei", 11)
        subtitle_label.setFont(subtitle_font)
        
        # 数据库状态指示
        db_connected = self.db_manager.connection is not None
        db_status = "✅ 数据库已连接" if db_connected else "⚠️ 数据库未连接"
        status_label = QLabel(db_status)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_font = QFont("Microsoft YaHei", 10)
        status_label.setFont(status_font)
        
        title_container.addWidget(title_label)
        title_container.addWidget(subtitle_label)
        title_container.addWidget(status_label)
        
        # 功能选项卡
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # 登录选项卡
        login_tab = self.create_login_tab()
        self.tab_widget.addTab(login_tab, "🔐 用户登录")
        
        # 注册选项卡
        register_tab = self.create_register_tab()
        self.tab_widget.addTab(register_tab, "📝 用户注册")
        
        # 添加到主布局
        main_layout.addLayout(title_container)
        main_layout.addWidget(self.tab_widget)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # 深蓝渐变色样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a237e, stop:0.3 #283593, stop:0.6 #3949ab, stop:1 #1a237e);
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
                color: white;
            }
            
            QLabel {
                color: white;
                background: transparent;
            }
            
            QLineEdit {
                padding: 15px 18px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                font-size: 15px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                selection-background-color: rgba(255, 255, 255, 0.3);
                min-height: 20px;
            }
            
            QLineEdit:focus {
                border-color: rgba(255, 255, 255, 0.7);
                background-color: rgba(255, 255, 255, 0.15);
            }
            
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
            
            QPushButton {
                padding: 15px 25px;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:0.5 #45a049, stop:1 #3d8b40);
                min-height: 25px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5CBF60, stop:0.5 #4CAF50, stop:1 #45a049);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:0.5 #3d8b40, stop:1 #2e7d32);
            }
            
            QCheckBox {
                font-size: 13px;
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                padding: 5px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.5);
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
            
            QTabWidget::pane {
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                background-color: rgba(255, 255, 255, 0.05);
                margin-top: 10px;
            }
            
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 12px 25px;
                margin-right: 3px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                font-weight: bold;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.25), stop:1 rgba(255, 255, 255, 0.15));
                color: white;
                border-bottom-color: transparent;
            }
            
            QTabBar::tab:hover {
                background: rgba(255, 255, 255, 0.2);
                color: white;
            }
            
            QFormLayout QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 5px 0;
            }
        """)
    
    def create_login_tab(self):
        """创建登录选项卡"""
        login_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 表单布局
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # 用户名输入
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        form_layout.addRow("👤 用户名:", self.username_input)
        
        # 密码输入
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("🔒 密码:", self.password_input)
        
        # 记住密码复选框
        self.remember_checkbox = QCheckBox("记住登录状态")
        
        # 登录按钮
        login_button = QPushButton("🔐 登录系统")
        login_button.clicked.connect(self.handle_login)
        
        # 回车键登录
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # 提示信息
        hint_label = QLabel("💡 提示：管理员账户 admin/admin123\n如果没有账户，请切换到注册选项卡创建新账户")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_font = QFont("Microsoft YaHei", 10)
        hint_label.setFont(hint_font)
        hint_label.setWordWrap(True)
        
        # 添加到布局
        layout.addLayout(form_layout)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(login_button)
        layout.addWidget(hint_label)
        layout.addStretch()
        
        login_widget.setLayout(layout)
        return login_widget
    
    def create_register_tab(self):
        """创建注册选项卡"""
        register_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 表单布局
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # 用户名输入
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("3-50个字符，支持中文、字母、数字、下划线")
        form_layout.addRow("👤 用户名:", self.reg_username_input)
        
        # 邮箱输入
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("请输入邮箱地址（可选）")
        form_layout.addRow("📧 邮箱:", self.reg_email_input)
        
        # 密码输入
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("至少6位字符")
        self.reg_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("🔒 密码:", self.reg_password_input)
        
        # 确认密码输入
        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setPlaceholderText("请再次输入密码")
        self.reg_confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("🔒 确认密码:", self.reg_confirm_password_input)
        
        # 注册按钮
        register_button = QPushButton("📝 注册新账户")
        register_button.clicked.connect(self.handle_register)
        
        # 提示信息
        hint_label = QLabel("💡 提示：注册成功后请切换到登录选项卡使用新账户登录")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_font = QFont("Microsoft YaHei", 10)
        hint_label.setFont(hint_font)
        hint_label.setWordWrap(True)
        
        # 添加到布局
        layout.addLayout(form_layout)
        layout.addWidget(register_button)
        layout.addWidget(hint_label)
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
        self.remember_checkbox.setChecked(False)
        
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
        if self.db_manager:
            self.db_manager.disconnect()
        event.accept()
