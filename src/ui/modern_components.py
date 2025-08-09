#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
现代化UI组件模块
包含自定义的现代化界面组件
"""

from PyQt6.QtWidgets import (
    QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, QToolButton
)
from PyQt6.QtCore import Qt, QRect, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPainter, QPen, QColor


class ModernLineEdit(QLineEdit):
    """现代化输入框 - 全面优化版"""
    
    def __init__(self, placeholder="", icon=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.icon = icon
        self.setup_style()
        self.setup_animations()
        
    def setup_style(self):
        """设置现代化样式 - 统一高度和显示效果"""
        self.setStyleSheet("""
            QLineEdit {
                padding: 18px 20px 18px 50px;
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 14px;
                font-size: 16px;
                font-weight: 500;
                background: rgba(20, 24, 32, 0.9);
                color: rgba(255, 255, 255, 0.95);
                selection-background-color: rgba(99, 102, 241, 0.3);
                min-height: 24px;
                height: 60px;
                letter-spacing: 0.2px;
                line-height: 24px;
            }
            
            QLineEdit:focus {
                border: 2px solid rgba(99, 102, 241, 0.7);
                background: rgba(20, 24, 32, 0.95);
            }
            
            QLineEdit:hover:!focus {
                border: 2px solid rgba(255, 255, 255, 0.25);
                background: rgba(20, 24, 32, 0.92);
            }
            
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
                font-style: normal;
                font-weight: 400;
            }
        """)
    
    def setup_animations(self):
        """设置动画效果"""
        self.focus_animation = QPropertyAnimation(self, b"geometry")
        self.focus_animation.setDuration(200)
        self.focus_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def paintEvent(self, event):
        """绘制图标"""
        super().paintEvent(event)
        if self.icon:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 绘制图标
            icon_rect = QRect(15, (self.height() - 20) // 2, 20, 20)
            painter.setPen(QPen(QColor(255, 255, 255, 150), 2))
            painter.setFont(QFont("Segoe UI Emoji", 14))
            painter.drawText(icon_rect, Qt.AlignmentFlag.AlignCenter, self.icon)


class ModernButton(QPushButton):
    """现代化按钮 - 全面优化版"""
    
    def __init__(self, text, primary=True):
        super().__init__(text)
        self.primary = primary
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_style()
        self.setup_shadow()
        self.setup_animations()
        
    def setup_style(self):
        """设置现代化样式 - 统一高度与输入框一致"""
        if self.primary:
            self.setStyleSheet("""
                QPushButton {
                    padding: 18px 32px;
                    border: none;
                    border-radius: 14px;
                    font-size: 16px;
                    font-weight: 600;
                    color: white;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6366f1, stop:0.5 #8b5cf6, stop:1 #a855f7);
                    min-height: 24px;
                    height: 60px;
                    letter-spacing: 0.5px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5855eb, stop:0.5 #7c3aed, stop:1 #9333ea);
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4f46e5, stop:0.5 #6d28d9, stop:1 #86198f);
                }
                
                QPushButton:disabled {
                    background: rgba(255, 255, 255, 0.08);
                    color: rgba(255, 255, 255, 0.4);
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    padding: 18px 28px;
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 14px;
                    font-size: 16px;
                    font-weight: 500;
                    color: rgba(255, 255, 255, 0.85);
                    background: rgba(255, 255, 255, 0.08);
                    min-height: 24px;
                    height: 60px;
                    letter-spacing: 0.3px;
                }
                
                QPushButton:hover {
                    border-color: rgba(255, 255, 255, 0.35);
                    color: white;
                    background: rgba(255, 255, 255, 0.15);
                }
                
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.12);
                    border-color: rgba(255, 255, 255, 0.25);
                }
            """)
    
    def setup_shadow(self):
        """设置增强阴影效果"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)
    
    def setup_animations(self):
        """设置按钮动画"""
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)


class ModernPasswordEdit(QLineEdit):
    """带显隐切换的现代化密码输入框"""
    
    def __init__(self, placeholder="", icon=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.icon = icon
        self._visible = False
        self._toggle_btn = QToolButton(self)
        self._setup_style()
        self._setup_toggle_button()
        self.setEchoMode(QLineEdit.EchoMode.Password)
    
    def _setup_style(self):
        self.setStyleSheet("""
            QLineEdit {
                padding: 18px 50px 18px 50px;
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 14px;
                font-size: 16px;
                font-weight: 500;
                background: rgba(20, 24, 32, 0.9);
                color: rgba(255, 255, 255, 0.95);
                selection-background-color: rgba(99, 102, 241, 0.3);
                min-height: 24px;
                height: 60px;
                letter-spacing: 0.2px;
                line-height: 24px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(99, 102, 241, 0.7);
                background: rgba(20, 24, 32, 0.95);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
                font-style: normal;
                font-weight: 400;
            }
        """)
    
    def _setup_toggle_button(self):
        self._toggle_btn.setText("👁")
        self._toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                color: rgba(255, 255, 255, 0.8);
                border: none;
                font-size: 16px;
                padding: 0px;
            }
            QToolButton:hover {
                color: white;
            }
        """)
        self._toggle_btn.clicked.connect(self._toggle_visibility)
        self._reposition_toggle()
    
    def _toggle_visibility(self):
        self._visible = not self._visible
        self.setEchoMode(QLineEdit.EchoMode.Normal if self._visible else QLineEdit.EchoMode.Password)
        self._toggle_btn.setText("🙈" if self._visible else "👁")
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition_toggle()
    
    def _reposition_toggle(self):
        btn_size = 24
        margin_right = 14
        self._toggle_btn.resize(btn_size, btn_size)
        self._toggle_btn.move(self.width() - btn_size - margin_right, (self.height() - btn_size) // 2)
    
    def paintEvent(self, event):
        """绘制左侧图标"""
        super().paintEvent(event)
        if self.icon:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            icon_rect = QRect(15, (self.height() - 20) // 2, 20, 20)
            painter.setPen(QPen(QColor(255, 255, 255, 150), 2))
            painter.setFont(QFont("Segoe UI Emoji", 14))
            painter.drawText(icon_rect, Qt.AlignmentFlag.AlignCenter, self.icon)


class GlassCard(QFrame):
    """现代化玻璃卡片效果 - 全面优化版"""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
        self.setup_animations()
        
    def setup_style(self):
        """设置现代化玻璃效果样式 - 提升视觉层次和质感"""
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 17, 25, 0.95), 
                    stop:0.5 rgba(18, 20, 28, 0.92),
                    stop:1 rgba(21, 23, 31, 0.90));
                border: 1.5px solid rgba(255, 255, 255, 0.15);
                border-radius: 24px;
                backdrop-filter: blur(40px);
            }
        """)
        
        # 添加增强阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 15)
        self.setGraphicsEffect(shadow)
    
    def setup_animations(self):
        """设置卡片动画效果"""
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(300)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 启动淡入动画
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(600)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        QTimer.singleShot(50, self.fade_animation.start)
