import os
from typing import Dict, Optional, List
from dotenv import load_dotenv, find_dotenv
from .bga_login import BGALogin
import json
import logging

class BGATranslator:
    def __init__(self):
        # 加载环境变量
        env_path = find_dotenv()
        if not env_path:
            raise ValueError("未找到 .env 文件")
            
        load_dotenv(env_path)
        
        # 获取配置
        self.username = os.getenv('BGA_USERNAME')
        self.password = os.getenv('BGA_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("请在 .env 文件中配置 BGA_USERNAME 和 BGA_PASSWORD")
            
        print(f"已加载配置: 用户名={self.username}")
            
        # 初始化登录客户端
        self.client = BGALogin(username=self.username, password=self.password)
        
        # 创建游戏数据目录
        self.games_dir = "data/games"
        os.makedirs(self.games_dir, exist_ok=True)
        
        # 配置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def login(self) -> bool:
        """
        使用配置的账号密码登录 BGA
        
        Returns:
            bool: 登录是否成功
        """
        try:
            print(f"正在使用账号 {self.username} 登录...")
            
            # 获取 request_token
            token = self.client.get_request_token()
            if not token:
                print("获取 request_token 失败")
                return False
            
            # 检查用户名
            check_result = self.client.check_username(self.username)
            if not check_result.get('success', False):
                print(f"用户名检查失败: {check_result.get('error', '未知错误')}")
                return False
            
            # 进行登录
            result = self.client.login_with_password(
                username=self.username,
                password=self.password
            )
            
            # 检查登录结果
            if result.get('success', False):
                print("登录成功")
                return True
            else:
                print(f"登录失败: {result.get('error', '未知错误')}")
                return False
        except Exception as e:
            print(f"登录失败: {str(e)}")
            return False
    
    def get_game_list(self) -> List[Dict]:
        """获取所有游戏列表"""
        try:
            url = "https://boardgamearena.com/gamelist/gamelist/gameList.html"
            response = self.client.session.post(url, headers={
                'x-request-token': self.client.request_token,
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 1:
                    return data.get('data', [])
                else:
                    self.logger.error(f"获取游戏列表失败: {data.get('error', '未知错误')}")
            else:
                self.logger.error(f"获取游戏列表失败，状态码: {response.status_code}")
                
            return []
        except Exception as e:
            self.logger.error(f"获取游戏列表时发生错误: {str(e)}")
            return []
    
    def get_game_details(self, game_id: str) -> Optional[Dict]:
        """获取指定游戏的详细信息"""
        try:
            url = "https://boardgamearena.com/gamelist/gamelist/gameDetails.html"
            self.logger.info(f"正在获取游戏 {game_id} 的详情...")
            self.logger.info(f"请求 URL: {url}")
            self.logger.info(f"请求头: {self.client.request_token}")
            
            response = self.client.session.post(url, headers={
                'x-request-token': self.client.request_token,
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'origin': 'https://boardgamearena.com',
                'referer': 'https://boardgamearena.com/translationhq'
            }, data={
                'game': game_id,
                'gamemode': 'realtime',
                'withtime': 'true',
                'rankingmode': 'simple'
            })
            
            self.logger.info(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
                
                # 检查响应状态
                if data.get('status') == 1:
                    return data.get('results', {})
                else:
                    self.logger.error(f"获取游戏详情失败: {data.get('error', '未知错误')}")
            else:
                self.logger.error(f"获取游戏详情失败，状态码: {response.status_code}")
                
            return None
        except Exception as e:
            self.logger.error(f"获取游戏详情时发生错误: {str(e)}")
            return None
    
    def save_game_data(self, game_id: str, data: Dict) -> bool:
        """
        保存游戏数据到文件
        
        Args:
            game_id: 游戏ID
            data: 游戏数据
            
        Returns:
            bool: 保存是否成功
        """
        try:
            game_dir = os.path.join(self.games_dir, game_id)
            os.makedirs(game_dir, exist_ok=True)
            
            # 分离游戏详情和翻译页面内容
            translation_page = data.pop('translation_page', '')
            
            # 保存游戏详情
            with open(os.path.join(game_dir, 'details.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 保存翻译页面
            if translation_page:
                with open(os.path.join(game_dir, 'translation.html'), 'w', encoding='utf-8') as f:
                    f.write(translation_page)
                
            self.logger.info(f"已保存游戏 {game_id} 的数据")
            return True
        except Exception as e:
            self.logger.error(f"保存游戏数据时发生错误: {str(e)}")
            return False
    
    def get_translations(self, game_id: str) -> Optional[Dict]:
        """
        获取游戏的翻译内容
        
        Args:
            game_id: 游戏ID
            
        Returns:
            Optional[Dict]: 翻译内容，如果获取失败则返回 None
        """
        # TODO: 实现获取翻译内容的功能
        pass
    
    def update_game_info(self, game_id: str) -> bool:
        """
        更新游戏信息到 game_info.json 文件
        
        Args:
            game_id: 游戏ID
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 获取游戏详情
            details = self.get_game_details(game_id)
            if not details:
                self.logger.error(f"无法获取游戏 {game_id} 的详情")
                return False
                
            # 创建游戏目录结构
            game_dir = os.path.join(self.games_dir, game_id)
            metadata_dir = os.path.join(game_dir, 'metadata')
            os.makedirs(metadata_dir, exist_ok=True)
            
            # 保存游戏信息
            game_info_path = os.path.join(metadata_dir, 'game_info.json')
            with open(game_info_path, 'w', encoding='utf-8') as f:
                json.dump(details, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"已更新游戏 {game_id} 的信息到 {game_info_path}")
            return True
        except Exception as e:
            self.logger.error(f"更新游戏信息时发生错误: {str(e)}")
            return False 