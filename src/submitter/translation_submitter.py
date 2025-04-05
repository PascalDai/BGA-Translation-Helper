import logging
import json
from pathlib import Path
from typing import Optional
from playwright.sync_api import sync_playwright, Page, Browser
import os
from dotenv import load_dotenv, find_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler('translation.log')  # 输出到文件
    ]
)

logger = logging.getLogger(__name__)

class TranslationSubmitter:
    def __init__(self, game_name: str):
        self.game_name = game_name
        self.game_dir = Path(f"data/games/{game_name}")
        self.untranslated_path = self.game_dir / "translations/untranslated.md"
        self.game_info_path = self.game_dir / "metadata/game_info.json"
        
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
            
        logger.info(f"已加载配置: 用户名={self.username}")
        
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
            logger.info("成功初始化浏览器")
        except Exception as e:
            logger.error(f"初始化浏览器失败: {e}")
            raise
            
    def __del__(self):
        """析构函数，确保关闭浏览器"""
        if hasattr(self, 'context'):
            self.context.close()
        if hasattr(self, 'browser'):
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
            
    def load_game_info(self) -> Optional[int]:
        """加载游戏信息，返回module_id"""
        try:
            with open(self.game_info_path, 'r', encoding='utf-8') as f:
                game_info = json.load(f)
                module_id = game_info.get('id')
                logger.info(f"成功加载游戏信息，module_id: {module_id}")
                return module_id
        except Exception as e:
            logger.error(f"加载游戏信息失败: {e}")
            return None
            
    def load_translation_table(self) -> dict:
        """加载翻译对照表"""
        translations = {}
        try:
            with open(self.untranslated_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 解析翻译对照表
                for line in content.split('\n'):
                    if '|' in line and '原文' in line and '译文' in line:
                        continue
                    if '|' in line and line.count('|') >= 3:  # 确保至少有3列
                        parts = [part.strip() for part in line.split('|')]
                        if len(parts) >= 4:  # 分割后应该至少有4部分：空、原文、原文出处、译文
                            original = parts[1]  # 第2列是原文
                            translation = parts[3]  # 第4列是译文
                            if original and translation and translation != '':  # 确保译文不为空
                                translations[original] = translation
                                logger.debug(f"加载翻译: {original} -> {translation}")
                logger.info(f"成功加载翻译对照表，共 {len(translations)} 条翻译")
                # 打印前5条翻译作为示例
                for i, (original, translation) in enumerate(list(translations.items())[:5]):
                    logger.info(f"示例翻译 {i+1}:")
                    logger.info(f"原文: {original}")
                    logger.info(f"译文: {translation}")
        except Exception as e:
            logger.error(f"加载翻译对照表失败: {e}")
        return translations
        
    def submit_translations(self) -> bool:
        """提交翻译内容"""
        try:
            # 1. 加载必要数据
            module_id = self.load_game_info()
            if not module_id:
                logger.error("无法获取module_id")
                return False
                
            translations = self.load_translation_table()
            if not translations:
                logger.error("没有可用的翻译内容")
                return False
                
            # 2. 登录并访问翻译页面
            logger.info("正在登录...")
            # 打开登录页面
            logger.info("正在打开登录页面...")
            self.page.goto("https://boardgamearena.com/account")
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(2000)  # 等待2秒确保页面完全加载
            logger.info(f"当前页面URL: {self.page.url}")
            
            # 输入用户名
            logger.info("正在输入用户名...")
            username_input = self.page.locator("form").filter(has_text="下一个").get_by_placeholder("电子邮件或用户名")
            username_input.wait_for(state="visible")  # 等待输入框可见
            username_input.click()
            username_input.fill(self.username)
            logger.info("用户名输入完成")
            
            # 点击"下一个"按钮
            logger.info("正在点击'下一个'按钮...")
            next_button = self.page.get_by_role("link", name="下一个")
            next_button.wait_for(state="visible")  # 等待按钮可见
            next_button.click()
            
            # 等待页面响应
            logger.info("等待密码输入页面加载...")
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(2000)  # 等待2秒
            logger.info(f"当前页面URL: {self.page.url}")
            
            # 输入密码
            logger.info("正在输入密码...")
            password_input = self.page.get_by_role("textbox", name="密码")
            password_input.wait_for(state="visible")  # 等待密码输入框可见
            password_input.click()
            password_input.fill(self.password)
            logger.info("密码输入完成")
            
            # 点击登录按钮
            logger.info("正在点击登录按钮...")
            login_button = self.page.locator("#account-module").get_by_role("link", name="登录", exact=True)
            login_button.wait_for(state="visible")  # 等待登录按钮可见
            login_button.click()
            
            # 等待登录成功
            logger.info("等待登录完成...")
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(5000)  # 等待5秒确保登录完成
            logger.info(f"当前页面URL: {self.page.url}")
            logger.info("登录成功！")
            
            # 先访问主页，确保登录状态生效
            logger.info("访问主页，确认登录状态...")
            self.page.goto("https://boardgamearena.com/")
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(5000)  # 等待5秒
            logger.info(f"当前页面URL: {self.page.url}")
            
            # 跳转到翻译页面
            logger.info("正在跳转到翻译页面...")
            translation_url = f"https://boardgamearena.com/translation?module_id={module_id}&source_locale=en_US&dest_locale=zh_CN&findtype=untranslated"
            logger.info(f"目标URL: {translation_url}")
            self.page.goto(translation_url)
            
            # 等待页面完全加载
            logger.info("等待页面加载...")
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(8000)  # 等待8秒，确保页面完全加载
            logger.info(f"当前页面URL: {self.page.url}")
            
            # 检查是否成功跳转到翻译页面
            current_url = self.page.url
            if "translation" not in current_url or str(module_id) not in current_url:
                logger.error(f"跳转失败，当前页面: {current_url}")
                logger.error("页面内容:")
                logger.error(self.page.content())
                return False
                
            logger.info("成功跳转到翻译页面")
            
            # 等待翻译块加载
            logger.info("等待翻译块加载...")
            try:
                while True:  # 循环处理每一页
                    # 先检查页面内容
                    logger.info("检查页面内容...")
                    page_content = self.page.content()
                    logger.info(f"页面内容长度: {len(page_content)}")
                    
                    # 直接查找原文输入框
                    logger.info("查找原文输入框...")
                    original_textareas = self.page.locator("textarea[id^='toTranslate_']").all()
                    total_blocks = len(original_textareas)
                    logger.info(f"找到 {total_blocks} 个原文输入框")
                    
                    if not original_textareas:
                        logger.info("当前页面没有找到需要翻译的内容，检查是否还有下一页...")
                        # 查找下一页按钮
                        next_page = self.page.locator("a.pagination_next")
                        if next_page.count() > 0 and not next_page.is_disabled():
                            logger.info("找到下一页按钮，点击进入下一页...")
                            next_page.click()
                            self.page.wait_for_load_state("networkidle")
                            self.page.wait_for_timeout(5000)  # 等待页面加载
                            continue
                        else:
                            logger.info("没有下一页了，翻译任务完成")
                            break
                    
                    # 处理每个翻译块
                    logger.info("=== 开始处理翻译 ===")
                    for textarea in original_textareas:
                        try:
                            # 获取原文输入框的ID和内容
                            original_id = textarea.get_attribute("id")
                            if not original_id:
                                logger.error("无法获取原文输入框ID")
                                continue
                                
                            # 使用evaluate处理JavaScript来获取文本内容
                            original_text = textarea.evaluate("node => node.value")
                            if not original_text:
                                logger.error(f"无法获取原文内容，ID: {original_id}")
                                continue
                                
                            logger.info(f"原文: {original_text}")
                            
                            # 查找对应的翻译
                            if original_text not in translations:
                                logger.warning(f"未找到原文的翻译: {original_text}")
                                continue
                                
                            translation = translations[original_text]
                            logger.info(f"找到对应翻译: {translation}")
                            
                            # 构造并定位译文输入框
                            translated_id = original_id.replace("toTranslate_", "translated_")
                            translated_textarea = self.page.locator(f"textarea#{translated_id}")
                            
                            # 填写译文
                            translated_textarea.wait_for(state="visible")
                            translated_textarea.click()
                            translated_textarea.fill(translation)
                            logger.info(f"已填写翻译到 {translated_id}")
                            
                            # 等待一小段时间，避免操作太快
                            self.page.wait_for_timeout(500)  # 等待0.5秒
                            
                        except Exception as e:
                            logger.error(f"处理翻译块时出错: {e}")
                            
                    logger.info("=== 当前页翻译处理结束 ===")
                    
                    # 检查是否有下一页
                    next_page = self.page.locator("a.pagination_next")
                    if next_page.count() > 0 and not next_page.is_disabled():
                        logger.info("找到下一页按钮，点击进入下一页...")
                        next_page.click()
                        self.page.wait_for_load_state("networkidle")
                        self.page.wait_for_timeout(5000)  # 等待页面加载
                    else:
                        logger.info("没有下一页了，翻译任务完成")
                        break
                    
            except Exception as e:
                logger.error(f"查找翻译块时出错: {e}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"提交翻译失败: {e}")
            return False 