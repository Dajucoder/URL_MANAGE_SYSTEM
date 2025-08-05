#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网站数据管理模块
管理推荐网站的数据
"""

# 推荐网站数据
RECOMMENDED_WEBSITES = {
    "学习教育": [
        {
            "name": "📚 中国大学MOOC",
            "url": "https://www.icourse163.org/",
            "description": "国家智慧教育平台，提供优质在线课程",
            "category": "在线教育",
            "rating": 5
        },
        {
            "name": "🎓 学堂在线",
            "url": "https://www.xuetangx.com/",
            "description": "清华大学发起的精品在线课程平台",
            "category": "在线教育", 
            "rating": 5
        },
        {
            "name": "📖 知乎",
            "url": "https://www.zhihu.com/",
            "description": "中文互联网高质量的问答社区",
            "category": "知识问答",
            "rating": 4
        },
        {
            "name": "💻 菜鸟教程",
            "url": "https://www.runoob.com/",
            "description": "提供编程技术教程的学习平台",
            "category": "编程学习",
            "rating": 5
        }
    ],
    "开发工具": [
        {
            "name": "🐙 GitHub",
            "url": "https://github.com/",
            "description": "全球最大的代码托管平台",
            "category": "代码托管",
            "rating": 5
        },
        {
            "name": "🔧 Stack Overflow",
            "url": "https://stackoverflow.com/",
            "description": "程序员问答社区",
            "category": "技术问答",
            "rating": 5
        },
        {
            "name": "📝 CodePen",
            "url": "https://codepen.io/",
            "description": "前端代码在线编辑器",
            "category": "在线编辑",
            "rating": 4
        },
        {
            "name": "🎨 Figma",
            "url": "https://www.figma.com/",
            "description": "协作式界面设计工具",
            "category": "设计工具",
            "rating": 5
        }
    ],
    "娱乐休闲": [
        {
            "name": "🎵 网易云音乐",
            "url": "https://music.163.com/",
            "description": "发现音乐，遇见美好",
            "category": "音乐平台",
            "rating": 5
        },
        {
            "name": "📺 哔哩哔哩",
            "url": "https://www.bilibili.com/",
            "description": "年轻人的文化社区",
            "category": "视频平台",
            "rating": 5
        },
        {
            "name": "🎮 Steam",
            "url": "https://store.steampowered.com/",
            "description": "PC游戏数字发行平台",
            "category": "游戏平台",
            "rating": 5
        },
        {
            "name": "📖 豆瓣",
            "url": "https://www.douban.com/",
            "description": "书影音记录生活",
            "category": "文化社区",
            "rating": 4
        }
    ],
    "实用工具": [
        {
            "name": "🌐 百度",
            "url": "https://www.baidu.com/",
            "description": "全球最大的中文搜索引擎",
            "category": "搜索引擎",
            "rating": 4
        },
        {
            "name": "📧 QQ邮箱",
            "url": "https://mail.qq.com/",
            "description": "腾讯邮箱服务",
            "category": "邮箱服务",
            "rating": 4
        },
        {
            "name": "☁️ 百度网盘",
            "url": "https://pan.baidu.com/",
            "description": "个人云存储服务",
            "category": "云存储",
            "rating": 4
        },
        {
            "name": "🗺️ 高德地图",
            "url": "https://www.amap.com/",
            "description": "专业的地图导航服务",
            "category": "地图导航",
            "rating": 5
        }
    ],
    "新闻资讯": [
        {
            "name": "📰 新浪新闻",
            "url": "https://news.sina.com.cn/",
            "description": "及时准确的新闻资讯",
            "category": "新闻门户",
            "rating": 4
        },
        {
            "name": "💼 36氪",
            "url": "https://36kr.com/",
            "description": "科技创业资讯平台",
            "category": "科技资讯",
            "rating": 4
        },
        {
            "name": "🏢 虎嗅网",
            "url": "https://www.huxiu.com/",
            "description": "商业资讯与观点平台",
            "category": "商业资讯",
            "rating": 4
        },
        {
            "name": "📱 IT之家",
            "url": "https://www.ithome.com/",
            "description": "IT科技资讯网站",
            "category": "科技资讯",
            "rating": 4
        }
    ]
}

def get_all_categories():
    """获取所有分类"""
    return list(RECOMMENDED_WEBSITES.keys())

def get_websites_by_category(category):
    """根据分类获取网站"""
    return RECOMMENDED_WEBSITES.get(category, [])

def get_all_websites():
    """获取所有网站"""
    all_websites = []
    for category, websites in RECOMMENDED_WEBSITES.items():
        for website in websites:
            website_copy = website.copy()
            website_copy['category_group'] = category
            all_websites.append(website_copy)
    return all_websites

def search_websites(keyword):
    """搜索网站"""
    results = []
    keyword = keyword.lower()
    
    for category, websites in RECOMMENDED_WEBSITES.items():
        for website in websites:
            if (keyword in website['name'].lower() or 
                keyword in website['description'].lower() or
                keyword in website['category'].lower()):
                website_copy = website.copy()
                website_copy['category_group'] = category
                results.append(website_copy)
    
    return results

def get_top_rated_websites(limit=10):
    """获取评分最高的网站"""
    all_websites = get_all_websites()
    sorted_websites = sorted(all_websites, key=lambda x: x['rating'], reverse=True)
    return sorted_websites[:limit]