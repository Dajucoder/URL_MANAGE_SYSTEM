#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口模块 - 网站推荐系统
用户登录后的主界面
"""

import sys
import os
import webbrowser
import json
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QLineEdit, QComboBox, QMessageBox,
    QGridLayout, QTextEdit, QSplitter, QProgressBar, QTabWidget,
    QDialog, QDialogButtonBox, QSlider, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPainter, QPainterPath, QColor

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.data.website_data import (
    get_all_categories, get_websites_by_category, 
    get_all_websites, search_websites, get_top_rated_websites
)
from src.core.managers import ThemeManager, StatisticsManager


class ThemeSettingsDialog(QDialog):
    """主题设置对话框"""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("🎨 主题设置")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("选择您喜欢的主题")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 主题选择
        themes = self.theme_manager.get_available_themes()
        for theme_key, theme_name in themes.items():
            button = QPushButton(f"🎨 {theme_name}")
            button.setFixedHeight(50)
            button.clicked.connect(lambda checked, key=theme_key: self.select_theme(key))
            
            # 当前主题高亮
            if theme_key == self.theme_manager.current_theme:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: 2px solid #45a049;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #333;
                        border: 1px solid #ccc;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)
            
            layout.addWidget(button)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def select_theme(self, theme_key):
        """选择主题"""
        if self.theme_manager.set_theme(theme_key):
            self.theme_changed.emit(theme_key)
            self.accept()


class WebsiteCard(QFrame):
    """网站卡片组件"""
    
    def __init__(self, website_data):
        super().__init__()
        self.website_data = website_data
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setFixedSize(380, 200)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 网站名称
        name_label = QLabel(self.website_data['name'])
        name_font = QFont("Microsoft YaHei", 12, QFont.Weight.Bold)
        name_label.setFont(name_font)
        name_label.setWordWrap(True)
        
        # 网站描述
        desc_label = QLabel(self.website_data['description'])
        desc_font = QFont("Microsoft YaHei", 10)
        desc_label.setFont(desc_font)
        desc_label.setWordWrap(True)
        desc_label.setMaximumHeight(60)
        desc_label.setMinimumHeight(60)
        
        # 分类和评分
        info_layout = QHBoxLayout()
        category_label = QLabel(f"分类: {self.website_data['category']}")
        rating_label = QLabel(f"评分: {'⭐' * self.website_data['rating']}")
        
        info_layout.addWidget(category_label)
        info_layout.addStretch()
        info_layout.addWidget(rating_label)
        
        # 访问按钮
        visit_button = QPushButton("🌐 访问网站")
        visit_button.clicked.connect(self.visit_website)
        
        layout.addWidget(name_label)
        layout.addWidget(desc_label)
        layout.addLayout(info_layout)
        layout.addWidget(visit_button)
        
        self.setLayout(layout)
        
        # 卡片样式
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                margin: 5px;
            }
            QFrame:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.5);
            }
            QLabel {
                color: white;
                background: transparent;
                border: none;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    
    def visit_website(self):
        """访问网站"""
        try:
            webbrowser.open(self.website_data['url'])
            print(f"🌐 正在打开网站: {self.website_data['name']}")
            
            # 记录网站访问统计
            if hasattr(self.parent(), 'stats_manager'):
                category = self.website_data.get('category', '未分类')
                self.parent().stats_manager.record_website_visit(
                    self.website_data['name'], category
                )
        except Exception as e:
            print(f"❌ 打开网站失败: {e}")
    
    def update_theme(self, theme):
        """更新主题"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {theme['card_bg']};
                border: 2px solid {theme['card_border']};
                border-radius: 10px;
                margin: 5px;
            }}
            QFrame:hover {{
                background-color: rgba(255, 255, 255, 0.15);
                border-color: {theme['accent_color']};
            }}
            QLabel {{
                color: {theme['text_color']};
                background: transparent;
                border: none;
            }}
            QPushButton {{
                background-color: {theme['accent_color']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(76, 175, 80, 0.8);
            }}
        """)


class MainWindow(QWidget):
    """主窗口类"""
    
    logout_requested = pyqtSignal()
    
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.current_websites = []
        self.theme_manager = ThemeManager()
        self.stats_manager = StatisticsManager()
        self.session_start_time = datetime.now()
        
        # 设置定时器更新会话时间
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_time)
        self.session_timer.start(60000)  # 每分钟更新一次
        
        self.init_ui()
        self.apply_current_theme()
        self.load_all_websites()
        
    def load_user_avatar(self):
        """加载用户头像"""
        try:
            avatar_path = self.user_info.get('avatar_path', 'default_avatar.png')
            full_path = f"assets/avatars/{avatar_path}"
            
            if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                # 创建圆形头像
                rounded_pixmap = self.create_rounded_avatar(pixmap)
                self.user_avatar.setPixmap(rounded_pixmap)
            else:
                # 设置默认头像
                self.user_avatar.setText("👤")
                self.user_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.user_avatar.setStyleSheet("""
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    border: 2px solid white;
                    color: white;
                    font-size: 16px;
                """)
        except Exception as e:
            print(f"❌ 加载用户头像失败: {e}")
            
    def create_rounded_avatar(self, pixmap):
        """创建圆形头像"""
        if pixmap.isNull():
            return pixmap
            
        size = min(32, 32)
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
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle(f"🌐 网站推荐系统 - 欢迎 {self.user_info['username']}")
        self.setGeometry(100, 100, 1200, 800)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部工具栏
        toolbar_layout = self.create_toolbar()
        main_layout.addLayout(toolbar_layout)
        
        # 内容区域
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧分类面板
        category_panel = self.create_category_panel()
        content_splitter.addWidget(category_panel)
        
        # 右侧网站展示区域
        website_area = self.create_website_area()
        content_splitter.addWidget(website_area)
        
        # 设置分割比例
        content_splitter.setSizes([250, 950])
        main_layout.addWidget(content_splitter)
        
        self.setLayout(main_layout)
    
    def apply_current_theme(self):
        """应用当前主题"""
        theme = self.theme_manager.get_current_theme()
        
        self.setStyleSheet(f"""
            QWidget {{
                background: {theme['background']};
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
                color: {theme['text_color']};
            }}
            
            QLineEdit {{
                padding: 10px;
                border: 2px solid {theme['card_border']};
                border-radius: 8px;
                background-color: {theme['card_bg']};
                color: {theme['text_color']};
                font-size: 14px;
            }}
            
            QLineEdit:focus {{
                border-color: {theme['accent_color']};
                background-color: rgba(255, 255, 255, 0.15);
            }}
            
            QPushButton {{
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: {theme['accent_color']};
            }}
            
            QPushButton:hover {{
                background-color: rgba(76, 175, 80, 0.8);
            }}
            
            QComboBox {{
                padding: 8px;
                border: 2px solid {theme['card_border']};
                border-radius: 8px;
                background-color: {theme['card_bg']};
                color: {theme['text_color']};
                font-size: 14px;
            }}
            
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            
            QLabel {{
                color: {theme['text_color']};
                background: transparent;
            }}
            
            QFrame {{
                background-color: {theme['card_bg']};
                border: 2px solid {theme['card_border']};
                border-radius: 10px;
            }}
            
            QFrame:hover {{
                background-color: rgba(255, 255, 255, 0.15);
                border-color: {theme['accent_color']};
            }}
        """)
        
        # 更新网站卡片样式
        for card in self.findChildren(WebsiteCard):
            card.update_theme(theme)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar_layout = QHBoxLayout()
        
        # 用户信息区域（头像和用户名）
        user_info_layout = QHBoxLayout()
        user_info_layout.setSpacing(10)
        
        # 用户头像
        self.user_avatar = QLabel()
        self.user_avatar.setFixedSize(32, 32)
        self.user_avatar.setScaledContents(True)
        self.user_avatar.setStyleSheet("border-radius: 16px; border: 2px solid white;")
        self.load_user_avatar()
        user_info_layout.addWidget(self.user_avatar)
        
        # 用户名
        user_label = QLabel(f"👤 当前用户: {self.user_info.get('display_name', self.user_info['username'])}")
        user_font = QFont("Microsoft YaHei", 12, QFont.Weight.Bold)
        user_label.setFont(user_font)
        user_info_layout.addWidget(user_label)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索网站...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self.search_websites)
        
        # 功能按钮区域
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # 主题切换按钮
        theme_btn = QPushButton("🎨 主题")
        theme_btn.clicked.connect(self.open_theme_settings)
        theme_btn.setStyleSheet("background-color: #9C27B0;")
        
        # 统计面板按钮
        stats_btn = QPushButton("📊 统计")
        stats_btn.clicked.connect(self.show_statistics)
        stats_btn.setStyleSheet("background-color: #FF5722;")
        
        # 个人信息按钮
        profile_btn = QPushButton("👤 个人信息")
        profile_btn.clicked.connect(self.open_profile)
        profile_btn.setStyleSheet("background-color: #2196F3;")
        
        # 我的网站按钮
        my_websites_btn = QPushButton("🌐 我的网站")
        my_websites_btn.clicked.connect(self.open_my_websites)
        my_websites_btn.setStyleSheet("background-color: #4CAF50;")
        
        # 管理员按钮（仅管理员可见）
        if self.user_info.get('is_admin', False):
            admin_btn = QPushButton("👑 管理面板")
            admin_btn.clicked.connect(self.open_admin_panel)
            admin_btn.setStyleSheet("background-color: #FF9800;")
            buttons_layout.addWidget(admin_btn)
        
        # 登出按钮
        logout_button = QPushButton("🚪 登出")
        logout_button.clicked.connect(self.handle_logout)
        logout_button.setStyleSheet("background-color: #f44336;")
        
        buttons_layout.addWidget(theme_btn)
        buttons_layout.addWidget(stats_btn)
        buttons_layout.addWidget(profile_btn)
        buttons_layout.addWidget(my_websites_btn)
        buttons_layout.addWidget(logout_button)
        
        toolbar_layout.addLayout(user_info_layout)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addLayout(buttons_layout)
        
        return toolbar_layout
    
    def create_category_panel(self):
        """创建分类面板"""
        panel = QFrame()
        panel.setMaximumWidth(250)
        panel.setFrameStyle(QFrame.Shape.Box)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 标题
        title_label = QLabel("📂 网站分类")
        title_font = QFont("Microsoft YaHei", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 全部网站按钮
        all_button = QPushButton("🌐 全部网站")
        all_button.clicked.connect(self.load_all_websites)
        layout.addWidget(all_button)
        
        # 热门推荐按钮
        top_button = QPushButton("🔥 热门推荐")
        top_button.clicked.connect(self.load_top_websites)
        layout.addWidget(top_button)
        
        # 分类按钮
        categories = get_all_categories()
        for category in categories:
            button = QPushButton(f"📁 {category}")
            button.clicked.connect(lambda checked, cat=category: self.load_category_websites(cat))
            layout.addWidget(button)
        
        layout.addStretch()
        panel.setLayout(layout)
        
        panel.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
        """)
        
        return panel
    
    def create_website_area(self):
        """创建网站展示区域"""
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 网站容器
        self.website_container = QWidget()
        self.website_layout = QGridLayout()
        self.website_layout.setSpacing(15)
        self.website_container.setLayout(self.website_layout)
        
        scroll_area.setWidget(self.website_container)
        
        return scroll_area
    
    def load_all_websites(self):
        """加载所有网站"""
        self.current_websites = get_all_websites()
        self.update_website_display("🌐 所有推荐网站")
    
    def load_top_websites(self):
        """加载热门网站"""
        self.current_websites = get_top_rated_websites(12)
        self.update_website_display("🔥 热门推荐网站")
    
    def load_category_websites(self, category):
        """加载分类网站"""
        websites = get_websites_by_category(category)
        self.current_websites = []
        for website in websites:
            website_copy = website.copy()
            website_copy['category_group'] = category
            self.current_websites.append(website_copy)
        self.update_website_display(f"📁 {category}")
    
    def search_websites(self):
        """搜索网站"""
        keyword = self.search_input.text().strip()
        if keyword:
            self.current_websites = search_websites(keyword)
            self.update_website_display(f"🔍 搜索结果: {keyword}")
        else:
            self.load_all_websites()
    
    def update_website_display(self, title):
        """更新网站显示"""
        # 清空现有内容
        for i in reversed(range(self.website_layout.count())):
            child = self.website_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # 计算每行卡片数量（根据窗口宽度自适应）
        window_width = self.width()
        card_width = 400  # 卡片宽度 + 间距
        available_width = window_width - 300  # 减去左侧面板宽度
        cols_per_row = max(1, min(4, available_width // card_width))  # 最少1个，最多4个
        
        # 添加标题
        title_label = QLabel(title)
        title_font = QFont("Microsoft YaHei", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("padding: 20px; font-size: 18px;")
        self.website_layout.addWidget(title_label, 0, 0, 1, cols_per_row)
        
        # 添加网站卡片
        if not self.current_websites:
            no_result_label = QLabel("😔 没有找到相关网站")
            no_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_result_label.setStyleSheet("padding: 40px; font-size: 16px; color: rgba(255, 255, 255, 0.7);")
            self.website_layout.addWidget(no_result_label, 1, 0, 1, cols_per_row)
        else:
            row = 1
            col = 0
            for website in self.current_websites:
                card = WebsiteCard(website)
                self.website_layout.addWidget(card, row, col)
                
                col += 1
                if col >= cols_per_row:  # 根据窗口宽度自适应
                    col = 0
                    row += 1
        
        # 添加底部间距
        spacer_label = QLabel("")
        spacer_label.setMinimumHeight(50)
        self.website_layout.addWidget(spacer_label, row + 1, 0, 1, cols_per_row)
    
    def handle_logout(self):
        """处理登出"""
        reply = QMessageBox.question(
            self, "确认登出", 
            "确定要登出当前账户吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            print(f"👋 用户 {self.user_info['username']} 已登出")
            self._logout_confirmed = True
            self.logout_requested.emit()
            self.close()  # 确保主窗口关闭
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 延迟更新布局，避免频繁重绘
        if hasattr(self, 'current_websites') and self.current_websites:
            # 使用定时器延迟更新，避免拖拽时频繁刷新
            if not hasattr(self, '_resize_timer'):
                from PyQt6.QtCore import QTimer
                self._resize_timer = QTimer()
                self._resize_timer.setSingleShot(True)
                self._resize_timer.timeout.connect(self._delayed_layout_update)
            
            self._resize_timer.start(200)  # 200ms延迟
    
    def _delayed_layout_update(self):
        """延迟的布局更新"""
        if hasattr(self, 'current_websites') and self.current_websites:
            # 重新计算并更新当前显示
            current_title = "🌐 网站推荐"  # 默认标题
            self.update_website_display(current_title)
    
    def create_database_manager(self):
        """创建数据库管理器实例"""
        try:
            from src.core.auth_system import ConfigManager, DatabaseManager
            
            config = ConfigManager()
            db_config = config.get_database_config()
            
            db_manager = DatabaseManager(
                host=db_config['host'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password'],
                port=int(db_config['port'])
            )
            
            if db_manager.connect():
                return db_manager
            else:
                raise Exception("数据库连接失败")
                
        except Exception as e:
            raise Exception(f"创建数据库管理器失败: {str(e)}")
    
    def open_profile(self):
        """打开个人信息界面"""
        try:
            from src.ui.profile_window import ProfileWindow
            
            # 创建数据库管理器
            db_manager = self.create_database_manager()
            
            # 创建个人信息窗口
            self.profile_window = ProfileWindow(self.user_info, db_manager)
            self.profile_window.profile_updated.connect(self.on_profile_updated)
            self.profile_window.show()
            
            print("👤 个人信息窗口已打开")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开个人信息界面: {str(e)}")
            print(f"❌ 打开个人信息界面失败: {e}")
    
    def open_my_websites(self):
        """打开我的网站管理界面"""
        try:
            from src.ui.user_websites_window import UserWebsitesWindow
            
            # 创建数据库管理器
            db_manager = self.create_database_manager()
            
            # 创建用户网站管理窗口
            self.user_websites_window = UserWebsitesWindow(self.user_info, db_manager)
            self.user_websites_window.show()
            
            print("🌐 用户网站管理窗口已打开")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开网站管理界面: {str(e)}")
            print(f"❌ 打开网站管理界面失败: {e}")
    
    def open_admin_panel(self):
        """打开管理员面板"""
        if not self.user_info.get('is_admin', False):
            QMessageBox.warning(self, "权限不足", "只有管理员才能访问管理面板")
            return
        
        try:
            from src.ui.admin_window import AdminWindow
            
            # 创建数据库管理器
            db_manager = self.create_database_manager()
            
            # 创建管理员窗口
            self.admin_window = AdminWindow(self.user_info, db_manager)
            self.admin_window.show()
            
            print("👑 管理员面板已打开")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开管理员面板: {str(e)}")
            print(f"❌ 打开管理员面板失败: {e}")
    
    def on_profile_updated(self, updated_info):
        """处理个人信息更新"""
        # 更新本地用户信息
        self.user_info.update(updated_info)
        
        # 更新界面显示
        self.setWindowTitle(f"🌐 网站推荐系统 - 欢迎 {self.user_info['username']}")
        
        # 更新头像
        self.load_user_avatar()
        
        # 如果工具栏中有用户标签，也需要更新
        for child in self.findChildren(QLabel):
            if child.text().startswith("👤 当前用户:"):
                display_name = self.user_info.get('display_name', self.user_info['username'])
                child.setText(f"👤 当前用户: {display_name}")
                break
        
        print(f"✅ 用户信息已更新: {self.user_info['username']}")
    
    def open_theme_settings(self):
        """打开主题设置"""
        dialog = ThemeSettingsDialog(self.theme_manager, self)
        dialog.theme_changed.connect(self.on_theme_changed)
        dialog.exec()
    
    def on_theme_changed(self, theme_name):
        """主题改变时的处理"""
        self.apply_current_theme()
        print(f"🎨 主题已切换为: {self.theme_manager.get_current_theme()['name']}")
    
    def show_statistics(self):
        """显示统计信息"""
        stats_dialog = StatisticsDialog(self.stats_manager, self)
        stats_dialog.exec()
    
    def update_session_time(self):
        """更新会话时间"""
        session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60
        # 确保统计数据结构存在
        if 'session_time' not in self.stats_manager.stats_data:
            self.stats_manager.stats_data['session_time'] = 0
        self.stats_manager.stats_data['session_time'] += 1  # 每分钟增加1分钟
        self.stats_manager.save_statistics()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口模块 - 网站推荐系统
用户登录后的主界面
"""

import sys
import os
import webbrowser
import json
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QLineEdit, QComboBox, QMessageBox,
    QGridLayout, QTextEdit, QSplitter, QProgressBar, QTabWidget,
    QDialog, QDialogButtonBox, QSlider, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPainter, QPainterPath, QColor

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.data.website_data import (
    get_all_categories, get_websites_by_category, 
    get_all_websites, search_websites, get_top_rated_websites
)
from src.core.managers import ThemeManager, StatisticsManager


class ThemeSettingsDialog(QDialog):
    """主题设置对话框"""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("🎨 主题设置")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("选择您喜欢的主题")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 主题选择
        themes = self.theme_manager.get_available_themes()
        for theme_key, theme_name in themes.items():
            button = QPushButton(f"🎨 {theme_name}")
            button.setFixedHeight(50)
            button.clicked.connect(lambda checked, key=theme_key: self.select_theme(key))
            
            # 当前主题高亮
            if theme_key == self.theme_manager.current_theme:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: 2px solid #45a049;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #333;
                        border: 1px solid #ccc;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)
            
            layout.addWidget(button)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def select_theme(self, theme_key):
        """选择主题"""
        if self.theme_manager.set_theme(theme_key):
            self.theme_changed.emit(theme_key)
            self.accept()


class WebsiteCard(QFrame):
    """网站卡片组件"""
    
    def __init__(self, website_data):
        super().__init__()
        self.website_data = website_data
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setFixedSize(380, 200)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 网站名称
        name_label = QLabel(self.website_data['name'])
        name_font = QFont("Microsoft YaHei", 12, QFont.Weight.Bold)
        name_label.setFont(name_font)
        name_label.setWordWrap(True)
        
        # 网站描述
        desc_label = QLabel(self.website_data['description'])
        desc_font = QFont("Microsoft YaHei", 10)
        desc_label.setFont(desc_font)
        desc_label.setWordWrap(True)
        desc_label.setMaximumHeight(60)
        desc_label.setMinimumHeight(60)
        
        # 分类和评分
        info_layout = QHBoxLayout()
        category_label = QLabel(f"分类: {self.website_data['category']}")
        rating_label = QLabel(f"评分: {'⭐' * self.website_data['rating']}")
        
        info_layout.addWidget(category_label)
        info_layout.addStretch()
        info_layout.addWidget(rating_label)
        
        # 访问按钮
        visit_button = QPushButton("🌐 访问网站")
        visit_button.clicked.connect(self.visit_website)
        
        layout.addWidget(name_label)
        layout.addWidget(desc_label)
        layout.addLayout(info_layout)
        layout.addWidget(visit_button)
        
        self.setLayout(layout)
        
        # 卡片样式
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                margin: 5px;
            }
            QFrame:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.5);
            }
            QLabel {
                color: white;
                background: transparent;
                border: none;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    
    def visit_website(self):
        """访问网站"""
        try:
            webbrowser.open(self.website_data['url'])
            print(f"🌐 正在打开网站: {self.website_data['name']}")
            
            # 记录网站访问统计
            if hasattr(self.parent(), 'stats_manager'):
                category = self.website_data.get('category', '未分类')
                self.parent().stats_manager.record_website_visit(
                    self.website_data['name'], category
                )
        except Exception as e:
            print(f"❌ 打开网站失败: {e}")
    
    def update_theme(self, theme):
        """更新主题"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {theme['card_bg']};
                border: 2px solid {theme['card_border']};
                border-radius: 10px;
                margin: 5px;
            }}
            QFrame:hover {{
                background-color: rgba(255, 255, 255, 0.15);
                border-color: {theme['accent_color']};
            }}
            QLabel {{
                color: {theme['text_color']};
                background: transparent;
                border: none;
            }}
            QPushButton {{
                background-color: {theme['accent_color']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(76, 175, 80, 0.8);
            }}
        """)


class MainWindow(QWidget):
    """主窗口类"""
    
    logout_requested = pyqtSignal()
    
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.current_websites = []
        self.theme_manager = ThemeManager()
        self.stats_manager = StatisticsManager()
        self.session_start_time = datetime.now()
        
        # 设置定时器更新会话时间
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_time)
        self.session_timer.start(60000)  # 每分钟更新一次
        
        self.init_ui()
        self.apply_current_theme()
        self.load_all_websites()
        
    def load_user_avatar(self):
        """加载用户头像"""
        try:
            avatar_path = self.user_info.get('avatar_path', 'default_avatar.png')
            full_path = f"assets/avatars/{avatar_path}"
            
            if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                # 创建圆形头像
                rounded_pixmap = self.create_rounded_avatar(pixmap)
                self.user_avatar.setPixmap(rounded_pixmap)
            else:
                # 设置默认头像
                self.user_avatar.setText("👤")
                self.user_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.user_avatar.setStyleSheet("""
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    border: 2px solid white;
                    color: white;
                    font-size: 16px;
                """)
        except Exception as e:
            print(f"❌ 加载用户头像失败: {e}")
            
    def create_rounded_avatar(self, pixmap):
        """创建圆形头像"""
        if pixmap.isNull():
            return pixmap
            
        size = min(32, 32)
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
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle(f"🌐 网站推荐系统 - 欢迎 {self.user_info['username']}")
        self.setGeometry(100, 100, 1200, 800)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部工具栏
        toolbar_layout = self.create_toolbar()
        main_layout.addLayout(toolbar_layout)
        
        # 内容区域
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧分类面板
        category_panel = self.create_category_panel()
        content_splitter.addWidget(category_panel)
        
        # 右侧网站展示区域
        website_area = self.create_website_area()
        content_splitter.addWidget(website_area)
        
        # 设置分割比例
        content_splitter.setSizes([250, 950])
        main_layout.addWidget(content_splitter)
        
        self.setLayout(main_layout)
    
    def apply_current_theme(self):
        """应用当前主题"""
        theme = self.theme_manager.get_current_theme()
        
        self.setStyleSheet(f"""
            QWidget {{
                background: {theme['background']};
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
                color: {theme['text_color']};
            }}
            
            QLineEdit {{
                padding: 10px;
                border: 2px solid {theme['card_border']};
                border-radius: 8px;
                background-color: {theme['card_bg']};
                color: {theme['text_color']};
                font-size: 14px;
            }}
            
            QLineEdit:focus {{
                border-color: {theme['accent_color']};
                background-color: rgba(255, 255, 255, 0.15);
            }}
            
            QPushButton {{
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: {theme['accent_color']};
            }}
            
            QPushButton:hover {{
                background-color: rgba(76, 175, 80, 0.8);
            }}
            
            QComboBox {{
                padding: 8px;
                border: 2px solid {theme['card_border']};
                border-radius: 8px;
                background-color: {theme['card_bg']};
                color: {theme['text_color']};
                font-size: 14px;
            }}
            
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            
            QLabel {{
                color: {theme['text_color']};
                background: transparent;
            }}
            
            QFrame {{
                background-color: {theme['card_bg']};
                border: 2px solid {theme['card_border']};
                border-radius: 10px;
            }}
            
            QFrame:hover {{
                background-color: rgba(255, 255, 255, 0.15);
                border-color: {theme['accent_color']};
            }}
        """)
        
        # 更新网站卡片样式
        for card in self.findChildren(WebsiteCard):
            card.update_theme(theme)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar_layout = QHBoxLayout()
        
        # 用户信息区域（头像和用户名）
        user_info_layout = QHBoxLayout()
        user_info_layout.setSpacing(10)
        
        # 用户头像
        self.user_avatar = QLabel()
        self.user_avatar.setFixedSize(32, 32)
        self.user_avatar.setScaledContents(True)
        self.user_avatar.setStyleSheet("border-radius: 16px; border: 2px solid white;")
        self.load_user_avatar()
        user_info_layout.addWidget(self.user_avatar)
        
        # 用户名
        user_label = QLabel(f"👤 当前用户: {self.user_info.get('display_name', self.user_info['username'])}")
        user_font = QFont("Microsoft YaHei", 12, QFont.Weight.Bold)
        user_label.setFont(user_font)
        user_info_layout.addWidget(user_label)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索网站...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self.search_websites)
        
        # 功能按钮区域
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # 主题切换按钮
        theme_btn = QPushButton("🎨 主题")
        theme_btn.clicked.connect(self.open_theme_settings)
        theme_btn.setStyleSheet("background-color: #9C27B0;")
        
        # 统计面板按钮
        stats_btn = QPushButton("📊 统计")
        stats_btn.clicked.connect(self.show_statistics)
        stats_btn.setStyleSheet("background-color: #FF5722;")
        
        # 个人信息按钮
        profile_btn = QPushButton("👤 个人信息")
        profile_btn.clicked.connect(self.open_profile)
        profile_btn.setStyleSheet("background-color: #2196F3;")
        
        # 我的网站按钮
        my_websites_btn = QPushButton("🌐 我的网站")
        my_websites_btn.clicked.connect(self.open_my_websites)
        my_websites_btn.setStyleSheet("background-color: #4CAF50;")
        
        # 管理员按钮（仅管理员可见）
        if self.user_info.get('is_admin', False):
            admin_btn = QPushButton("👑 管理面板")
            admin_btn.clicked.connect(self.open_admin_panel)
            admin_btn.setStyleSheet("background-color: #FF9800;")
            buttons_layout.addWidget(admin_btn)
        
        # 登出按钮
        logout_button = QPushButton("🚪 登出")
        logout_button.clicked.connect(self.handle_logout)
        logout_button.setStyleSheet("background-color: #f44336;")
        
        buttons_layout.addWidget(theme_btn)
        buttons_layout.addWidget(stats_btn)
        buttons_layout.addWidget(profile_btn)
        buttons_layout.addWidget(my_websites_btn)
        buttons_layout.addWidget(logout_button)
        
        toolbar_layout.addLayout(user_info_layout)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addLayout(buttons_layout)
        
        return toolbar_layout
    
    def create_category_panel(self):
        """创建分类面板"""
        panel = QFrame()
        panel.setMaximumWidth(250)
        panel.setFrameStyle(QFrame.Shape.Box)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 标题
        title_label = QLabel("📂 网站分类")
        title_font = QFont("Microsoft YaHei", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 全部网站按钮
        all_button = QPushButton("🌐 全部网站")
        all_button.clicked.connect(self.load_all_websites)
        layout.addWidget(all_button)
        
        # 热门推荐按钮
        top_button = QPushButton("🔥 热门推荐")
        top_button.clicked.connect(self.load_top_websites)
        layout.addWidget(top_button)
        
        # 分类按钮
        categories = get_all_categories()
        for category in categories:
            button = QPushButton(f"📁 {category}")
            button.clicked.connect(lambda checked, cat=category: self.load_category_websites(cat))
            layout.addWidget(button)
        
        layout.addStretch()
        panel.setLayout(layout)
        
        panel.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
        """)
        
        return panel
    
    def create_website_area(self):
        """创建网站展示区域"""
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 网站容器
        self.website_container = QWidget()
        self.website_layout = QGridLayout()
        self.website_layout.setSpacing(15)
        self.website_container.setLayout(self.website_layout)
        
        scroll_area.setWidget(self.website_container)
        
        return scroll_area
    
    def load_all_websites(self):
        """加载所有网站"""
        self.current_websites = get_all_websites()
        self.update_website_display("🌐 所有推荐网站")
    
    def load_top_websites(self):
        """加载热门网站"""
        self.current_websites = get_top_rated_websites(12)
        self.update_website_display("🔥 热门推荐网站")
    
    def load_category_websites(self, category):
        """加载分类网站"""
        websites = get_websites_by_category(category)
        self.current_websites = []
        for website in websites:
            website_copy = website.copy()
            website_copy['category_group'] = category
            self.current_websites.append(website_copy)
        self.update_website_display(f"📁 {category}")
    
    def search_websites(self):
        """搜索网站"""
        keyword = self.search_input.text().strip()
        if keyword:
            self.current_websites = search_websites(keyword)
            self.update_website_display(f"🔍 搜索结果: {keyword}")
        else:
            self.load_all_websites()
    
    def update_website_display(self, title):
        """更新网站显示"""
        # 清空现有内容
        for i in reversed(range(self.website_layout.count())):
            child = self.website_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # 计算每行卡片数量（根据窗口宽度自适应）
        window_width = self.width()
        card_width = 400  # 卡片宽度 + 间距
        available_width = window_width - 300  # 减去左侧面板宽度
        cols_per_row = max(1, min(4, available_width // card_width))  # 最少1个，最多4个
        
        # 添加标题
        title_label = QLabel(title)
        title_font = QFont("Microsoft YaHei", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("padding: 20px; font-size: 18px;")
        self.website_layout.addWidget(title_label, 0, 0, 1, cols_per_row)
        
        # 添加网站卡片
        if not self.current_websites:
            no_result_label = QLabel("😔 没有找到相关网站")
            no_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_result_label.setStyleSheet("padding: 40px; font-size: 16px; color: rgba(255, 255, 255, 0.7);")
            self.website_layout.addWidget(no_result_label, 1, 0, 1, cols_per_row)
        else:
            row = 1
            col = 0
            for website in self.current_websites:
                card = WebsiteCard(website)
                self.website_layout.addWidget(card, row, col)
                
                col += 1
                if col >= cols_per_row:  # 根据窗口宽度自适应
                    col = 0
                    row += 1
        
        # 添加底部间距
        spacer_label = QLabel("")
        spacer_label.setMinimumHeight(50)
        self.website_layout.addWidget(spacer_label, row + 1, 0, 1, cols_per_row)
    
    def handle_logout(self):
        """处理登出"""
        reply = QMessageBox.question(
            self, "确认登出", 
            "确定要登出当前账户吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            print(f"👋 用户 {self.user_info['username']} 已登出")
            self._logout_confirmed = True
            self.logout_requested.emit()
            self.close()  # 确保主窗口关闭
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 延迟更新布局，避免频繁重绘
        if hasattr(self, 'current_websites') and self.current_websites:
            # 使用定时器延迟更新，避免拖拽时频繁刷新
            if not hasattr(self, '_resize_timer'):
                from PyQt6.QtCore import QTimer
                self._resize_timer = QTimer()
                self._resize_timer.setSingleShot(True)
                self._resize_timer.timeout.connect(self._delayed_layout_update)
            
            self._resize_timer.start(200)  # 200ms延迟
    
    def _delayed_layout_update(self):
        """延迟的布局更新"""
        if hasattr(self, 'current_websites') and self.current_websites:
            # 重新计算并更新当前显示
            current_title = "🌐 网站推荐"  # 默认标题
            self.update_website_display(current_title)
    
    def create_database_manager(self):
        """创建数据库管理器实例"""
        try:
            from src.core.auth_system import ConfigManager, DatabaseManager
            
            config = ConfigManager()
            db_config = config.get_database_config()
            
            db_manager = DatabaseManager(
                host=db_config['host'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password'],
                port=int(db_config['port'])
            )
            
            if db_manager.connect():
                return db_manager
            else:
                raise Exception("数据库连接失败")
                
        except Exception as e:
            raise Exception(f"创建数据库管理器失败: {str(e)}")
    
    def open_profile(self):
        """打开个人信息界面"""
        try:
            from src.ui.profile_window import ProfileWindow
            
            # 创建数据库管理器
            db_manager = self.create_database_manager()
            
            # 创建个人信息窗口
            self.profile_window = ProfileWindow(self.user_info, db_manager)
            self.profile_window.profile_updated.connect(self.on_profile_updated)
            self.profile_window.show()
            
            print("👤 个人信息窗口已打开")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开个人信息界面: {str(e)}")
            print(f"❌ 打开个人信息界面失败: {e}")
    
    def open_my_websites(self):
        """打开我的网站管理界面"""
        try:
            from src.ui.user_websites_window import UserWebsitesWindow
            
            # 创建数据库管理器
            db_manager = self.create_database_manager()
            
            # 创建用户网站管理窗口
            self.user_websites_window = UserWebsitesWindow(self.user_info, db_manager)
            self.user_websites_window.show()
            
            print("🌐 用户网站管理窗口已打开")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开网站管理界面: {str(e)}")
            print(f"❌ 打开网站管理界面失败: {e}")
    
    def open_admin_panel(self):
        """打开管理员面板"""
        if not self.user_info.get('is_admin', False):
            QMessageBox.warning(self, "权限不足", "只有管理员才能访问管理面板")
            return
        
        try:
            from src.ui.admin_window import AdminWindow
            
            # 创建数据库管理器
            db_manager = self.create_database_manager()
            
            # 创建管理员窗口
            self.admin_window = AdminWindow(self.user_info, db_manager)
            self.admin_window.show()
            
            print("👑 管理员面板已打开")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开管理员面板: {str(e)}")
            print(f"❌ 打开管理员面板失败: {e}")
    
    def on_profile_updated(self, updated_info):
        """处理个人信息更新"""
        # 更新本地用户信息
        self.user_info.update(updated_info)
        
        # 更新界面显示
        self.setWindowTitle(f"🌐 网站推荐系统 - 欢迎 {self.user_info['username']}")
        
        # 更新头像
        self.load_user_avatar()
        
        # 如果工具栏中有用户标签，也需要更新
        for child in self.findChildren(QLabel):
            if child.text().startswith("👤 当前用户:"):
                display_name = self.user_info.get('display_name', self.user_info['username'])
                child.setText(f"👤 当前用户: {display_name}")
                break
        
        print(f"✅ 用户信息已更新: {self.user_info['username']}")
    
    def open_theme_settings(self):
        """打开主题设置"""
        dialog = ThemeSettingsDialog(self.theme_manager, self)
        dialog.theme_changed.connect(self.on_theme_changed)
        dialog.exec()
    
    def on_theme_changed(self, theme_name):
        """主题改变时的处理"""
        self.apply_current_theme()
        print(f"🎨 主题已切换为: {self.theme_manager.get_current_theme()['name']}")
    
    def show_statistics(self):
        """显示统计信息"""
        stats_dialog = StatisticsDialog(self.stats_manager, self)
        stats_dialog.exec()
    
    def update_session_time(self):
        """更新会话时间"""
        session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60
        # 确保统计数据结构存在
        if not hasattr(self.stats_manager, 'stats_data'):
            self.stats_manager.stats_data = {}
        if 'session_time' not in self.stats_manager.stats_data:
            self.stats_manager.stats_data['session_time'] = 0
        self.stats_manager.stats_data['session_time'] += 1  # 每分钟增加1分钟
        self.stats_manager.save_statistics()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        if hasattr(self, '_logout_confirmed') and self._logout_confirmed:
            event.accept()
        else:
            reply = QMessageBox.question(
                self, "确认退出", 
                "确定要退出系统吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                print(f"👋 用户 {self.user_info['username']} 已退出系统")
                self.logout_requested.emit()
                event.accept()
            else:
                event.ignore()


class StatisticsDialog(QDialog):
    """统计信息对话框"""
    
    def __init__(self, stats_manager, parent=None):
        super().__init__(parent)
        self.stats_manager = stats_manager
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("📊 使用统计")
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout()
        
        # 创建选项卡
        tab_widget = QTabWidget()
        
        # 总体统计选项卡
        overview_tab = self.create_overview_tab()
        tab_widget.addTab(overview_tab, "📈 总体统计")
        
        # 分类偏好选项卡
        category_tab = self.create_category_tab()
        tab_widget.addTab(category_tab, "📂 分类偏好")
        
        # 网站排行选项卡
        website_tab = self.create_website_tab()
        tab_widget.addTab(website_tab, "🌐 网站排行")
        
        # 活动趋势选项卡
        activity_tab = self.create_activity_tab()
        tab_widget.addTab(activity_tab, "📅 活动趋势")
        
        layout.addWidget(tab_widget)
        
        # 关闭按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        # 设置样式
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #4CAF50;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
    
    def create_overview_tab(self):
        """创建总体统计选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        stats = self.stats_manager.stats
        
        # 总访问次数
        total_label = QLabel(f"🌐 总访问次数: {stats['total_visits']}")
        total_label.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        layout.addWidget(total_label)
        
        # 会话时间
        session_time = stats.get('session_time', 0)
        session_label = QLabel(f"⏰ 总使用时间: {session_time} 分钟")
        session_label.setFont(QFont("Microsoft YaHei", 12))
        layout.addWidget(session_label)
        
        # 最后登录时间
        last_login = stats.get('last_login')
        if last_login:
            login_label = QLabel(f"🕐 最后登录: {last_login}")
        else:
            login_label = QLabel("🕐 最后登录: 首次登录")
        login_label.setFont(QFont("Microsoft YaHei", 12))
        layout.addWidget(login_label)
        
        # 分隔线
        layout.addWidget(QLabel("─" * 50))
        
        # 快速统计
        unique_categories = len(stats['favorite_categories'])
        unique_websites = len(stats['website_clicks'])
        
        quick_stats = f"""
        📊 快速统计:
        • 访问过的分类数: {unique_categories}
        • 访问过的网站数: {unique_websites}
        • 平均每日访问: {stats['total_visits'] / max(1, len(stats['daily_activity']))} 次
        """
        
        quick_label = QLabel(quick_stats)
        quick_label.setFont(QFont("Microsoft YaHei", 11))
        layout.addWidget(quick_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_category_tab(self):
        """创建分类偏好选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title_label = QLabel("📂 您最喜欢的网站分类")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        top_categories = self.stats_manager.get_top_categories()
        
        if not top_categories:
            no_data_label = QLabel("暂无数据，开始浏览网站来查看统计信息吧！")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_data_label)
        else:
            max_count = max(count for _, count in top_categories) if top_categories else 1
            
            for i, (category, count) in enumerate(top_categories, 1):
                # 分类名称和次数
                category_layout = QHBoxLayout()
                category_label = QLabel(f"{i}. {category}")
                count_label = QLabel(f"{count} 次")
                category_layout.addWidget(category_label)
                category_layout.addStretch()
                category_layout.addWidget(count_label)
                layout.addLayout(category_layout)
                
                # 进度条
                progress = QProgressBar()
                progress.setMaximum(max_count)
                progress.setValue(count)
                progress.setTextVisible(False)
                progress.setFixedHeight(20)
                layout.addWidget(progress)
                
                layout.addSpacing(10)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_website_tab(self):
        """创建网站排行选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title_label = QLabel("🌐 最常访问的网站")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        top_websites = self.stats_manager.get_top_websites()
        
        if not top_websites:
            no_data_label = QLabel("暂无数据，开始访问网站来查看排行吧！")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_data_label)
        else:
            max_count = max(count for _, count in top_websites) if top_websites else 1
            
            for i, (website, count) in enumerate(top_websites, 1):
                # 网站名称和次数
                website_layout = QHBoxLayout()
                website_label = QLabel(f"{i}. {website}")
                count_label = QLabel(f"{count} 次")
                website_layout.addWidget(website_label)
                website_layout.addStretch()
                website_layout.addWidget(count_label)
                layout.addLayout(website_layout)
                
                # 进度条
                progress = QProgressBar()
                progress.setMaximum(max_count)
                progress.setValue(count)
                progress.setTextVisible(False)
                progress.setFixedHeight(20)
                layout.addWidget(progress)
                
                layout.addSpacing(10)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_activity_tab(self):
        """创建活动趋势选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title_label = QLabel("📅 最近7天活动趋势")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        recent_activity = self.stats_manager.get_recent_activity()
        
        if not any(activity for _, activity in recent_activity):
            no_data_label = QLabel("最近7天暂无活动记录")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_data_label)
        else:
            max_activity = max(activity for _, activity in recent_activity) if recent_activity else 1
            
            for date, activity in recent_activity:
                # 日期和活动次数
                date_layout = QHBoxLayout()
                date_label = QLabel(date)
                activity_label = QLabel(f"{activity} 次访问")
                date_layout.addWidget(date_label)
                date_layout.addStretch()
                date_layout.addWidget(activity_label)
                layout.addLayout(date_layout)
                
                # 活动条
                progress = QProgressBar()
                progress.setMaximum(max_activity)
                progress.setValue(activity)
                progress.setTextVisible(False)
                progress.setFixedHeight(15)
                layout.addWidget(progress)
                
                layout.addSpacing(8)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget


if __name__ == "__main__":
    # 测试用的用户信息
    test_user = {
        'id': 1,
        'username': '测试用户',
        'email': 'test@example.com'
    }
    
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow(test_user)
    window.show()
    sys.exit(app.exec())
