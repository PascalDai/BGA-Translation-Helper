#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF 处理模块
负责 PDF 文件的读取和预处理
"""

import logging
from pathlib import Path
from typing import List, Optional
import PyPDF2
from PIL import Image
import io

logger = logging.getLogger(__name__)

class PDFProcessor:
    """PDF 文件处理类"""
    
    def __init__(self, pdf_path: str):
        """
        初始化 PDF 处理器
        
        Args:
            pdf_path: PDF 文件路径
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")
        
        self.pdf_reader = None
        self._load_pdf()
    
    def _load_pdf(self):
        """加载 PDF 文件"""
        try:
            self.pdf_reader = PyPDF2.PdfReader(str(self.pdf_path))
            logger.info(f"成功加载 PDF 文件: {self.pdf_path}")
        except Exception as e:
            logger.error(f"加载 PDF 文件失败: {e}")
            raise
    
    def get_page_count(self) -> int:
        """
        获取 PDF 页数
        
        Returns:
            int: PDF 页数
        """
        return len(self.pdf_reader.pages)
    
    def extract_page_image(self, page_num: int) -> Optional[Image.Image]:
        """
        提取指定页面的图像
        
        Args:
            page_num: 页码（从0开始）
            
        Returns:
            Optional[Image.Image]: 页面图像，如果提取失败则返回 None
        """
        try:
            page = self.pdf_reader.pages[page_num]
            xObject = page['/Resources']['/XObject'].get_object()
            
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    data = xObject[obj].get_data()
                    return Image.open(io.BytesIO(data))
            
            logger.warning(f"页面 {page_num} 未找到图像")
            return None
            
        except Exception as e:
            logger.error(f"提取页面 {page_num} 图像失败: {e}")
            return None
    
    def extract_text(self, page_num: int) -> str:
        """
        提取指定页面的文本
        
        Args:
            page_num: 页码（从0开始）
            
        Returns:
            str: 页面文本
        """
        try:
            page = self.pdf_reader.pages[page_num]
            text = page.extract_text()
            logger.info(f"成功提取页面 {page_num} 文本")
            return text
        except Exception as e:
            logger.error(f"提取页面 {page_num} 文本失败: {e}")
            return "" 