#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BGA 翻译助手主程序
"""

import os
import logging
import argparse
from pathlib import Path
from .ocr import OCRManager
from .bga_translator import BGATranslator
from .submitter.translation_submitter import TranslationSubmitter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GameManager:
    """游戏管理器类"""
    
    def __init__(self, game_name: str):
        """
        初始化游戏管理器
        
        Args:
            game_name: 游戏名称
        """
        self.game_name = game_name
        self.base_dir = Path("data/games") / game_name
        self.rules_dir = self.base_dir / "rules"
        self.translations_dir = self.base_dir / "translations"
        self.metadata_dir = self.base_dir / "metadata"
        
        # 创建必要的目录
        self._create_directories()
    
    def _create_directories(self):
        """创建必要的目录"""
        try:
            os.makedirs(self.rules_dir, exist_ok=True)
            os.makedirs(self.translations_dir, exist_ok=True)
            os.makedirs(self.metadata_dir, exist_ok=True)
            logger.info(f"成功创建游戏目录: {self.game_name}")
        except Exception as e:
            logger.error(f"创建游戏目录失败: {e}")
            raise
    
    def fetch_game_info(self):
        """获取游戏信息"""
        try:
            # 初始化翻译器
            translator = BGATranslator()
            
            # 登录 BGA
            if not translator.login():
                raise Exception("登录失败")
            
            # 获取游戏信息
            if translator.update_game_info(self.game_name):
                logger.info(f"成功获取游戏 {self.game_name} 的信息")
            else:
                raise Exception(f"获取游戏 {self.game_name} 的信息失败")
                
        except Exception as e:
            logger.error(f"获取游戏信息失败: {e}")
            raise
    
    def fetch_translations(self):
        """获取翻译内容"""
        try:
            # 初始化翻译器
            translator = BGATranslator(self.game_name)
            
            # 登录 BGA
            if not translator.login():
                raise Exception("登录失败")
            
            # 获取翻译内容
            translations = translator.get_translations(self.game_name)
            if translations:
                logger.info(f"成功获取游戏 {self.game_name} 的翻译内容")
                return True
            else:
                raise Exception(f"获取游戏 {self.game_name} 的翻译内容失败")
                
        except Exception as e:
            logger.error(f"获取翻译内容失败: {e}")
            raise
    
    def process_rulebook(self):
        """处理规则书"""
        try:
            # 检查规则书是否存在
            rulebook_path = self.rules_dir / "original.pdf"
            if not rulebook_path.exists():
                raise FileNotFoundError(f"规则书不存在: {rulebook_path}")
            
            # 初始化 OCR 管理器
            ocr_manager = OCRManager()
            
            # 处理规则书
            logger.info("开始处理规则书...")
            extracted_text = ocr_manager.process_pdf(str(rulebook_path))
            
            # 保存提取的文本
            output_path = self.rules_dir / "extracted.md"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            
            logger.info(f"规则书处理完成，文本已保存至: {output_path}")
            
        except Exception as e:
            logger.error(f"处理规则书失败: {e}")
            raise

def submit_translations(args):
    """提交翻译内容到BGA平台"""
    try:
        logger.info(f"开始提交游戏 {args.game_name} 的翻译内容...")
        submitter = TranslationSubmitter(args.game_name)
        if submitter.submit_translations():
            logger.info("翻译提交成功！")
        else:
            logger.error("翻译提交失败，请查看日志了解详情。")
    except Exception as e:
        logger.error(f"提交翻译时发生错误: {e}")
        raise

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="BGA 翻译助手")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 初始化游戏命令
    init_parser = subparsers.add_parser("init-game", help="初始化游戏目录")
    init_parser.add_argument("game_name", help="游戏名称")
    
    # 处理规则书命令
    process_parser = subparsers.add_parser("process-rulebook", help="处理规则书")
    process_parser.add_argument("game_name", help="游戏名称")
    
    # 获取游戏信息命令
    fetch_info_parser = subparsers.add_parser("fetch-game-info", help="获取游戏信息")
    fetch_info_parser.add_argument("game_name", help="游戏名称")
    
    # 获取翻译内容命令
    fetch_trans_parser = subparsers.add_parser("fetch-translation", help="获取翻译内容")
    fetch_trans_parser.add_argument("game_name", help="游戏名称")
    
    # 添加提交翻译命令
    submit_parser = subparsers.add_parser('submit-translations', help='提交翻译内容')
    submit_parser.add_argument('game_name', help='游戏名称')
    submit_parser.set_defaults(func=submit_translations)
    
    args = parser.parse_args()
    
    try:
        game_manager = GameManager(args.game_name)
        
        if args.command == "init-game":
            logger.info(f"游戏 {args.game_name} 初始化完成")
            
        elif args.command == "process-rulebook":
            game_manager.process_rulebook()
            
        elif args.command == "fetch-game-info":
            game_manager.fetch_game_info()
            
        elif args.command == "fetch-translation":
            game_manager.fetch_translations()
            
        elif args.command == "submit-translations":
            submit_translations(args)
            
        else:
            parser.print_help()
            
    except Exception as e:
        logger.error(f"操作失败: {e}")

if __name__ == "__main__":
    main() 