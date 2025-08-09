#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全新现代化登录窗口 - 2025年设计标准
采用流体设计、微交互和响应式布局
"""

import sys
import os
import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QMessageBox, QStackedWidget, QFormLayout,
    QToolButton, QGraphicsOpacityEffect, QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, 
    QParallelAnimationGroup, QSequentialAnimationGroup, QRect, QPoint
)
from PyQt6.QtGui import (
    QFont, QPainter, QLinearGradient, QColor, QBrush, QPen,
    QPixmap, QIcon, QFontMetrics
)

from src.core.auth_system import AuthController


class FluidCard(QFrame):
    """流体设计卡片组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("fluid_card")
        self.setup_style()
        self.setup_animations()
    
    def setup_style(self):
        """设置流体卡片样式"""
        self.setStyleSheet("""
            #fluid_card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:0.5 rgba(248, 250, 252, 0.98),
                    stop:1 rgba(241, 245, 249, 0.95));
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 24px;
                backdrop-filter: blur(20px);
            }
        """)
    
    def setup_animations(self):
        """设置卡片动画"""
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(300)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)


class ModernInput(QLineEdit):
    """现代化输入框组件"""
    
    def __init__(self, placeholder="", input_type="text", icon=""):
        super().__init__()
        self.input_type = input_type
        self.icon = icon
        self.is_focused = False
        self.setPlaceholderText(placeholder)
        self.setup_style()
        self.setup_animations()
        
        if input_type == "password":
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self.setup_password_toggle()
    
    def setup_style(self):
        """设置现代化输入框样式"""
        self.setStyleSheet("""
            QLineEdit {
                background: rgba(248, 250, 252, 0.8);
                border: 2px solid rgba(226, 232, 240, 0.6);
                border-radius: 16px;
                padding: 18px 24px 18px 56px;
                font-size: 16px;
                font-weight: 500;
                color: #1e293b;
                selection-background-color: rgba(59, 130, 246, 0.3);
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
            }
            
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                background: rgba(255, 255, 255, 0.95);
                box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
            }
            
            QLineEdit:hover:!focus {
                border: 2px solid rgba(148, 163, 184, 0.8);
                background: rgba(255, 255, 255, 0.9);
            }
            
            QLineEdit::placeholder {
                color: rgba(100, 116, 139, 0.7);
                font-weight: 400;
            }
        """)
        
        # 设置固定高度确保一致性
        self.setFixedHeight(64)
    
    def setup_animations(self):
        """设置输入框动画"""
        self.focus_animation = QPropertyAnimation(self, b"geometry")
        self.focus_animation.setDuration(200)
        self.focus_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def setup_password_toggle(self):
        """设置密码显示切换按钮"""
        self.toggle_btn = QToolButton(self)
        self.toggle_btn.setText("👁")
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                border: none;
                color: #64748b;
                font-size: 18px;
                padding: 8px;
                border-radius: 8px;
            }
            QToolButton:hover {
                background: rgba(148, 163, 184, 0.1);
                color: #475569;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_password_visibility)
        self.position_toggle_button()
    
    def toggle_password_visibility(self):
        """切换密码可见性"""
        if self.echoMode() == QLineEdit.EchoMode.Password:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("🙈")
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("👁")
    
    def position_toggle_button(self):
        """定位切换按钮"""
        btn_size = 32
        margin = 16
        self.toggle_btn.resize(btn_size, btn_size)
        self.toggle_btn.move(
            self.width() - btn_size - margin,
            (self.height() - btn_size) // 2
        )
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        if hasattr(self, 'toggle_btn'):
            self.position_toggle_button()
    
    def paintEvent(self, event):
        """绘制图标"""
        super().paintEvent(event)
        if self.icon:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 绘制图标
            icon_rect = QRect(20, (self.height() - 24) // 2, 24, 24)
            painter.setPen(QPen(QColor(100, 116, 139), 2))
            painter.setFont(QFont("Segoe UI Emoji", 16))
            painter.drawText(icon_rect, Qt.AlignmentFlag.AlignCenter, self.icon)
    
    def focusInEvent(self, event):
        """获得焦点事件"""
        super().focusInEvent(event)
        self.is_focused = True
    
    def focusOutEvent(self, event):
        """失去焦点事件"""
        super().focusOutEvent(event)
        self.is_focused = False


class ModernButton(QPushButton):
    """现代化按钮组件"""
    
    def __init__(self, text, button_style="primary", icon=""):
        super().__init__(text)
        self.button_style = button_style
        self.icon = icon
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_style()
        self.setup_animations()
    
    def setup_style(self):
        """设置按钮样式"""
        if self.button_style == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3b82f6, stop:0.5 #1d4ed8, stop:1 #1e40af);
                    border: none;
                    border-radius: 16px;
                    color: white;
                    font-size: 16px;
                    font-weight: 600;
                    padding: 18px 32px;
                    font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                    letter-spacing: 0.5px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #2563eb, stop:0.5 #1e40af, stop:1 #1e3a8a);
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #1d4ed8, stop:0.5 #1e3a8a, stop:1 #172554);
                    transform: translateY(0px);
                }
                
                QPushButton:disabled {
                    background: #e2e8f0;
                    color: #94a3b8;
                }
            """)
        elif self.button_style == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(248, 250, 252, 0.8);
                    border: 2px solid rgba(226, 232, 240, 0.8);
                    border-radius: 16px;
                    color: #475569;
                    font-size: 16px;
                    font-weight: 500;
                    padding: 18px 32px;
                    font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                }
                
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.95);
                    border-color: #94a3b8;
                    color: #334155;
                    transform: translateY(-1px);
                    box-shadow: 0 6px 20px rgba(148, 163, 184, 0.2);
                }
                
                QPushButton:pressed {
                    background: rgba(241, 245, 249, 0.9);
                    transform: translateY(0px);
                }
            """)
        
        # 设置固定高度
        self.setFixedHeight(64)
    
    def setup_animations(self):
        """设置按钮动画"""
        self.click_animation = QPropertyAnimation(self, b"geometry")
        self.click_animation.setDuration(150)
        self.click_animation.setEasingCurve(QEasingCurve.Type.OutCubic)


