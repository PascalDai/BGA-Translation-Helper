#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BGA Translation Helper 主程序入口
"""

import argparse
import logging
from pathlib import Path
from utils.game_manager import GameManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_game(args):
    """初始化新游戏目录"""
    logger.info(f"正在初始化游戏: {args.game_name}")
    
    game_manager = GameManager()
    if game_manager.init_game(args.game_name):
        logger.info(f"游戏 {args.game_name} 初始化成功")
    else:
        logger.error(f"游戏 {args.game_name} 初始化失败")

def extract_text(args):
    """提取规则书文本"""
    logger.info(f"正在提取游戏规则文本: {args.game_name}")
    # TODO: 实现文本提取逻辑

def fetch_translations(args):
    """获取BGA翻译"""
    logger.info(f"正在获取BGA翻译: {args.game_name}")
    # TODO: 实现翻译获取逻辑

def start_translation(args):
    """开始翻译"""
    logger.info(f"开始翻译: {args.game_name}")
    # TODO: 实现翻译界面逻辑

def main():
    parser = argparse.ArgumentParser(description='BGA Translation Helper')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 初始化游戏命令
    init_parser = subparsers.add_parser('init-game', help='初始化新游戏')
    init_parser.add_argument('game_name', help='游戏名称')
    init_parser.set_defaults(func=init_game)

    # 提取文本命令
    extract_parser = subparsers.add_parser('extract-text', help='提取规则书文本')
    extract_parser.add_argument('game_name', help='游戏名称')
    extract_parser.set_defaults(func=extract_text)

    # 获取翻译命令
    fetch_parser = subparsers.add_parser('fetch-translations', help='获取BGA翻译')
    fetch_parser.add_argument('game_name', help='游戏名称')
    fetch_parser.set_defaults(func=fetch_translations)

    # 开始翻译命令
    translate_parser = subparsers.add_parser('start-translation', help='开始翻译')
    translate_parser.add_argument('game_name', help='游戏名称')
    translate_parser.set_defaults(func=start_translation)

    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 