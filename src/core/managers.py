"""
管理器模块 - 包含主题管理器和统计管理器
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer


class ThemeManager:
    """主题管理器 - 管理应用程序的主题和样式"""
    
    def __init__(self):
        self.config_file = "config/theme_config.json"
        self.current_theme = "default"
        self.themes = {
            "default": {
                "name": "默认主题",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2)",
                "primary": "#007acc",
                "secondary": "#5a5a5a",
                "text": "#333333",
                "text_color": "#333333",
                "accent": "#ff6b35",
                "accent_color": "#ff6b35",
                "card_bg": "rgba(255, 255, 255, 0.1)",
                "card_border": "rgba(255, 255, 255, 0.3)"
            },
            "dark_blue": {
                "name": "深蓝主题",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a237e, stop:1 #3949ab)",
                "primary": "#89b4fa",
                "secondary": "#6c7086",
                "text": "#cdd6f4",
                "text_color": "#cdd6f4",
                "accent": "#f38ba8",
                "accent_color": "#4CAF50",
                "card_bg": "rgba(255, 255, 255, 0.1)",
                "card_border": "rgba(255, 255, 255, 0.3)"
            },
            "purple_gradient": {
                "name": "紫色渐变",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2)",
                "primary": "#9d4edd",
                "secondary": "#7209b7",
                "text": "#ffffff",
                "text_color": "#ffffff",
                "accent": "#f72585",
                "accent_color": "#9C27B0",
                "card_bg": "rgba(255, 255, 255, 0.1)",
                "card_border": "rgba(255, 255, 255, 0.3)"
            },
            "green_nature": {
                "name": "自然绿色",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #11998e, stop:1 #38ef7d)",
                "primary": "#2a9d8f",
                "secondary": "#e9c46a",
                "text": "#f4f3ee",
                "text_color": "#f4f3ee",
                "accent": "#e76f51",
                "accent_color": "#4CAF50",
                "card_bg": "rgba(255, 255, 255, 0.1)",
                "card_border": "rgba(255, 255, 255, 0.3)"
            },
            "sunset_orange": {
                "name": "日落橙色",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff9a9e, stop:1 #fecfef)",
                "primary": "#f7931e",
                "secondary": "#ffb627",
                "text": "#ffffff",
                "text_color": "#ffffff",
                "accent": "#c5283d",
                "accent_color": "#FF5722",
                "card_bg": "rgba(255, 255, 255, 0.1)",
                "card_border": "rgba(255, 255, 255, 0.3)"
            }
        }
        self.load_theme_config()
    
    def load_theme_config(self):
        """加载主题配置"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_theme = config.get('current_theme', 'default')
        except Exception as e:
            print(f"加载主题配置失败: {e}")
            self.current_theme = "default"
    
    def save_theme_config(self):
        """保存主题配置"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            config = {
                'current_theme': self.current_theme,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存主题配置失败: {e}")
    
    def get_available_themes(self) -> Dict[str, str]:
        """获取可用主题列表"""
        return {key: theme["name"] for key, theme in self.themes.items()}
    
    def set_theme(self, theme_name: str) -> bool:
        """设置当前主题"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_theme_config()
            return True
        return False
    
    def get_current_theme(self) -> Dict[str, str]:
        """获取当前主题配置"""
        return self.themes.get(self.current_theme, self.themes["default"])
    
    def generate_stylesheet(self) -> str:
        """生成当前主题的样式表"""
        theme = self.get_current_theme()
        
        return f"""
        QMainWindow {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        QPushButton {{
            background-color: {theme['primary']};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {theme['accent']};
        }}
        
        QPushButton:pressed {{
            background-color: {theme['secondary']};
        }}
        
        QLineEdit {{
            background-color: white;
            border: 2px solid {theme['secondary']};
            padding: 8px;
            border-radius: 4px;
            color: #333;
        }}
        
        QLineEdit:focus {{
            border-color: {theme['primary']};
        }}
        
        QLabel {{
            color: {theme['text']};
        }}
        
        QListWidget {{
            background-color: white;
            border: 1px solid {theme['secondary']};
            border-radius: 4px;
        }}
        
        QListWidget::item {{
            padding: 8px;
            border-bottom: 1px solid #eee;
        }}
        
        QListWidget::item:selected {{
            background-color: {theme['primary']};
            color: white;
        }}
        
        QMenuBar {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        QMenuBar::item:selected {{
            background-color: {theme['primary']};
        }}
        
        QMenu {{
            background-color: {theme['background']};
            color: {theme['text']};
            border: 1px solid {theme['secondary']};
        }}
        
        QMenu::item:selected {{
            background-color: {theme['primary']};
        }}
        """


