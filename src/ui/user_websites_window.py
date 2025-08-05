#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户自定义网站管理界面
用户可以添加、编辑、删除自己的推荐网站
"""

import sys
import os
import webbrowser
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QComboBox, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QSpinBox,
    QGroupBox, QScrollArea, QFrame, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class AddWebsiteDialog(QDialog):
    """添加网站对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("➕ 添加推荐网站")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 表单区域
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # 网站名称
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("请输入网站名称")
        form_layout.addRow("🌐 网站名称:", self.name_input)
        
        # 网站URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        form_layout.addRow("🔗 网站地址:", self.url_input)
        
        # 网站描述
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("请输入网站描述...")
        self.description_input.setMaximumHeight(80)
        form_layout.addRow("📝 网站描述:", self.description_input)
        
        # 网站分类
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems([
            "学习教育", "开发工具", "娱乐休闲", "实用工具", "新闻资讯",
            "社交媒体", "购物网站", "视频音乐", "设计创意", "其他"
        ])
        form_layout.addRow("📂 网站分类:", self.category_input)
        
        # 网站评分
        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 5)
        self.rating_input.setValue(5)
        self.rating_input.setSuffix(" ⭐")
        form_layout.addRow("⭐ 网站评分:", self.rating_input)
        
        # 是否私有
        self.is_private_checkbox = QCheckBox("仅自己可见")
        self.is_private_checkbox.setChecked(True)
        form_layout.addRow("🔒 隐私设置:", self.is_private_checkbox)
        
        layout.addLayout(form_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 保存")
        save_btn.clicked.connect(self.accept)
        save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; }")
        
        cancel_btn = QPushButton("❌ 取消")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 应用样式
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a237e, stop:0.3 #283593, stop:0.6 #3949ab, stop:1 #1a237e);
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
                color: white;
            }
            
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 14px;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: rgba(255, 255, 255, 0.7);
                background-color: rgba(255, 255, 255, 0.15);
            }
            
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            
            QPushButton:hover {
                opacity: 0.8;
            }
            
            QLabel {
                color: white;
                background: transparent;
            }
            
            QCheckBox {
                color: white;
                font-size: 14px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid rgba(255, 255, 255, 0.5);
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
        """)
    
    def get_website_data(self):
        """获取网站数据"""
        return {
            'name': self.name_input.text().strip(),
            'url': self.url_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'category': self.category_input.currentText().strip(),
            'rating': self.rating_input.value(),
            'is_private': self.is_private_checkbox.isChecked()
        }
    
    def validate_data(self):
        """验证数据"""
        data = self.get_website_data()
        
        if not data['name']:
            QMessageBox.warning(self, "输入错误", "请输入网站名称")
            return False
        
        if not data['url']:
            QMessageBox.warning(self, "输入错误", "请输入网站地址")
            return False
        
        # 简单的URL验证
        if not (data['url'].startswith('http://') or data['url'].startswith('https://')):
            QMessageBox.warning(self, "格式错误", "网站地址必须以 http:// 或 https:// 开头")
            return False
        
        if not data['description']:
            QMessageBox.warning(self, "输入错误", "请输入网站描述")
            return False
        
        if not data['category']:
            QMessageBox.warning(self, "输入错误", "请选择或输入网站分类")
            return False
        
        return True
    
    def accept(self):
        """确认添加"""
        if self.validate_data():
            super().accept()


class UserWebsitesWindow(QWidget):
    """用户自定义网站管理窗口"""
    
    def __init__(self, user_info, db_manager):
        super().__init__()
        self.user_info = user_info
        self.db_manager = db_manager
        self.init_ui()
        self.load_user_websites()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle(f"🌐 我的推荐网站 - {self.user_info['username']}")
        self.setGeometry(100, 100, 1000, 700)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部工具栏
        toolbar_layout = self.create_toolbar()
        main_layout.addLayout(toolbar_layout)
        
        # 网站列表
        self.websites_table = QTableWidget()
        self.websites_table.setColumnCount(7)
        self.websites_table.setHorizontalHeaderLabels([
            "网站名称", "分类", "评分", "隐私", "创建时间", "访问", "操作"
        ])
        
        # 设置表格属性
        header = self.websites_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # 网站名称列自适应
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        
        self.websites_table.setAlternatingRowColors(True)
        self.websites_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        main_layout.addWidget(self.websites_table)
        
        # 统计信息
        stats_layout = QHBoxLayout()
        self.total_websites_label = QLabel("我的网站: 0")
        self.public_websites_label = QLabel("公开: 0")
        self.private_websites_label = QLabel("私有: 0")
        
        stats_layout.addWidget(self.total_websites_label)
        stats_layout.addWidget(self.public_websites_label)
        stats_layout.addWidget(self.private_websites_label)
        stats_layout.addStretch()
        
        main_layout.addLayout(stats_layout)
        
        self.setLayout(main_layout)
        
        # 应用样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a237e, stop:0.3 #283593, stop:0.6 #3949ab, stop:1 #1a237e);
                font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
                color: white;
            }
            
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                gridline-color: rgba(255, 255, 255, 0.2);
            }
            
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QTableWidget::item:selected {
                background-color: rgba(255, 255, 255, 0.2);
            }
            
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
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
            
            QLabel {
                color: white;
                background: transparent;
                font-size: 14px;
            }
        """)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar_layout = QHBoxLayout()
        
        # 标题
        title_label = QLabel("🌐 我的推荐网站")
        title_font = QFont("Microsoft YaHei", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索我的网站...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self.search_websites)
        
        # 添加网站按钮
        add_btn = QPushButton("➕ 添加网站")
        add_btn.clicked.connect(self.add_website)
        add_btn.setStyleSheet("QPushButton { background-color: #4CAF50; }")
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.load_user_websites)
        refresh_btn.setStyleSheet("QPushButton { background-color: #2196F3; }")
        
        # 关闭按钮
        close_btn = QPushButton("❌ 关闭")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
        
        toolbar_layout.addWidget(title_label)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(add_btn)
        toolbar_layout.addWidget(refresh_btn)
        toolbar_layout.addWidget(close_btn)
        
        return toolbar_layout
    
    def load_user_websites(self):
        """加载用户网站"""
        query = """
        SELECT id, name, url, description, category, rating, is_private, created_at
        FROM user_websites 
        WHERE user_id = %s 
        ORDER BY created_at DESC
        """
        
        websites = self.db_manager.execute_query(query, (self.user_info['id'],))
        
        self.websites_table.setRowCount(len(websites))
        
        for row, website in enumerate(websites):
            website_id, name, url, description, category, rating, is_private, created_at = website
            
            # 网站名称（可点击）
            name_item = QTableWidgetItem(name)
            name_item.setToolTip(f"描述: {description}\n地址: {url}")
            self.websites_table.setItem(row, 0, name_item)
            
            # 分类
            self.websites_table.setItem(row, 1, QTableWidgetItem(category))
            
            # 评分
            rating_text = "⭐" * rating
            self.websites_table.setItem(row, 2, QTableWidgetItem(rating_text))
            
            # 隐私设置
            privacy_text = "🔒 私有" if is_private else "🌐 公开"
            privacy_item = QTableWidgetItem(privacy_text)
            if is_private:
                privacy_item.setBackground(Qt.GlobalColor.darkRed)
            else:
                privacy_item.setBackground(Qt.GlobalColor.darkGreen)
            self.websites_table.setItem(row, 3, privacy_item)
            
            # 创建时间
            created_time = str(created_at).split('.')[0] if created_at else "未知"
            self.websites_table.setItem(row, 4, QTableWidgetItem(created_time))
            
            # 访问按钮
            visit_btn = QPushButton("🌐 访问")
            visit_btn.setFixedSize(60, 30)
            visit_btn.clicked.connect(lambda checked, u=url, n=name: self.visit_website(u, n))
            visit_btn.setStyleSheet("QPushButton { background-color: #2196F3; font-size: 12px; }")
            self.websites_table.setCellWidget(row, 5, visit_btn)
            
            # 操作按钮
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(5, 2, 5, 2)
            action_layout.setSpacing(5)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 25)
            edit_btn.clicked.connect(lambda checked, wid=website_id: self.edit_website(wid))
            edit_btn.setStyleSheet("QPushButton { background-color: #ff9800; font-size: 12px; }")
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(30, 25)
            delete_btn.clicked.connect(lambda checked, wid=website_id: self.delete_website(wid))
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; font-size: 12px; }")
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_widget.setLayout(action_layout)
            
            self.websites_table.setCellWidget(row, 6, action_widget)
        
        # 更新统计信息
        self.update_stats()
    
    def update_stats(self):
        """更新统计信息"""
        # 总网站数
        total_query = "SELECT COUNT(*) FROM user_websites WHERE user_id = %s"
        total_result = self.db_manager.execute_query(total_query, (self.user_info['id'],))
        total_websites = total_result[0][0] if total_result else 0
        
        # 公开网站数
        public_query = "SELECT COUNT(*) FROM user_websites WHERE user_id = %s AND is_private = FALSE"
        public_result = self.db_manager.execute_query(public_query, (self.user_info['id'],))
        public_websites = public_result[0][0] if public_result else 0
        
        # 私有网站数
        private_websites = total_websites - public_websites
        
        self.total_websites_label.setText(f"我的网站: {total_websites}")
        self.public_websites_label.setText(f"公开: {public_websites}")
        self.private_websites_label.setText(f"私有: {private_websites}")
    
    def search_websites(self):
        """搜索网站"""
        keyword = self.search_input.text().strip()
        if not keyword:
            self.load_user_websites()
            return
        
        query = """
        SELECT id, name, url, description, category, rating, is_private, created_at
        FROM user_websites 
        WHERE user_id = %s AND (name ILIKE %s OR description ILIKE %s OR category ILIKE %s)
        ORDER BY created_at DESC
        """
        
        search_pattern = f"%{keyword}%"
        websites = self.db_manager.execute_query(query, (
            self.user_info['id'], search_pattern, search_pattern, search_pattern
        ))
        
        # 更新表格显示（逻辑与load_user_websites相同）
        self.websites_table.setRowCount(len(websites))
        # ... 填充表格的代码 ...
    
    def add_website(self):
        """添加网站"""
        dialog = AddWebsiteDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            website_data = dialog.get_website_data()
            
            # 插入数据库
            insert_query = """
            INSERT INTO user_websites (user_id, name, url, description, category, rating, is_private, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            if self.db_manager.execute_non_query(insert_query, (
                self.user_info['id'],
                website_data['name'],
                website_data['url'],
                website_data['description'],
                website_data['category'],
                website_data['rating'],
                website_data['is_private'],
                datetime.now()
            )):
                QMessageBox.information(self, "成功", "网站添加成功！")
                self.load_user_websites()
                
                # 记录系统日志
                self.log_action("添加网站", f"添加了网站: {website_data['name']}")
            else:
                QMessageBox.critical(self, "失败", "网站添加失败，请稍后重试")
    
    def edit_website(self, website_id):
        """编辑网站"""
        # 获取网站信息
        query = "SELECT name, url, description, category, rating, is_private FROM user_websites WHERE id = %s"
        result = self.db_manager.execute_query(query, (website_id,))
        
        if not result:
            QMessageBox.warning(self, "错误", "网站信息不存在")
            return
        
        website_info = result[0]
        
        # 创建编辑对话框
        dialog = AddWebsiteDialog(self)
        dialog.setWindowTitle("✏️ 编辑推荐网站")
        
        # 填充现有数据
        dialog.name_input.setText(website_info[0])
        dialog.url_input.setText(website_info[1])
        dialog.description_input.setPlainText(website_info[2])
        dialog.category_input.setCurrentText(website_info[3])
        dialog.rating_input.setValue(website_info[4])
        dialog.is_private_checkbox.setChecked(website_info[5])
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            website_data = dialog.get_website_data()
            
            # 更新数据库
            update_query = """
            UPDATE user_websites 
            SET name = %s, url = %s, description = %s, category = %s, rating = %s, is_private = %s, updated_at = %s
            WHERE id = %s
            """
            
            if self.db_manager.execute_non_query(update_query, (
                website_data['name'],
                website_data['url'],
                website_data['description'],
                website_data['category'],
                website_data['rating'],
                website_data['is_private'],
                datetime.now(),
                website_id
            )):
                QMessageBox.information(self, "成功", "网站信息更新成功！")
                self.load_user_websites()
                
                # 记录系统日志
                self.log_action("编辑网站", f"编辑了网站: {website_data['name']}")
            else:
                QMessageBox.critical(self, "失败", "网站信息更新失败，请稍后重试")
    
    def delete_website(self, website_id):
        """删除网站"""
        # 获取网站名称
        query = "SELECT name FROM user_websites WHERE id = %s"
        result = self.db_manager.execute_query(query, (website_id,))
        
        if not result:
            QMessageBox.warning(self, "错误", "网站信息不存在")
            return
        
        website_name = result[0][0]
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除网站 '{website_name}' 吗？\n此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            delete_query = "DELETE FROM user_websites WHERE id = %s"
            if self.db_manager.execute_non_query(delete_query, (website_id,)):
                QMessageBox.information(self, "成功", "网站删除成功！")
                self.load_user_websites()
                
                # 记录系统日志
                self.log_action("删除网站", f"删除了网站: {website_name}")
            else:
                QMessageBox.critical(self, "失败", "网站删除失败，请稍后重试")
    
    def visit_website(self, url, name):
        """访问网站"""
        try:
            webbrowser.open(url)
            print(f"🌐 正在打开网站: {name}")
            
            # 记录访问统计
            self.record_visit(name, url)
            
            # 记录系统日志
            self.log_action("访问网站", f"访问了网站: {name}")
            
        except Exception as e:
            print(f"❌ 打开网站失败: {e}")
            QMessageBox.warning(self, "错误", f"无法打开网站: {str(e)}")
    
    def record_visit(self, website_name, website_url):
        """记录网站访问"""
        # 检查是否已有访问记录
        check_query = """
        SELECT id, visit_count FROM website_stats 
        WHERE website_name = %s AND website_url = %s AND user_id = %s
        """
        
        result = self.db_manager.execute_query(check_query, (website_name, website_url, self.user_info['id']))
        
        if result:
            # 更新访问次数
            stats_id, visit_count = result[0]
            update_query = """
            UPDATE website_stats 
            SET visit_count = %s, last_visited = %s 
            WHERE id = %s
            """
            self.db_manager.execute_non_query(update_query, (visit_count + 1, datetime.now(), stats_id))
        else:
            # 创建新的访问记录
            insert_query = """
            INSERT INTO website_stats (website_name, website_url, user_id, visit_count, last_visited)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.db_manager.execute_non_query(insert_query, (
                website_name, website_url, self.user_info['id'], 1, datetime.now()
            ))
    
    def log_action(self, action, details):
        """记录系统日志"""
        log_query = """
        INSERT INTO system_logs (user_id, action, details, created_at)
        VALUES (%s, %s, %s, %s)
        """
        
        self.db_manager.execute_non_query(log_query, (
            self.user_info['id'], action, details, datetime.now()
        ))


if __name__ == "__main__":
    # 测试用的用户信息
    test_user = {
        'id': 1,
        'username': '测试用户',
        'email': 'test@example.com'
    }
    
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    # 模拟数据库管理器
    class MockDBManager:
        def execute_query(self, query, params=None):
            return []
        
        def execute_non_query(self, query, params=None):
            return True
    
    window = UserWebsitesWindow(test_user, MockDBManager())
    window.show()
    sys.exit(app.exec())
