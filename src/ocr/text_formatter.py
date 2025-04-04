#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文本格式化模块
负责处理和格式化提取的文本
"""

import logging
import re
from typing import List

logger = logging.getLogger(__name__)

class TextFormatter:
    """文本格式化类"""
    
    def __init__(self):
        """初始化文本格式化器"""
        # 编译常用的正则表达式
        self.whitespace_pattern = re.compile(r'\s+')
        self.page_number_pattern = re.compile(r'^\s*\d+\s*$')
        self.empty_line_pattern = re.compile(r'^\s*$')
    
    def format_text(self, text: str) -> str:
        """
        格式化文本
        
        Args:
            text: 原始文本
            
        Returns:
            str: 格式化后的文本
        """
        try:
            # 分割文本为行
            lines = text.split('\n')
            
            # 处理每一行
            processed_lines = []
            for line in lines:
                # 移除多余空白字符
                line = self.whitespace_pattern.sub(' ', line).strip()
                
                # 跳过页码和空行
                if self.page_number_pattern.match(line) or self.empty_line_pattern.match(line):
                    continue
                
                if line:
                    processed_lines.append(line)
            
            # 重新组合文本
            formatted_text = '\n'.join(processed_lines)
            
            logger.info("文本格式化完成")
            return formatted_text
            
        except Exception as e:
            logger.error(f"文本格式化失败: {e}")
            return text
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """
        将文本分割成段落
        
        Args:
            text: 格式化后的文本
            
        Returns:
            List[str]: 段落列表
        """
        # 使用空行分割段落
        paragraphs = re.split(r'\n\s*\n', text)
        
        # 过滤空段落
        return [p.strip() for p in paragraphs if p.strip()]
    
    def clean_text(self, text: str) -> str:
        """
        清理文本中的特殊字符和格式
        
        Args:
            text: 原始文本
            
        Returns:
            str: 清理后的文本
        """
        # 移除特殊字符
        text = re.sub(r'[^\w\s.,;:!?()\-\'"]', '', text)
        
        # 标准化引号
        text = text.replace('"', '"').replace('"', '"')
        
        return text 