class StatisticsManager:
    """统计管理器 - 管理用户行为统计和数据分析"""
    
    def __init__(self):
        self.stats_file = "config/statistics.json"
        self.stats_data = {
            "total_visits": 0,
            "favorite_categories": {},
            "daily_activity": {},
            "website_clicks": {},
            "session_time": 0,
            "last_login": None,
            "login_count": 0,
            "search_count": 0,
            "website_visits": {},
            "user_preferences": {},
            "system_performance": {
                "avg_response_time": 0,
                "error_count": 0,
                "uptime": 0
            }
        }
        # 为了向后兼容，添加 stats 属性
        self.stats = self.stats_data
        self.load_statistics()
        
        # 设置定时保存
        try:
            self.save_timer = QTimer()
            self.save_timer.timeout.connect(self.save_statistics)
            self.save_timer.start(300000)  # 每5分钟保存一次
        except:
            # 如果QTimer不可用，跳过定时保存
            pass
    
    def load_statistics(self):
        """加载统计数据"""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    self.stats_data.update(loaded_data)
        except Exception as e:
            print(f"加载统计数据失败: {e}")
    
    def save_statistics(self):
        """保存统计数据"""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存统计数据失败: {e}")
    
    def record_login(self, username: str):
        """记录登录事件"""
        self.stats_data["login_count"] += 1
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.stats_data["daily_activity"]:
            self.stats_data["daily_activity"][today] = {
                "logins": 0,
                "searches": 0,
                "visits": 0
            }
        
        self.stats_data["daily_activity"][today]["logins"] += 1
        
        # 记录用户偏好
        if username not in self.stats_data["user_preferences"]:
            self.stats_data["user_preferences"][username] = {
                "login_times": [],
                "favorite_categories": {},
                "search_keywords": []
            }
        
        self.stats_data["user_preferences"][username]["login_times"].append(
            datetime.now().isoformat()
        )
    
    def record_search(self, keyword: str, username: str = None):
        """记录搜索事件"""
        self.stats_data["search_count"] += 1
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today in self.stats_data["daily_activity"]:
            self.stats_data["daily_activity"][today]["searches"] += 1
        
        if username and username in self.stats_data["user_preferences"]:
            self.stats_data["user_preferences"][username]["search_keywords"].append({
                "keyword": keyword,
                "timestamp": datetime.now().isoformat()
            })
    
    def record_website_visit(self, website_name: str, category: str = "未分类"):
        """记录网站访问"""
        # 更新总访问次数
        self.stats_data["total_visits"] += 1
        
        # 更新网站点击统计
        if website_name not in self.stats_data["website_clicks"]:
            self.stats_data["website_clicks"][website_name] = 0
        self.stats_data["website_clicks"][website_name] += 1
        
        # 更新分类偏好
        if category not in self.stats_data["favorite_categories"]:
            self.stats_data["favorite_categories"][category] = 0
        self.stats_data["favorite_categories"][category] += 1
        
        # 更新每日活动
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.stats_data["daily_activity"]:
            self.stats_data["daily_activity"][today] = {"visits": 0}
        self.stats_data["daily_activity"][today]["visits"] += 1
        
        # 更新最后登录时间
        self.stats_data["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存统计数据
        self.save_statistics()
    
    def get_popular_websites(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取热门网站列表"""
        websites = []
        for url, data in self.stats_data["website_visits"].items():
            websites.append({
                "url": url,
                "visits": data["count"],
                "last_visit": data["last_visit"],
                "unique_visitors": len(data["visitors"])
            })
        
        return sorted(websites, key=lambda x: x["visits"], reverse=True)[:limit]
    
    def get_daily_activity(self, days: int = 7) -> Dict[str, Dict[str, int]]:
        """获取每日活动统计"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)
        
        result = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            result[date_str] = self.stats_data["daily_activity"].get(date_str, {
                "logins": 0,
                "searches": 0,
                "visits": 0
            })
            current_date += timedelta(days=1)
        
        return result
    
    def get_user_activity_summary(self, username: str) -> Dict[str, Any]:
        """获取用户活动摘要"""
        if username not in self.stats_data["user_preferences"]:
            return {"error": "用户数据不存在"}
        
        user_data = self.stats_data["user_preferences"][username]
        
        return {
            "total_logins": len(user_data["login_times"]),
            "total_searches": len(user_data["search_keywords"]),
            "favorite_keywords": self._get_top_keywords(user_data["search_keywords"]),
            "login_pattern": self._analyze_login_pattern(user_data["login_times"]),
            "last_activity": user_data["login_times"][-1] if user_data["login_times"] else None
        }
    
    def _get_top_keywords(self, search_data: List[Dict[str, str]], limit: int = 5) -> List[str]:
        """获取用户最常搜索的关键词"""
        keyword_count = {}
        for search in search_data:
            keyword = search["keyword"]
            keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        
        return sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def _analyze_login_pattern(self, login_times: List[str]) -> Dict[str, Any]:
        """分析用户登录模式"""
        if not login_times:
            return {"pattern": "无数据"}
        
        hours = []
        for time_str in login_times:
            try:
                dt = datetime.fromisoformat(time_str)
                hours.append(dt.hour)
            except:
                continue
        
        if not hours:
            return {"pattern": "数据解析错误"}
        
        # 分析最活跃的时间段
        hour_count = {}
        for hour in hours:
            hour_count[hour] = hour_count.get(hour, 0) + 1
        
        most_active_hour = max(hour_count.items(), key=lambda x: x[1])
        
        return {
            "most_active_hour": most_active_hour[0],
            "activity_distribution": hour_count,
            "total_sessions": len(login_times)
        }
    
    def get_system_overview(self) -> Dict[str, Any]:
        """获取系统概览统计"""
        return {
            "total_logins": self.stats_data["login_count"],
            "total_searches": self.stats_data["search_count"],
            "total_websites": len(self.stats_data["website_visits"]),
            "active_users": len(self.stats_data["user_preferences"]),
            "system_performance": self.stats_data["system_performance"]
        }
    
    def get_top_categories(self, limit: int = 5):
        """获取最受欢迎的分类"""
        categories = self.stats_data.get("favorite_categories", {})
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        return sorted_categories[:limit]
    
    def get_top_websites(self, limit: int = 10):
        """获取最受欢迎的网站"""
        websites = self.stats_data.get("website_clicks", {})
        sorted_websites = sorted(websites.items(), key=lambda x: x[1], reverse=True)
        return sorted_websites[:limit]
    
    def get_recent_activity(self, days: int = 7):
        """获取最近几天的活动"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)
        
        result = []
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            activity_count = self.stats_data.get("daily_activity", {}).get(date_str, {}).get("visits", 0)
            result.append((date_str, activity_count))
            current_date += timedelta(days=1)
        
        return result