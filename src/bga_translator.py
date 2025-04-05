import os
from typing import Dict, Optional, List
from dotenv import load_dotenv, find_dotenv
from .bga_login import BGALogin
import json
import logging
from playwright.sync_api import sync_playwright, Page, Browser
from pathlib import Path

class BGATranslator:
    def __init__(self, game_name: str):
        # 加载环境变量
        env_path = find_dotenv()
        if not env_path:
            raise ValueError("未找到 .env 文件")
            
        load_dotenv(env_path)
        
        # 获取配置
        self.username = os.getenv('BGA_USERNAME')
        self.password = os.getenv('BGA_PASSWORD')
        self.game_name = game_name
        
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
        
        # 初始化 Playwright
        self.init_browser()
        
    def init_browser(self):
        """初始化 Playwright 浏览器"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=False,
                args=['--start-maximized']
            )
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            self.page = self.context.new_page()
            print("成功初始化浏览器")
        except Exception as e:
            print(f"初始化浏览器失败: {e}")
            raise
            
    def login(self) -> bool:
        """使用 Playwright 登录 BGA"""
        try:
            # 打开登录页面
            self.page.goto("https://boardgamearena.com/account")
            print("已打开登录页面")
            
            # 输入用户名
            self.page.locator("form").filter(has_text="下一个").get_by_placeholder("电子邮件或用户名").click()
            self.page.locator("form").filter(has_text="下一个").get_by_placeholder("电子邮件或用户名").fill(self.username)
            print(f"已输入用户名: {self.username}")
            
            # 点击"下一个"按钮
            self.page.get_by_role("link", name="下一个").click()
            print("已点击'下一个'按钮")
            
            # 输入密码
            self.page.get_by_role("textbox", name="密码").click()
            self.page.get_by_role("textbox", name="密码").fill(self.password)
            print("已输入密码")
            
            # 点击登录按钮
            self.page.locator("#account-module").get_by_role("link", name="登录", exact=True).click()
            print("已点击登录按钮")
            
            # 等待登录成功
            self.page.wait_for_load_state("networkidle")
            print("登录成功！")
            
            # 获取 module_id
            print("正在获取 module_id...")
            game_info_path = Path(f"data/games/{self.game_name}/metadata/game_info.json")
            if not game_info_path.exists():
                print(f"错误：找不到游戏信息文件 {game_info_path}")
                return False
                
            with open(game_info_path, 'r', encoding='utf-8') as f:
                game_info = json.load(f)
                module_id = game_info.get('id')
                if not module_id:
                    print("错误：游戏信息中没有找到 module_id")
                    return False
                    
            print(f"成功获取 module_id: {module_id}")
            
            # 跳转到翻译页面
            print("正在跳转到翻译页面...")
            translation_url = f"https://boardgamearena.com/translation?module_id={module_id}&source_locale=en_US&dest_locale=zh_CN&findtype=untranslated"
            self.page.goto(translation_url)
            self.page.wait_for_load_state("networkidle")
            print("已跳转到翻译页面，请开始录制翻译操作...")
            
            return True
        except Exception as e:
            print(f"登录失败: {str(e)}")
            return False
            
    def __del__(self):
        """析构函数，确保关闭浏览器"""
        if hasattr(self, 'context'):
            self.context.close()
        if hasattr(self, 'browser'):
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
    
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
        try:
            self.logger.info(f"开始获取游戏 {game_id} 的翻译内容...")
            
            # 获取游戏信息
            game_info_path = Path(f"data/games/{game_id}/metadata/game_info.json")
            if not game_info_path.exists():
                self.logger.error(f"错误：找不到游戏信息文件 {game_info_path}")
                return None
                
            with open(game_info_path, 'r', encoding='utf-8') as f:
                game_info = json.load(f)
                module_id = game_info.get('id')
                if not module_id:
                    self.logger.error("错误：游戏信息中没有找到 module_id")
                    return None
                    
            self.logger.info(f"成功获取 module_id: {module_id}")
            
            # 创建翻译目录
            translations_dir = Path(f"data/games/{game_id}/translations")
            translations_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. 获取所有翻译内容
            self.logger.info("正在获取所有翻译内容...")
            all_translations_url = f"https://boardgamearena.com/translation?module_id={module_id}&source_locale=en_US&dest_locale=zh_CN&findtype=all"
            self.page.goto(all_translations_url)
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(5000)  # 等待5秒确保页面加载完成
            
            all_translations = {}
            all_textareas = self.page.locator("textarea[id^='toTranslate_']").all()
            
            for textarea in all_textareas:
                try:
                    original_id = textarea.get_attribute("id")
                    if not original_id:
                        continue
                        
                    original_text = textarea.evaluate("node => node.value")
                    if not original_text:
                        continue
                        
                    # 获取原文出处
                    context_elem = self.page.locator(f"#context_{original_id.split('_')[1]}")
                    context = context_elem.inner_text() if context_elem.count() > 0 else ""
                    
                    # 获取已有的翻译（如果有）
                    translation_textarea = self.page.locator(f"#translation_{original_id.split('_')[1]}")
                    translation = translation_textarea.evaluate("node => node.value") if translation_textarea.count() > 0 else ""
                    
                    all_translations[original_id] = {
                        "original": original_text,
                        "context": context,
                        "translation": translation
                    }
                    
                except Exception as e:
                    self.logger.error(f"处理翻译项时出错: {e}")
                    continue
            
            # 2. 获取未翻译内容
            self.logger.info("正在获取未翻译内容...")
            untranslated_url = f"https://boardgamearena.com/translation?module_id={module_id}&source_locale=en_US&dest_locale=zh_CN&findtype=untranslated"
            self.page.goto(untranslated_url)
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(5000)
            
            untranslated = {}
            untranslated_textareas = self.page.locator("textarea[id^='toTranslate_']").all()
            
            for textarea in untranslated_textareas:
                try:
                    original_id = textarea.get_attribute("id")
                    if not original_id:
                        continue
                        
                    original_text = textarea.evaluate("node => node.value")
                    if not original_text:
                        continue
                        
                    context_elem = self.page.locator(f"#context_{original_id.split('_')[1]}")
                    context = context_elem.inner_text() if context_elem.count() > 0 else ""
                    
                    untranslated[original_id] = {
                        "original": original_text,
                        "context": context,
                        "translation": ""
                    }
                    
                except Exception as e:
                    self.logger.error(f"处理未翻译项时出错: {e}")
                    continue
            
            # 保存所有翻译内容
            all_json_path = translations_dir / "all_translations.json"
            with open(all_json_path, "w", encoding="utf-8") as f:
                json.dump(all_translations, f, ensure_ascii=False, indent=2)
                
            # 保存未翻译内容
            untranslated_json_path = translations_dir / "untranslated.json"
            with open(untranslated_json_path, "w", encoding="utf-8") as f:
                json.dump(untranslated, f, ensure_ascii=False, indent=2)
                
            # 生成所有翻译的对照表
            all_md_content = "| 原文 | 原文出处 | 当前译文 |\n|------|----------|----------|\n"
            for item in all_translations.values():
                all_md_content += f"| {item['original']} | {item['context']} | {item['translation']} |\n"
                
            all_md_path = translations_dir / "all_translations.md"
            with open(all_md_path, "w", encoding="utf-8") as f:
                f.write(all_md_content)
                
            # 生成未翻译内容的对照表
            untranslated_md_content = "| 原文 | 原文出处 | 译文 |\n|------|----------|------|\n"
            for item in untranslated.values():
                untranslated_md_content += f"| {item['original']} | {item['context']} | |\n"
                
            untranslated_md_path = translations_dir / "untranslated.md"
            with open(untranslated_md_path, "w", encoding="utf-8") as f:
                f.write(untranslated_md_content)
                
            self.logger.info(f"成功保存翻译内容到 {translations_dir}")
            self.logger.info(f"- 所有翻译JSON：{all_json_path}")
            self.logger.info(f"- 所有翻译Markdown：{all_md_path}")
            self.logger.info(f"- 未翻译JSON：{untranslated_json_path}")
            self.logger.info(f"- 未翻译Markdown：{untranslated_md_path}")
            
            return {"all": all_translations, "untranslated": untranslated}
            
        except Exception as e:
            self.logger.error(f"获取翻译内容时发生错误: {str(e)}")
            return None
    
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