class ModernCheckBox(QCheckBox):
    """现代化复选框"""
    
    def __init__(self, text):
        super().__init__(text)
        self.setup_style()
    
    def setup_style(self):
        """设置复选框样式"""
        self.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                font-weight: 500;
                color: #475569;
                spacing: 12px;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #cbd5e1;
                border-radius: 6px;
                background: rgba(248, 250, 252, 0.8);
            }
            
            QCheckBox::indicator:hover {
                border-color: #94a3b8;
                background: rgba(255, 255, 255, 0.9);
            }
            
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #1d4ed8);
                border-color: #3b82f6;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            QCheckBox::indicator:checked:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1e40af);
            }
        """)


class TabButton(QPushButton):
    """现代化选项卡按钮"""
    
    def __init__(self, text, icon=""):
        super().__init__(text)
        self.icon = icon
        self.is_active = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_style()
    
    def setup_style(self):
        """设置选项卡样式"""
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
                color: #64748b;
                font-size: 16px;
                font-weight: 500;
                padding: 16px 24px;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                text-align: left;
            }
            
            QPushButton:hover {
                background: rgba(248, 250, 252, 0.8);
                color: #475569;
            }
        """)
    
    def set_active(self, active):
        """设置激活状态"""
        self.is_active = active
        if active:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(59, 130, 246, 0.1), 
                        stop:1 rgba(29, 78, 216, 0.1));
                    border: 2px solid rgba(59, 130, 246, 0.3);
                    border-radius: 12px;
                    color: #1d4ed8;
                    font-size: 16px;
                    font-weight: 600;
                    padding: 16px 24px;
                    font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(59, 130, 246, 0.15), 
                        stop:1 rgba(29, 78, 216, 0.15));
                    border-color: rgba(59, 130, 246, 0.4);
                }
            """)
        else:
            self.setup_style()


class ModernLoginWindow(QWidget):
    """全新现代化登录窗口"""
    
    # 信号定义
    login_success = pyqtSignal(dict)
    
    def __init__(self, db_manager, config):
        super().__init__()
        self.db_manager = db_manager
        self.config = config
        self.auth_controller = AuthController(db_manager)
        self.current_page = "login"
        
        self.init_ui()
        self.setup_animations()
        self.setup_responsive_design()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("🌐 网站推荐系统 - 现代化登录")
        self.setup_window_properties()
        self.create_layout()
        self.apply_global_styles()
    
    def setup_window_properties(self):
        """设置窗口属性"""
        # 响应式窗口大小
        screen = self.screen().availableGeometry()
        base_width = 1200
        base_height = 800
        
        # 根据屏幕大小调整
        width = min(base_width, int(screen.width() * 0.8))
        height = min(base_height, int(screen.height() * 0.85))
        
        self.setFixedSize(width, height)
        self.center_window()
        
        # 现代化窗口样式
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def create_layout(self):
        """创建布局"""
        # 主容器
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(0)
        
        # 主卡片
        self.main_card = FluidCard()
        card_layout = QHBoxLayout(self.main_card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        # 左侧品牌区域
        left_panel = self.create_brand_panel()
        card_layout.addWidget(left_panel, 2)
        
        # 右侧表单区域
        right_panel = self.create_form_panel()
        card_layout.addWidget(right_panel, 3)
        
        main_layout.addWidget(self.main_card)
        self.setLayout(main_layout)
    
    def create_brand_panel(self):
        """创建品牌展示面板"""
        panel = QWidget()
        panel.setObjectName("brand_panel")
        panel.setStyleSheet("""
            #brand_panel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3b82f6, stop:0.3 #1d4ed8, 
                    stop:0.7 #1e40af, stop:1 #1e3a8a);
                border-top-left-radius: 24px;
                border-bottom-left-radius: 24px;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(48, 64, 48, 64)
        layout.setSpacing(32)
        
        # 品牌标题
        brand_title = QLabel("网站推荐系统")
        brand_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: 700;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                letter-spacing: -0.5px;
            }
        """)
        
        # 品牌副标题
        brand_subtitle = QLabel("现代化 · 智能化 · 个性化")
        brand_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 18px;
                font-weight: 500;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                letter-spacing: 0.5px;
            }
        """)
        
        layout.addStretch(1)
        
        # 品牌图标
        brand_icon = QLabel("🌐")
        brand_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_icon.setStyleSheet("""
            QLabel {
                font-size: 120px;
                margin: 32px 0;
            }
        """)
        
        layout.addWidget(brand_title)
        layout.addWidget(brand_subtitle)
        layout.addWidget(brand_icon)
        layout.addStretch(1)
        
        # 特性列表
        features = ["🔐 安全认证", "⚡ 快速响应", "🎨 现代设计", "📱 响应式布局"]
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            feature_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.8);
                    font-size: 16px;
                    font-weight: 500;
                    font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                    padding: 8px 0;
                }
            """)
            layout.addWidget(feature_label)
        
        layout.addStretch(1)
        return panel
    
    def create_form_panel(self):
        """创建表单面板"""
        panel = QWidget()
        panel.setObjectName("form_panel")
        panel.setStyleSheet("""
            #form_panel {
                background: rgba(255, 255, 255, 0.95);
                border-top-right-radius: 24px;
                border-bottom-right-radius: 24px;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(32)
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 选项卡区域
        tab_area = self.create_tab_area()
        layout.addWidget(tab_area)
        
        # 表单堆栈
        self.form_stack = QStackedWidget()
        self.form_stack.addWidget(self.create_login_form())
        self.form_stack.addWidget(self.create_register_form())
        layout.addWidget(self.form_stack)
        
        layout.addStretch()
        
        # 底部信息
        footer = self.create_footer()
        layout.addWidget(footer)
        
        return panel
    
    def create_toolbar(self):
        """创建顶部工具栏"""
        toolbar = QWidget()
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题
        title = QLabel("欢迎使用")
        title.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 24px;
                font-weight: 600;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
            }
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        
        # 关闭按钮
        close_btn = QToolButton()
        close_btn.setText("✕")
        close_btn.setToolTip("关闭")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QToolButton {
                background: rgba(248, 250, 252, 0.8);
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 8px;
                color: #64748b;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                width: 32px;
                height: 32px;
            }
            QToolButton:hover {
                background: rgba(239, 68, 68, 0.1);
                border-color: rgba(239, 68, 68, 0.3);
                color: #dc2626;
            }
        """)
        
        layout.addWidget(close_btn)
        return toolbar
    
    def create_tab_area(self):
        """创建选项卡区域"""
        tab_area = QWidget()
        layout = QHBoxLayout(tab_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # 登录选项卡
        self.login_tab = TabButton("🔐 登录", "🔐")
        self.login_tab.clicked.connect(lambda: self.switch_tab("login"))
        self.login_tab.set_active(True)
        
        # 注册选项卡
        self.register_tab = TabButton("📝 注册", "📝")
        self.register_tab.clicked.connect(lambda: self.switch_tab("register"))
        
        layout.addWidget(self.login_tab)
        layout.addWidget(self.register_tab)
        layout.addStretch()
        
        return tab_area
    
    def create_login_form(self):
        """创建登录表单"""
        form = QWidget()
        layout = QVBoxLayout(form)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 32, 0, 0)
        
        # 表单标题
        title = QLabel("登录您的账户")
        title.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 20px;
                font-weight: 600;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                margin-bottom: 8px;
            }
        """)
        layout.addWidget(title)
        
        # 用户名输入
        self.username_input = ModernInput("请输入用户名", "text", "👤")
        layout.addWidget(self.username_input)
        
        # 密码输入
        self.password_input = ModernInput("请输入密码", "password", "🔒")
        layout.addWidget(self.password_input)
        
        # 记住登录选项
        options_layout = QHBoxLayout()
        self.remember_checkbox = ModernCheckBox("记住登录状态")
        options_layout.addWidget(self.remember_checkbox)
        options_layout.addStretch()
        
        # 忘记密码链接
        forgot_link = QLabel('<a href="#" style="color: #3b82f6; text-decoration: none;">忘记密码？</a>')
        forgot_link.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
            }
        """)
        options_layout.addWidget(forgot_link)
        
        layout.addLayout(options_layout)
        
        # 登录按钮
        self.login_button = ModernButton("🔐 立即登录", "primary")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        # 游客模式按钮
        guest_button = ModernButton("🧭 游客体验", "secondary")
        guest_button.clicked.connect(self.handle_guest_login)
        layout.addWidget(guest_button)
        
        # 提示信息
        hint = QLabel("💡 默认管理员账户：admin / admin123")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 13px;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                background: rgba(248, 250, 252, 0.8);
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 8px;
                padding: 12px 16px;
                margin-top: 16px;
            }
        """)
        layout.addWidget(hint)
        
        # 回车键登录
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        return form
    
    def create_register_form(self):
        """创建注册表单"""
        form = QWidget()
        layout = QVBoxLayout(form)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 32, 0, 0)
        
        # 表单标题
        title = QLabel("创建新账户")
        title.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 20px;
                font-weight: 600;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                margin-bottom: 8px;
            }
        """)
        layout.addWidget(title)
        
        # 用户名输入
        self.reg_username_input = ModernInput("用户名 (3-50个字符)", "text", "👤")
        layout.addWidget(self.reg_username_input)
        
        # 邮箱输入
        self.reg_email_input = ModernInput("邮箱地址 (可选)", "email", "📧")
        layout.addWidget(self.reg_email_input)
        
        # 密码输入
        self.reg_password_input = ModernInput("密码 (至少6位)", "password", "🔒")
        layout.addWidget(self.reg_password_input)
        
        # 密码强度提示
        self.password_strength_label = QLabel("请输入密码以查看强度")
        self.password_strength_label.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 13px;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                padding: 8px 12px;
                background: transparent;
            }
        """)
        layout.addWidget(self.password_strength_label)
        
        # 确认密码输入
        self.reg_confirm_password_input = ModernInput("确认密码", "password", "🔒")
        layout.addWidget(self.reg_confirm_password_input)
        
        # 注册按钮
        register_button = ModernButton("📝 创建账户", "primary")
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button)
        
        # 提示信息
        hint = QLabel("🎉 注册成功后将自动切换到登录页面")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 13px;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                background: rgba(248, 250, 252, 0.8);
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 8px;
                padding: 12px 16px;
                margin-top: 16px;
            }
        """)
        layout.addWidget(hint)
        
        # 连接密码强度检查
        self.reg_password_input.textChanged.connect(self.update_password_strength)
        
        return form
    
    def create_footer(self):
        """创建底部信息"""
        footer = QWidget()
        layout = QVBoxLayout(footer)
        layout.setSpacing(8)
        
        # 版权信息
        copyright_label = QLabel("© 2025 网站推荐系统 | 现代化界面设计")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setStyleSheet("""
            QLabel {
                color: #94a3b8;
                font-size: 12px;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
            }
        """)
        
        layout.addWidget(copyright_label)
        return footer
    
    def apply_global_styles(self):
        """应用全局样式"""
        self.setStyleSheet("""
            ModernLoginWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 0.1),
                    stop:0.5 rgba(147, 197, 253, 0.1),
                    stop:1 rgba(219, 234, 254, 0.1));
            }
        """)
    
    def setup_animations(self):
        """设置动画效果"""
        # 窗口淡入动画
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(600)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 卡片缩放动画
        self.scale_animation = QPropertyAnimation(self.main_card, b"geometry")
        self.scale_animation.setDuration(400)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
        # 启动动画
        QTimer.singleShot(100, self.fade_animation.start)
    
    def setup_responsive_design(self):
        """设置响应式设计"""
        # 根据窗口大小调整布局
        self.resizeEvent = self.handle_resize
    
    def handle_resize(self, event):
        """处理窗口大小改变"""
        # 响应式调整逻辑
        width = self.width()
        if width < 800:
            # 小屏幕布局调整
            pass
        super().resizeEvent(event)
    
    def switch_tab(self, tab_name):
        """切换选项卡"""
        self.current_page = tab_name
        
        if tab_name == "login":
            self.form_stack.setCurrentIndex(0)
            self.login_tab.set_active(True)
            self.register_tab.set_active(False)
        else:
            self.form_stack.setCurrentIndex(1)
            self.login_tab.set_active(False)
            self.register_tab.set_active(True)
        
        # 添加切换动画
        self.animate_tab_switch()
    
    def animate_tab_switch(self):
        """选项卡切换动画"""
        # 淡出淡入效果
        opacity_effect = QGraphicsOpacityEffect()
        self.form_stack.setGraphicsEffect(opacity_effect)
        
        self.opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        self.opacity_animation.setStartValue(0.3)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.opacity_animation.start()
    
    def handle_login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_modern_message("输入错误", "请输入用户名和密码", "warning")
            return
        
        # 禁用按钮避免重复点击
        self.login_button.setEnabled(False)
        self.login_button.setText("⏳ 正在登录...")
        
        # 执行登录
        success, message, user = self.auth_controller.login(username, password)
        
        if success:
            self.show_modern_message("登录成功", f"欢迎回来，{user['username']}！", "success")
            
            # 保存登录状态
            if self.remember_checkbox.isChecked():
                self.save_login_cache(username)
            
            # 发送登录成功信号
            QTimer.singleShot(1000, lambda: self.login_success.emit(user))
        else:
            self.show_modern_message("登录失败", message, "error")
        
        # 恢复按钮
        self.login_button.setEnabled(True)
        self.login_button.setText("🔐 立即登录")
    
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
            self.show_modern_message("注册成功", message, "success")
            # 清空表单
            self.clear_register_form()
            # 切换到登录页面
            QTimer.singleShot(2000, lambda: self.switch_tab("login"))
        else:
            self.show_modern_message("注册失败", message, "error")
    
    def handle_guest_login(self):
        """处理游客登录"""
        guest_user = {
            'id': 0,
            'username': 'guest',
            'email': None,
            'display_name': '游客',
            'avatar_path': 'default_avatar.png',
            'is_admin': False,
            'created_at': None,
            'last_login': None
        }
        
        self.show_modern_message("游客模式", "已进入游客体验模式", "success")
        QTimer.singleShot(1000, lambda: self.login_success.emit(guest_user))
    
    def update_password_strength(self):
        """更新密码强度"""
        password = self.reg_password_input.text()
        
        if not password:
            self.password_strength_label.setText("请输入密码以查看强度")
            color = "#64748b"
        else:
            try:
                result = self.auth_controller.security_manager.check_password_strength(password)
                if isinstance(result, tuple) and len(result) >= 2:
                    ok, msg = result[0], result[1]
                else:
                    ok, msg = True, "密码强度检查失败"
            except Exception:
                ok, msg = True, "密码强度未知"
            
            self.password_strength_label.setText(msg)
            
            # 根据强度设置颜色
            if "很弱" in msg or "太短" in msg:
                color = "#ef4444"  # 红色
            elif "弱" in msg:
                color = "#f97316"  # 橙色
            elif "中等" in msg:
                color = "#eab308"  # 黄色
            elif "强" in msg or "很强" in msg:
                color = "#22c55e"  # 绿色
            else:
                color = "#64748b"  # 默认灰色
        
        # 更新样式
        self.password_strength_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 13px;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                font-weight: 500;
                padding: 8px 12px;
                background: transparent;
            }}
        """)
    
    def show_modern_message(self, title, message, msg_type="info"):
        """显示现代化消息框"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # 根据消息类型设置图标
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
        
        # 设置现代化样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background: white;
                color: #1e293b;
                font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
                border-radius: 12px;
            }
            
            QMessageBox QLabel {
                color: #1e293b;
                font-size: 14px;
                padding: 16px;
            }
            
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #1d4ed8);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1e40af);
            }
        """)
        
        msg_box.exec()
    
    def save_login_cache(self, username):
        """保存登录缓存"""
        try:
            import json
            cache_dir = os.path.join(os.path.expanduser('~'), '.url_reco_cache')
            os.makedirs(cache_dir, exist_ok=True)
            cache_file = os.path.join(cache_dir, 'login_cache.json')
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({'last_username': username}, f, ensure_ascii=False)
        except Exception:
            pass
    
    def load_login_cache(self):
        """加载登录缓存"""
        try:
            import json
            cache_file = os.path.join(os.path.expanduser('~'), '.url_reco_cache', 'login_cache.json')
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                last_username = data.get('last_username')
                if last_username:
                    self.username_input.setText(last_username)
                    self.remember_checkbox.setChecked(True)
        except Exception:
            pass
    
    def clear_register_form(self):
        """清空注册表单"""
        self.reg_username_input.clear()
        self.reg_email_input.clear()
        self.reg_password_input.clear()
        self.reg_confirm_password_input.clear()
        self.password_strength_label.setText("请输入密码以查看强度")
    
    def center_window(self):
        """窗口居中显示"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def mousePressEvent(self, event):
        """鼠标按下事件 - 用于拖拽窗口"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 拖拽窗口"""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 关闭数据库连接
        if self.db_manager:
            self.db_manager.disconnect()
        event.accept()
    
    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        # 加载登录缓存
        self.load_login_cache()
