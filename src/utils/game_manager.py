#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏目录管理模块
"""

import os
import logging
from pathlib import Path
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class GameManager:
    """游戏目录管理类"""
    
    def __init__(self, base_dir: str = "data/games"):
        """
        初始化游戏管理器
        
        Args:
            base_dir: 游戏数据的基础目录
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def init_game(self, game_name: str) -> bool:
        """
        初始化新游戏目录
        
        Args:
            game_name: 游戏名称
            
        Returns:
            bool: 是否成功创建
        """
        try:
            # 创建游戏主目录
            game_dir = self.base_dir / game_name
            if game_dir.exists():
                logger.warning(f"游戏目录已存在: {game_dir}")
                return False
            
            # 创建子目录
            rules_dir = game_dir / "rules"
            translations_dir = game_dir / "translations"
            metadata_dir = game_dir / "metadata"
            
            for dir_path in [rules_dir, translations_dir, metadata_dir]:
                dir_path.mkdir(parents=True)
                logger.info(f"创建目录: {dir_path}")
            
            # 创建初始文件
            self._create_initial_files(game_dir)
            
            logger.info(f"成功初始化游戏目录: {game_dir}")
            return True
            
        except Exception as e:
            logger.error(f"初始化游戏目录失败: {e}")
            return False
    
    def _create_initial_files(self, game_dir: Path):
        """
        创建初始文件
        
        Args:
            game_dir: 游戏目录路径
        """
        # 创建游戏信息文件
        game_info = {
            "name": game_dir.name,
            "created_at": str(datetime.now()),
            "status": "initialized",
            "last_updated": str(datetime.now())
        }
        
        with open(game_dir / "metadata" / "game_info.json", "w", encoding="utf-8") as f:
            json.dump(game_info, f, ensure_ascii=False, indent=2)
        
        # 创建空的翻译文件
        for file_name in ["bga_translations.md", "my_translations.md"]:
            with open(game_dir / "translations" / file_name, "w", encoding="utf-8") as f:
                f.write("# 翻译内容\n\n")
        
        # 创建空的规则提取文件
        with open(game_dir / "rules" / "extracted.md", "w", encoding="utf-8") as f:
            f.write("# 规则书文本\n\n") 