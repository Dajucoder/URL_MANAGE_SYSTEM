#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户个人信息界面
支持头像上传、信息修改等功能
"""

import sys
import os
import hashlib
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QFormLayout,
    QGroupBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPainterPath

class AvatarWidget(QLabel):
    """头像显示组件"""
    
    clicked = pyqtSignal()
    
    def __init__(self, size=120):
        super().__init__()
        self.size = size
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 3px solid rgba(255, 255, 255, 0.5);
                border-radius: 60px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QLabel:hover {
                border-color: rgba(255, 255, 255, 0.8);
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.load_default_avatar()
    
    def load_default_avatar(self):
        """加载默认头像"""
        default_path = "assets/avatars/default_avatar.png"
        if os.path.exists(default_path):
            self.load_avatar(default_path)
        else:
            # 创建默认头像文本
            self.setText("👤")
            self.setStyleSheet(self.styleSheet() + """
                QLabel {
                    font-size: 48px;
                    color: rgba(255, 255, 255, 0.8);
                }
            """)
    
    def load_avatar(self, image_path):
        """加载头像图片"""
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # 创建圆形头像
                rounded_pixmap = self.create_rounded_pixmap(pixmap)
                self.setPixmap(rounded_pixmap)
                return True
        return False
    
    def create_rounded_pixmap(self, pixmap):
        """创建圆形头像"""
        size = self.size - 6  # 减去边框宽度
        rounded = QPixmap(size, size)
        rounded.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 创建圆形路径
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        
        # 绘制缩放后的图片
        scaled_pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()
        
        return rounded
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ProfileWindow(QWidget):
    """用户个人信息窗口"""
    
    profile_updated = pyqtSignal(dict)  # 个人信息更新信号
    
    def __init__(self, user_info, db_manager):
        super().__init__()
        self.user_info = user_info
        self.db_manager = db_manager
        self.init_ui()
        self.load_user_data()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle(f"👤 个人信息 - {self.user_info['username']}")
        self.setFixedSize(600, 700)
        self.center_window()
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(25)
        
        # 头像区域
        avatar_group = self.create_avatar_section()
        content_layout.addWidget(avatar_group)
        
        # 基本信息区域
        basic_info_group = self.create_basic_info_section()
        content_layout.addWidget(basic_info_group)
        
        # 账户信息区域
        account_info_group = self.create_account_info_section()
        content_layout.addWidget(account_info_group)
        
        # 操作按钮区域
        button_layout = self.create_button_section()
        content_layout.addLayout(button_layout)
        
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
        # 应用样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a237e, stop:0.3 #283593, stop:0.6 #3949ab, stop:1 #1a237e);
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
                color: white;
            }
            
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: rgba(255, 255, 255, 0.05);
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: white;
            }
            
            QLineEdit, QTextEdit {
                padding: 10px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 14px;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border-color: rgba(255, 255, 255, 0.7);
                background-color: rgba(255, 255, 255, 0.15);
            }
            
            QPushButton {
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: #4CAF50;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            QLabel {
                color: white;
                background: transparent;
            }
            
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
    
    def create_avatar_section(self):
        """创建头像区域"""
        group = QGroupBox("🖼️ 头像设置")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        
        # 头像显示
        self.avatar_widget = AvatarWidget(120)
        self.avatar_widget.clicked.connect(self.change_avatar)
        layout.addWidget(self.avatar_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 头像操作按钮
        avatar_buttons_layout = QHBoxLayout()
        
        change_avatar_btn = QPushButton("📁 更换头像")
        change_avatar_btn.clicked.connect(self.change_avatar)
        
        reset_avatar_btn = QPushButton("🔄 重置头像")
        reset_avatar_btn.clicked.connect(self.reset_avatar)
        reset_avatar_btn.setStyleSheet("QPushButton { background-color: #ff9800; }")
        
        avatar_buttons_layout.addWidget(change_avatar_btn)
        avatar_buttons_layout.addWidget(reset_avatar_btn)
        layout.addLayout(avatar_buttons_layout)
        
        # 提示信息
        # 提示信息
        tip_label = QLabel("💡 点击头像或按钮更换头像\n支持 PNG、JPG、JPEG 格式，最大5MB，建议尺寸 128x128")
        tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tip_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        layout.addWidget(tip_label)
        
        group.setLayout(layout)
        return group
    
    def create_basic_info_section(self):
        """创建基本信息区域"""
        group = QGroupBox("📝 基本信息")
        layout = QFormLayout()
        layout.setSpacing(15)
        
        # 用户名修改
        self.username_input = QLineEdit()
        self.username_input.setText(self.user_info['username'])
        self.username_input.setPlaceholderText("3-50个字符，支持中文、字母、数字、下划线")
        layout.addRow("用户名:", self.username_input)
        
        # 显示名称
        self.display_name_input = QLineEdit()
        self.display_name_input.setPlaceholderText("请输入显示名称")
        layout.addRow("显示名称:", self.display_name_input)
        
        # 邮箱地址
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("请输入邮箱地址")
        layout.addRow("邮箱地址:", self.email_input)
        
        group.setLayout(layout)
        return group
    
    def create_account_info_section(self):
        """创建账户信息区域"""
        group = QGroupBox("🔐 账户信息")
        layout = QFormLayout()
        layout.setSpacing(15)
        
        # 用户名（只读）
        self.username_label = QLabel()
        self.username_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        layout.addRow("用户名:", self.username_label)
        
        # 账户类型
        self.account_type_label = QLabel()
        layout.addRow("账户类型:", self.account_type_label)
        
        # 注册时间
        self.created_time_label = QLabel()
        layout.addRow("注册时间:", self.created_time_label)
        
        # 最后登录
        self.last_login_label = QLabel()
        layout.addRow("最后登录:", self.last_login_label)
        
        # 密码修改区域
        password_frame = QFrame()
        password_layout = QVBoxLayout()
        password_layout.setSpacing(10)
        
        self.old_password_input = QLineEdit()
        self.old_password_input.setPlaceholderText("请输入当前密码")
        self.old_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("请输入新密码（至少6位）")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("请确认新密码")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        change_password_btn = QPushButton("🔒 修改密码")
        change_password_btn.clicked.connect(self.change_password)
        change_password_btn.setStyleSheet("QPushButton { background-color: #2196F3; }")
        
        password_layout.addWidget(QLabel("修改密码:"))
        password_layout.addWidget(self.old_password_input)
        password_layout.addWidget(self.new_password_input)
        password_layout.addWidget(self.confirm_password_input)
        password_layout.addWidget(change_password_btn)
        
        password_frame.setLayout(password_layout)
        layout.addRow(password_frame)
        
        group.setLayout(layout)
        return group
    
    def create_button_section(self):
        """创建操作按钮区域"""
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # 保存按钮
        save_btn = QPushButton("💾 保存信息")
        save_btn.clicked.connect(self.save_profile)
        save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; font-size: 16px; }")
        
        # 取消按钮
        cancel_btn = QPushButton("❌ 取消")
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setStyleSheet("QPushButton { background-color: #f44336; font-size: 16px; }")
        
        layout.addStretch()
        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)
        layout.addStretch()
        
        return layout
    
    def center_window(self):
        """窗口居中显示"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def load_user_data(self):
        """加载用户数据"""
        # 加载基本信息
        self.username_label.setText(self.user_info['username'])
        self.display_name_input.setText(self.user_info.get('display_name', ''))
        self.email_input.setText(self.user_info.get('email', ''))
        
        # 账户类型
        account_type = "👑 管理员" if self.user_info.get('is_admin', False) else "👤 普通用户"
        self.account_type_label.setText(account_type)
        
        # 时间信息
        created_at = self.user_info.get('created_at', '')
        if created_at:
            self.created_time_label.setText(str(created_at).split('.')[0])
        
        last_login = self.user_info.get('last_login', '')
        if last_login:
            self.last_login_label.setText(str(last_login).split('.')[0])
        
        # 加载头像
        avatar_path = self.user_info.get('avatar_path', 'default_avatar.png')
        if avatar_path and avatar_path != 'default_avatar.png':
            full_path = f"assets/avatars/{avatar_path}"
            if not self.avatar_widget.load_avatar(full_path):
                self.avatar_widget.load_default_avatar()
    
    def change_avatar(self):
        """更换头像"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "选择头像图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.gif);;所有文件 (*)"
        )
        
        if file_path:
            # 检查文件大小（限制2MB）
            # 检查文件大小（限制5MB）
            file_size = os.path.getsize(file_path)
            if file_size > 5 * 1024 * 1024:
                QMessageBox.warning(self, "文件过大", "头像文件大小不能超过5MB")
                return
            
            # 生成新的文件名
            file_ext = os.path.splitext(file_path)[1]
            new_filename = f"user_{self.user_info['id']}_{int(datetime.now().timestamp())}{file_ext}"
            new_path = f"assets/avatars/{new_filename}"
            
            # 确保目录存在
            os.makedirs("assets/avatars", exist_ok=True)
            
            # 复制文件
            try:
                import shutil
                shutil.copy2(file_path, new_path)
                
                # 更新头像显示
                if self.avatar_widget.load_avatar(new_path):
                    self.user_info['avatar_path'] = new_filename
                    QMessageBox.information(self, "成功", "头像更换成功！请点击保存信息以确认更改。")
                else:
                    QMessageBox.warning(self, "失败", "头像加载失败，请检查图片格式")
                    
            except Exception as e:
                QMessageBox.critical(self, "错误", f"头像保存失败: {str(e)}")
    
    def reset_avatar(self):
        """重置头像"""
        reply = QMessageBox.question(
            self, "确认重置", 
            "确定要重置为默认头像吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.avatar_widget.load_default_avatar()
            self.user_info['avatar_path'] = 'default_avatar.png'
            QMessageBox.information(self, "成功", "头像已重置为默认头像！请点击保存信息以确认更改。")
    
    def change_password(self):
        """修改密码"""
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # 验证输入
        if not old_password:
            QMessageBox.warning(self, "输入错误", "请输入当前密码")
            return
        
        if len(new_password) < 6:
            QMessageBox.warning(self, "密码太短", "新密码长度至少6位")
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "密码不匹配", "两次输入的新密码不一致")
            return
        
        # 验证当前密码
        old_password_hash = hashlib.sha256(old_password.encode('utf-8')).hexdigest()
        query = "SELECT password_hash FROM users WHERE id = %s"
        result = self.db_manager.execute_query(query, (self.user_info['id'],))
        
        if not result or result[0][0] != old_password_hash:
            QMessageBox.warning(self, "密码错误", "当前密码不正确")
            return
        
        # 更新密码
        new_password_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        update_query = "UPDATE users SET password_hash = %s, updated_at = %s WHERE id = %s"
        
        if self.db_manager.execute_non_query(update_query, (new_password_hash, datetime.now(), self.user_info['id'])):
            QMessageBox.information(self, "成功", "密码修改成功！")
            # 清空密码输入框
            self.old_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
        else:
            QMessageBox.critical(self, "失败", "密码修改失败，请稍后重试")
    
    def save_profile(self):
        """保存个人信息"""
        username = self.username_input.text().strip()
        display_name = self.display_name_input.text().strip()
        email = self.email_input.text().strip()
        avatar_path = self.user_info.get('avatar_path', 'default_avatar.png')
        
        # 验证用户名
        if username != self.user_info['username']:
            # 验证用户名格式
            if not username or len(username) < 3 or len(username) > 50:
                QMessageBox.warning(self, "格式错误", "用户名长度必须在3-50个字符之间")
                return
            
            if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
                QMessageBox.warning(self, "格式错误", "用户名只能包含字母、数字、下划线和中文")
                return
            
            # 检查用户名是否已存在
            query = "SELECT id FROM users WHERE username = %s AND id != %s"
            result = self.db_manager.execute_query(query, (username, self.user_info['id']))
            if result:
                QMessageBox.warning(self, "用户名已存在", "该用户名已被其他用户使用，请选择其他用户名")
                return
        
        # 验证邮箱格式
        if email:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                QMessageBox.warning(self, "格式错误", "邮箱格式不正确")
                return
        
        # 更新数据库
        update_query = """
        UPDATE users SET username = %s, display_name = %s, email = %s, avatar_path = %s, updated_at = %s 
        WHERE id = %s
        """
        
        if self.db_manager.execute_non_query(update_query, (
            username, display_name, email, avatar_path, datetime.now(), self.user_info['id']
        )):
            # 更新用户信息
            self.user_info['username'] = username
            self.user_info['display_name'] = display_name
            self.user_info['email'] = email
            self.user_info['avatar_path'] = avatar_path
            
            # 更新窗口标题
            self.setWindowTitle(f"👤 个人信息 - {username}")
            
            QMessageBox.information(self, "成功", "个人信息保存成功！")
            self.profile_updated.emit(self.user_info)
        else:
            QMessageBox.critical(self, "失败", "个人信息保存失败，请稍后重试")
    
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


if __name__ == "__main__":
    # 测试用的用户信息
    test_user = {
        'id': 1,
        'username': '测试用户',
        'email': 'test@example.com',
        'display_name': '测试显示名',
        'avatar_path': 'default_avatar.png',
        'is_admin': False,
        'created_at': datetime.now(),
        'last_login': datetime.now()
    }
    
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    # 模拟数据库管理器
    class MockDBManager:
        def execute_query(self, query, params=None):
            return [['mock_hash']]
        
        def execute_non_query(self, query, params=None):
            return True
    
    window = ProfileWindow(test_user, MockDBManager())
    window.show()
    sys.exit(app.exec())
