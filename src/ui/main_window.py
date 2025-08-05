#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口模块 - 网站推荐系统
用户登录后的主界面
"""

import sys
import os
import webbrowser
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QLineEdit, QComboBox, QMessageBox,
    QGridLayout, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.data.website_data import (
    get_all_categories, get_websites_by_category, 
    get_all_websites, search_websites, get_top_rated_websites
)


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
        except Exception as e:
            print(f"❌ 打开网站失败: {e}")


class MainWindow(QWidget):
    """主窗口类"""
    
    logout_requested = pyqtSignal()
    
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.current_websites = []
        self.init_ui()
        self.load_all_websites()
    
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
        
        # 应用样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a237e, stop:0.3 #283593, stop:0.6 #3949ab, stop:1 #1a237e);
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
                color: white;
            }
            
            QLineEdit {
                padding: 10px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border-color: rgba(255, 255, 255, 0.7);
                background-color: rgba(255, 255, 255, 0.15);
            }
            
            QPushButton {
                padding: 10px 20px;
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
            
            QComboBox {
                padding: 8px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 14px;
            }
            
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            QLabel {
                color: white;
                background: transparent;
            }
        """)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar_layout = QHBoxLayout()
        
        # 用户信息
        user_label = QLabel(f"👤 当前用户: {self.user_info['username']}")
        user_font = QFont("Microsoft YaHei", 12, QFont.Weight.Bold)
        user_label.setFont(user_font)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索网站...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self.search_websites)
        
        # 功能按钮区域
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
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
        
        buttons_layout.addWidget(profile_btn)
        buttons_layout.addWidget(my_websites_btn)
        buttons_layout.addWidget(logout_button)
        
        toolbar_layout.addWidget(user_label)
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
        
        # 如果工具栏中有用户标签，也需要更新
        for child in self.findChildren(QLabel):
            if child.text().startswith("👤 当前用户:"):
                child.setText(f"👤 当前用户: {self.user_info['username']}")
                break
        
        print(f"✅ 用户信息已更新: {self.user_info['username']}")
    
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