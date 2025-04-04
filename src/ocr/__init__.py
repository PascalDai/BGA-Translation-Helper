#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR 模块入口
提供统一的 OCR 处理接口
"""

from .pdf_processor import PDFProcessor
from .ocr_processor import OCRProcessor
from .text_formatter import TextFormatter

class OCRManager:
    """OCR 管理器类"""
    
    def __init__(self):
        """初始化 OCR 管理器"""
        self.pdf_processor = None
        self.ocr_processor = OCRProcessor()
        self.text_formatter = TextFormatter()
    
    def process_pdf(self, pdf_path: str) -> str:
        """
        处理 PDF 文件并提取文本
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            str: 提取并格式化后的文本
        """
        try:
            # 初始化 PDF 处理器
            self.pdf_processor = PDFProcessor(pdf_path)
            
            # 获取总页数
            total_pages = self.pdf_processor.get_page_count()
            
            # 处理每一页
            all_text = []
            for page_num in range(total_pages):
                # 尝试直接提取文本
                text = self.pdf_processor.extract_text(page_num)
                
                # 如果文本为空，尝试使用 OCR
                if not text.strip():
                    image = self.pdf_processor.extract_page_image(page_num)
                    if image:
                        text = self.ocr_processor.process_image(image)
                
                # 格式化文本
                if text:
                    formatted_text = self.text_formatter.format_text(text)
                    all_text.append(formatted_text)
            
            # 合并所有文本
            final_text = '\n\n'.join(all_text)
            
            # 清理文本
            final_text = self.text_formatter.clean_text(final_text)
            
            return final_text
            
        except Exception as e:
            raise Exception(f"PDF 处理失败: {e}")
