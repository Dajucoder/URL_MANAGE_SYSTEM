#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
管理员界面
系统管理、用户管理、数据统计等功能
"""

import sys
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QTabWidget, QGroupBox,
    QLineEdit, QTextEdit, QComboBox, QMessageBox, QHeaderView,
    QScrollArea, QFrame, QFormLayout, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon

class AdminWindow(QWidget):
    """管理员主窗口"""
    
    def __init__(self, user_info, db_manager):
        super().__init__()
        self.user_info = user_info
        self.db_manager = db_manager
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("👑 管理员面板")
        self.setGeometry(100, 100, 1200, 800)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部标题
        title_layout = self.create_title_section()
        main_layout.addLayout(title_layout)
        
        # 选项卡
        tab_widget = QTabWidget()
        
        # 系统概览选项卡
        overview_tab = self.create_overview_tab()
        tab_widget.addTab(overview_tab, "📊 系统概览")
        
        # 用户管理选项卡
        user_management_tab = self.create_user_management_tab()
        tab_widget.addTab(user_management_tab, "👥 用户管理")
        
        # 网站管理选项卡
        website_management_tab = self.create_website_management_tab()
        tab_widget.addTab(website_management_tab, "🌐 网站管理")
        
        # 系统日志选项卡
        logs_tab = self.create_logs_tab()
        tab_widget.addTab(logs_tab, "📋 系统日志")
        
        main_layout.addWidget(tab_widget)
        
        self.setLayout(main_layout)
        
        # 应用样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a237e, stop:0.3 #283593, stop:0.6 #3949ab, stop:1 #1a237e);
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
                color: white;
            }
            
            QTabWidget::pane {
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.05);
            }
            
            QTabBar::tab {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                padding: 12px 20px;
                margin: 2px;
                border-radius: 8px;
                font-weight: bold;
            }
            
            QTabBar::tab:selected {
                background-color: rgba(255, 255, 255, 0.2);
            }
            
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                gridline-color: rgba(255, 255, 255, 0.2);
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
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
            
            QLabel {
                color: white;
                background: transparent;
            }
        """)
    
    def create_title_section(self):
        """创建标题区域"""
        layout = QHBoxLayout()
        
        # 标题
        title_label = QLabel("👑 系统管理面板")
        title_font = QFont("Microsoft YaHei", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        
        # 管理员信息
        admin_info = QLabel(f"管理员: {self.user_info['username']}")
        admin_info.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.8);")
        
        # 关闭按钮
        close_btn = QPushButton("❌ 关闭")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("background-color: #f44336;")
        
        layout.addWidget(title_label)
        layout.addWidget(admin_info)
        layout.addStretch()
        layout.addWidget(close_btn)
        
        return layout
    
    def create_overview_tab(self):
        """创建系统概览选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # 统计卡片区域
        stats_layout = QHBoxLayout()
        
        # 用户统计
        users_group = QGroupBox("👥 用户统计")
        users_layout = QVBoxLayout()
        
        self.total_users_label = QLabel("总用户数: 加载中...")
        self.active_users_label = QLabel("活跃用户: 加载中...")
        self.admin_users_label = QLabel("管理员数: 加载中...")
        
        users_layout.addWidget(self.total_users_label)
        users_layout.addWidget(self.active_users_label)
        users_layout.addWidget(self.admin_users_label)
        users_group.setLayout(users_layout)
        
        # 网站统计
        websites_group = QGroupBox("🌐 网站统计")
        websites_layout = QVBoxLayout()
        
        self.total_websites_label = QLabel("用户网站: 加载中...")
        self.public_websites_label = QLabel("公开网站: 加载中...")
        self.private_websites_label = QLabel("私有网站: 加载中...")
        
        websites_layout.addWidget(self.total_websites_label)
        websites_layout.addWidget(self.public_websites_label)
        websites_layout.addWidget(self.private_websites_label)
        websites_group.setLayout(websites_layout)
        
        # 访问统计
        visits_group = QGroupBox("📊 访问统计")
        visits_layout = QVBoxLayout()
        
        self.total_visits_label = QLabel("总访问量: 加载中...")
        self.today_visits_label = QLabel("今日访问: 加载中...")
        self.popular_website_label = QLabel("热门网站: 加载中...")
        
        visits_layout.addWidget(self.total_visits_label)
        visits_layout.addWidget(self.today_visits_label)
        visits_layout.addWidget(self.popular_website_label)
        visits_group.setLayout(visits_layout)
        
        stats_layout.addWidget(users_group)
        stats_layout.addWidget(websites_group)
        stats_layout.addWidget(visits_group)
        
        layout.addLayout(stats_layout)
        
        # 快速操作区域
        actions_group = QGroupBox("⚡ 快速操作")
        actions_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新统计")
        refresh_btn.clicked.connect(self.load_statistics)
        
        backup_btn = QPushButton("💾 数据备份")
        backup_btn.clicked.connect(self.backup_data)
        backup_btn.setStyleSheet("background-color: #2196F3;")
        
        cleanup_btn = QPushButton("🧹 清理日志")
        cleanup_btn.clicked.connect(self.cleanup_logs)
        cleanup_btn.setStyleSheet("background-color: #FF9800;")
        
        actions_layout.addWidget(refresh_btn)
        actions_layout.addWidget(backup_btn)
        actions_layout.addWidget(cleanup_btn)
        actions_layout.addStretch()
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_user_management_tab(self):
        """创建用户管理选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 搜索用户...")
        search_input.setMaximumWidth(300)
        
        add_user_btn = QPushButton("➕ 添加用户")
        add_user_btn.clicked.connect(self.add_user)
        
        refresh_users_btn = QPushButton("🔄 刷新")
        refresh_users_btn.clicked.connect(self.load_users)
        
        toolbar_layout.addWidget(QLabel("👥 用户管理"))
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(search_input)
        toolbar_layout.addWidget(add_user_btn)
        toolbar_layout.addWidget(refresh_users_btn)
        
        layout.addLayout(toolbar_layout)
        
        # 用户表格
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "用户名", "邮箱", "类型", "注册时间", "操作"
        ])
        
        # 设置表格属性
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        # 设置操作列的固定宽度
        self.users_table.setColumnWidth(5, 160)
        # 设置表格行高
        self.users_table.verticalHeader().setDefaultSectionSize(50)
        # 隐藏垂直表头
        self.users_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.users_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_website_management_tab(self):
        """创建网站管理选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        website_search_input = QLineEdit()
        website_search_input.setPlaceholderText("🔍 搜索网站...")
        website_search_input.setMaximumWidth(300)
        
        refresh_websites_btn = QPushButton("🔄 刷新")
        refresh_websites_btn.clicked.connect(self.load_websites)
        
        toolbar_layout.addWidget(QLabel("🌐 用户网站管理"))
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(website_search_input)
        toolbar_layout.addWidget(refresh_websites_btn)
        
        layout.addLayout(toolbar_layout)
        
        # 网站表格
        self.websites_table = QTableWidget()
        self.websites_table.setColumnCount(7)
        self.websites_table.setHorizontalHeaderLabels([
            "ID", "网站名称", "用户", "分类", "评分", "隐私", "操作"
        ])
        
        # 设置表格属性
        header = self.websites_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # 设置操作列的固定宽度
        self.websites_table.setColumnWidth(6, 120)
        # 设置表格行高
        self.websites_table.verticalHeader().setDefaultSectionSize(50)
        # 隐藏垂直表头
        self.websites_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.websites_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_logs_tab(self):
        """创建系统日志选项卡"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        log_search_input = QLineEdit()
        log_search_input.setPlaceholderText("🔍 搜索日志...")
        log_search_input.setMaximumWidth(300)
        
        refresh_logs_btn = QPushButton("🔄 刷新")
        refresh_logs_btn.clicked.connect(self.load_logs)
        
        clear_logs_btn = QPushButton("🗑️ 清空日志")
        clear_logs_btn.clicked.connect(self.clear_logs)
        clear_logs_btn.setStyleSheet("background-color: #f44336;")
        
        toolbar_layout.addWidget(QLabel("📋 系统日志"))
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(log_search_input)
        toolbar_layout.addWidget(refresh_logs_btn)
        toolbar_layout.addWidget(clear_logs_btn)
        
        layout.addLayout(toolbar_layout)
        
        # 日志表格
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(5)
        self.logs_table.setHorizontalHeaderLabels([
            "时间", "用户", "操作", "详情", "IP地址"
        ])
        
        # 设置表格属性
        header = self.logs_table.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.logs_table)
        
        widget.setLayout(layout)
        return widget
    
    def load_statistics(self):
        """加载统计数据"""
        try:
            # 用户统计
            total_users_query = "SELECT COUNT(*) FROM users"
            total_users = self.db_manager.execute_query(total_users_query)
            self.total_users_label.setText(f"总用户数: {total_users[0][0] if total_users else 0}")
            
            # 活跃用户（最近7天登录）
            active_users_query = """
            SELECT COUNT(*) FROM users 
            WHERE last_login >= %s
            """
            week_ago = datetime.now() - timedelta(days=7)
            active_users = self.db_manager.execute_query(active_users_query, (week_ago,))
            self.active_users_label.setText(f"活跃用户: {active_users[0][0] if active_users else 0}")
            
            # 管理员数量
            admin_users_query = "SELECT COUNT(*) FROM users WHERE is_admin = TRUE"
            admin_users = self.db_manager.execute_query(admin_users_query)
            self.admin_users_label.setText(f"管理员数: {admin_users[0][0] if admin_users else 0}")
            
            # 网站统计
            total_websites_query = "SELECT COUNT(*) FROM user_websites"
            total_websites = self.db_manager.execute_query(total_websites_query)
            self.total_websites_label.setText(f"用户网站: {total_websites[0][0] if total_websites else 0}")
            
            public_websites_query = "SELECT COUNT(*) FROM user_websites WHERE is_private = FALSE"
            public_websites = self.db_manager.execute_query(public_websites_query)
            self.public_websites_label.setText(f"公开网站: {public_websites[0][0] if public_websites else 0}")
            
            private_websites_query = "SELECT COUNT(*) FROM user_websites WHERE is_private = TRUE"
            private_websites = self.db_manager.execute_query(private_websites_query)
            self.private_websites_label.setText(f"私有网站: {private_websites[0][0] if private_websites else 0}")
            
            # 访问统计
            total_visits_query = "SELECT SUM(visit_count) FROM website_stats"
            total_visits = self.db_manager.execute_query(total_visits_query)
            total_count = total_visits[0][0] if total_visits and total_visits[0][0] else 0
            self.total_visits_label.setText(f"总访问量: {total_count}")
            
            # 今日访问
            today_visits_query = """
            SELECT COUNT(*) FROM website_stats 
            WHERE DATE(last_visited) = CURRENT_DATE
            """
            today_visits = self.db_manager.execute_query(today_visits_query)
            self.today_visits_label.setText(f"今日访问: {today_visits[0][0] if today_visits else 0}")
            
            # 热门网站
            popular_query = """
            SELECT website_name FROM website_stats 
            ORDER BY visit_count DESC LIMIT 1
            """
            popular = self.db_manager.execute_query(popular_query)
            popular_name = popular[0][0] if popular else "暂无数据"
            self.popular_website_label.setText(f"热门网站: {popular_name}")
            
        except Exception as e:
            print(f"❌ 加载统计数据失败: {e}")
            QMessageBox.warning(self, "错误", f"加载统计数据失败: {str(e)}")
    
    def load_users(self):
        """加载用户列表"""
        try:
            query = """
            SELECT id, username, email, is_admin, created_at 
            FROM users 
            ORDER BY created_at DESC
            """
            users = self.db_manager.execute_query(query)
            
            self.users_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                user_id, username, email, is_admin, created_at = user
                
                self.users_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
                self.users_table.setItem(row, 1, QTableWidgetItem(username))
                self.users_table.setItem(row, 2, QTableWidgetItem(email or "未设置"))
                
                user_type = "👑 管理员" if is_admin else "👤 普通用户"
                self.users_table.setItem(row, 3, QTableWidgetItem(user_type))
                
                created_time = str(created_at).split('.')[0] if created_at else "未知"
                self.users_table.setItem(row, 4, QTableWidgetItem(created_time))
                
                # 操作按钮
                action_widget = QWidget()
                action_layout = QHBoxLayout()
                action_layout.setContentsMargins(8, 5, 8, 5)
                action_layout.setSpacing(5)
                
                edit_btn = QPushButton("✏️ 编辑")
                edit_btn.setFixedSize(60, 35)
                edit_btn.clicked.connect(lambda checked, uid=user_id: self.edit_user(uid))
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        border: none;
                        border-radius: 5px;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                """)
                
                delete_btn = QPushButton("🗑️ 删除")
                delete_btn.setFixedSize(60, 35)
                delete_btn.clicked.connect(lambda checked, uid=user_id: self.delete_user(uid))
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        border: none;
                        border-radius: 5px;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #da190b;
                    }
                """)
                
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(delete_btn)
                action_widget.setLayout(action_layout)
                
                self.users_table.setCellWidget(row, 5, action_widget)
                
        except Exception as e:
            print(f"❌ 加载用户列表失败: {e}")
            QMessageBox.warning(self, "错误", f"加载用户列表失败: {str(e)}")
    
    def load_websites(self):
        """加载网站列表"""
        try:
            query = """
            SELECT uw.id, uw.name, u.username, uw.category, uw.rating, uw.is_private
            FROM user_websites uw
            JOIN users u ON uw.user_id = u.id
            ORDER BY uw.created_at DESC
            """
            websites = self.db_manager.execute_query(query)
            
            self.websites_table.setRowCount(len(websites))
            
            for row, website in enumerate(websites):
                website_id, name, username, category, rating, is_private = website
                
                self.websites_table.setItem(row, 0, QTableWidgetItem(str(website_id)))
                self.websites_table.setItem(row, 1, QTableWidgetItem(name))
                self.websites_table.setItem(row, 2, QTableWidgetItem(username))
                self.websites_table.setItem(row, 3, QTableWidgetItem(category))
                self.websites_table.setItem(row, 4, QTableWidgetItem("⭐" * rating))
                
                privacy_text = "🔒 私有" if is_private else "🌐 公开"
                self.websites_table.setItem(row, 5, QTableWidgetItem(privacy_text))
                
                # 操作按钮
                action_widget = QWidget()
                action_layout = QHBoxLayout()
                action_layout.setContentsMargins(8, 5, 8, 5)
                action_layout.setSpacing(5)
                
                delete_btn = QPushButton("🗑️ 删除")
                delete_btn.setFixedSize(80, 35)
                delete_btn.clicked.connect(lambda checked, wid=website_id: self.delete_website(wid))
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        border: none;
                        border-radius: 5px;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #da190b;
                    }
                """)
                
                action_layout.addWidget(delete_btn)
                action_widget.setLayout(action_layout)
                
                self.websites_table.setCellWidget(row, 6, action_widget)
                
        except Exception as e:
            print(f"❌ 加载网站列表失败: {e}")
            QMessageBox.warning(self, "错误", f"加载网站列表失败: {str(e)}")
    
    def load_logs(self):
        """加载系统日志"""
        try:
            query = """
            SELECT sl.created_at, u.username, sl.action, sl.details, sl.ip_address
            FROM system_logs sl
            LEFT JOIN users u ON sl.user_id = u.id
            ORDER BY sl.created_at DESC
            LIMIT 100
            """
            logs = self.db_manager.execute_query(query)
            
            self.logs_table.setRowCount(len(logs))
            
            for row, log in enumerate(logs):
                created_at, username, action, details, ip_address = log
                
                log_time = str(created_at).split('.')[0] if created_at else "未知"
                self.logs_table.setItem(row, 0, QTableWidgetItem(log_time))
                self.logs_table.setItem(row, 1, QTableWidgetItem(username or "系统"))
                self.logs_table.setItem(row, 2, QTableWidgetItem(action))
                self.logs_table.setItem(row, 3, QTableWidgetItem(details or ""))
                self.logs_table.setItem(row, 4, QTableWidgetItem(ip_address or ""))
                
        except Exception as e:
            print(f"❌ 加载系统日志失败: {e}")
            QMessageBox.warning(self, "错误", f"加载系统日志失败: {str(e)}")
    
    def add_user(self):
        """添加用户"""
        QMessageBox.information(self, "功能开发中", "添加用户功能正在开发中...")
    
    def edit_user(self, user_id):
        """编辑用户"""
        QMessageBox.information(self, "功能开发中", f"编辑用户 {user_id} 功能正在开发中...")
    
    def delete_user(self, user_id):
        """删除用户"""
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除用户 ID {user_id} 吗？\n此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_query = "DELETE FROM users WHERE id = %s"
                if self.db_manager.execute_non_query(delete_query, (user_id,)):
                    QMessageBox.information(self, "成功", "用户删除成功！")
                    self.load_users()
                    self.load_statistics()
                else:
                    QMessageBox.critical(self, "失败", "用户删除失败")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除用户失败: {str(e)}")
    
    def delete_website(self, website_id):
        """删除网站"""
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除网站 ID {website_id} 吗？\n此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_query = "DELETE FROM user_websites WHERE id = %s"
                if self.db_manager.execute_non_query(delete_query, (website_id,)):
                    QMessageBox.information(self, "成功", "网站删除成功！")
                    self.load_websites()
                    self.load_statistics()
                else:
                    QMessageBox.critical(self, "失败", "网站删除失败")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除网站失败: {str(e)}")
    
    def backup_data(self):
        """数据备份"""
        QMessageBox.information(self, "功能开发中", "数据备份功能正在开发中...")
    
    def cleanup_logs(self):
        """清理日志"""
        reply = QMessageBox.question(
            self, "确认清理", 
            "确定要清理30天前的系统日志吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                cleanup_date = datetime.now() - timedelta(days=30)
                cleanup_query = "DELETE FROM system_logs WHERE created_at < %s"
                if self.db_manager.execute_non_query(cleanup_query, (cleanup_date,)):
                    QMessageBox.information(self, "成功", "日志清理完成！")
                    self.load_logs()
                else:
                    QMessageBox.critical(self, "失败", "日志清理失败")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"清理日志失败: {str(e)}")
    
    def clear_logs(self):
        """清空所有日志"""
        reply = QMessageBox.question(
            self, "确认清空", 
            "确定要清空所有系统日志吗？\n此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                clear_query = "DELETE FROM system_logs"
                if self.db_manager.execute_non_query(clear_query):
                    QMessageBox.information(self, "成功", "所有日志已清空！")
                    self.load_logs()
                else:
                    QMessageBox.critical(self, "失败", "清空日志失败")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"清空日志失败: {str(e)}")
    
    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        # 加载数据
        self.load_users()
        self.load_websites()
        self.load_logs()


if __name__ == "__main__":
    # 测试用的管理员信息
    test_admin = {
        'id': 1,
        'username': 'admin',
        'email': 'admin@system.local',
        'is_admin': True
    }
    
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    # 模拟数据库管理器
    class MockDBManager:
        def execute_query(self, query, params=None):
            return []
        
        def execute_non_query(self, query, params=None):
            return True
    
    window = AdminWindow(test_admin, MockDBManager())
    window.show()
    sys.exit(app.exec())
