#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BGA 爬虫模块
负责从 BGA 平台获取翻译内容
"""

import logging
import os
import time
from pathlib import Path
from typing import Optional, Dict, List
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

class BGACrawler:
    """BGA 爬虫类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.session = requests.Session()
        self.base_url = "https://boardgamearena.com"
        self.is_logged_in = False
        
        # 配置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        # 初始化会话
        self._init_session()
    
    def _init_session(self):
        """初始化会话"""
        try:
            # 获取登录页面
            response = self.session.get(
                f"{self.base_url}/account",
                headers=self.headers
            )
            response.raise_for_status()
            
            # 解析 CSRF token
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token = soup.find('meta', {'name': 'csrf-token'})
            if csrf_token:
                self.headers['X-CSRF-TOKEN'] = csrf_token['content']
            
            logger.info("会话初始化成功")
            
        except Exception as e:
            logger.error(f"会话初始化失败: {e}")
            raise
    
    def login(self) -> bool:
        """
        登录 BGA 平台
        
        Returns:
            bool: 登录是否成功
        """
        try:
            # 获取登录凭据
            username = os.getenv("BGA_USERNAME")
            password = os.getenv("BGA_PASSWORD")
            
            if not username or not password:
                raise ValueError("未设置 BGA 账号信息，请在 .env 文件中配置")
            
            # 准备登录数据
            login_data = {
                "email": username,
                "password": password,
                "remember": "1"
            }
            
            # 发送登录请求
            response = self.session.post(
                f"{self.base_url}/account/login",
                data=login_data,
                headers=self.headers,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # 检查登录状态
            self.is_logged_in = "account" in response.url
            if self.is_logged_in:
                logger.info("BGA 登录成功")
            else:
                logger.error("BGA 登录失败")
            
            return self.is_logged_in
            
        except Exception as e:
            logger.error(f"BGA 登录失败: {e}")
            return False
    
    def get_game_translations(self, game_name: str) -> Optional[Dict]:
        """
        获取游戏翻译内容
        
        Args:
            game_name: 游戏名称
            
        Returns:
            Optional[Dict]: 翻译内容，如果获取失败则返回 None
        """
        try:
            if not self.is_logged_in:
                if not self.login():
                    return None
            
            # 获取翻译页面
            response = self.session.get(
                f"{self.base_url}/translation/translation?game={game_name}",
                headers=self.headers
            )
            response.raise_for_status()
            
            # 解析翻译内容
            soup = BeautifulSoup(response.text, 'html.parser')
            translations = {}
            
            # TODO: 实现翻译内容解析
            # 这里需要根据实际页面结构来实现
            
            return translations
            
        except Exception as e:
            logger.error(f"获取游戏翻译失败: {e}")
            return None
    
    def save_translations(self, game_name: str, translations: Dict) -> bool:
        """
        保存翻译内容到文件
        
        Args:
            game_name: 游戏名称
            translations: 翻译内容
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 创建保存目录
            save_dir = Path("data/games") / game_name / "translations"
            save_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存翻译内容
            with open(save_dir / "bga_translations.md", "w", encoding="utf-8") as f:
                f.write("# BGA 翻译内容\n\n")
                for key, value in translations.items():
                    f.write(f"## {key}\n\n")
                    f.write(f"{value}\n\n")
            
            logger.info(f"翻译内容已保存到: {save_dir / 'bga_translations.md'}")
            return True
            
        except Exception as e:
            logger.error(f"保存翻译内容失败: {e}")
            return False 