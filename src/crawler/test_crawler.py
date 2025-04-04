#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BGA 爬虫测试脚本
"""

import logging
from pathlib import Path
from bga_crawler import BGACrawler

def main():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # 初始化爬虫
        crawler = BGACrawler()
        logger.info("爬虫初始化成功")
        
        # 测试登录
        if crawler.login():
            logger.info("登录测试成功")
            
            # 测试获取翻译
            game_name = "Propuh"
            translations = crawler.get_game_translations(game_name)
            
            if translations:
                # 保存翻译
                if crawler.save_translations(game_name, translations):
                    logger.info("翻译保存成功")
                else:
                    logger.error("翻译保存失败")
            else:
                logger.error("获取翻译失败")
        else:
            logger.error("登录测试失败")
            
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")

if __name__ == "__main__":
    main() 