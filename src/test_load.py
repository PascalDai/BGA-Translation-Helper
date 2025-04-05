import logging
import time
from .submitter import TranslationSubmitter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_load_and_login():
    """测试加载游戏信息和访问翻译页面"""
    submitter = TranslationSubmitter("propuh")
    
    try:
        # 1. 测试加载游戏信息
        module_id = submitter.load_game_info()
        print(f"\nmodule_id: {module_id}")
        
        # 2. 测试加载翻译对照表
        translations = submitter.load_translation_table()
        print(f"\n翻译总数: {len(translations)}")
        
        # 3. 测试登录和访问翻译页面
        submitter.translator.login()
        url = f"https://boardgamearena.com/translation?module_id={module_id}&source_locale=en_US&dest_locale=zh_CN&findtype=untranslated"
        print(f"\n访问页面: {url}")
        submitter.translator.driver.get(url)
        
        # 4. 等待页面加载并检查元素
        WebDriverWait(submitter.translator.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "translation_block"))
        )
        print("\n页面加载成功，找到翻译块元素")
        
        # 5. 获取并显示页面上的翻译块数量
        translation_blocks = submitter.translator.driver.find_elements(By.CLASS_NAME, "translation_block")
        print(f"页面上的翻译块数量: {len(translation_blocks)}")
        
        # 6. 显示第一个翻译块的原文（如果存在）
        if translation_blocks:
            original_text = translation_blocks[0].find_element(By.CLASS_NAME, "original_text").text.strip()
            print(f"第一个翻译块的原文: {original_text}")
        
        # 暂停5秒，让我们可以看到页面
        print("\n等待5秒查看页面...")
        time.sleep(5)
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
    finally:
        # 关闭浏览器
        submitter.translator.driver.quit()

if __name__ == "__main__":
    test_load_and_login() 