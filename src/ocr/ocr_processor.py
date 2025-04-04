#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR 处理模块
负责使用 Mistral AI OCR API 进行文本识别
"""

import logging
import os
import base64
import time
import io
from pathlib import Path
from typing import Optional, Tuple, List
from PIL import Image
from mistralai import Mistral
from PIL import ImageEnhance
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

class OCRProcessor:
    """OCR 处理器类"""
    
    def __init__(self):
        """初始化 OCR 处理器"""
        try:
            # 获取 API 密钥
            api_key = os.getenv("MISTRAL_API_KEY")
            if not api_key:
                raise ValueError("未设置 MISTRAL_API_KEY 环境变量，请在 .env 文件中配置")
            
            # 初始化 Mistral 客户端
            self.client = Mistral(api_key=api_key)
            logger.info("OCR 处理器初始化完成")
            
            # 初始化请求计时器
            self.last_request_time = 0
            self.min_request_interval = 5.0  # 增加请求间隔到 5 秒
            
        except Exception as e:
            logger.error(f"OCR 处理器初始化失败: {e}")
            raise
    
    def process_image(self, image: Image.Image, page_number: int) -> Tuple[Optional[str], List[str]]:
        """
        处理图像并提取文本和图像信息
        
        Args:
            image: PIL Image 对象
            page_number: 页面编号
            
        Returns:
            Tuple[Optional[str], List[str]]: (提取的文本, 图像描述列表)
        """
        try:
            # 等待请求间隔
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            if time_since_last_request < self.min_request_interval:
                wait_time = self.min_request_interval - time_since_last_request
                logger.info(f"等待 {wait_time:.1f} 秒后继续处理...")
                time.sleep(wait_time)
            
            # 将图像转换为适合 OCR 的格式
            processed_image = self._preprocess_image(image)
            
            # 将图像保存到内存中的字节流
            img_byte_arr = io.BytesIO()
            processed_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # 将图像转换为 base64
            image_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            
            # 使用 Mistral OCR API 进行文本识别
            response = self.client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{image_base64}"
                },
                include_image_base64=True
            )
            
            # 更新请求时间
            self.last_request_time = time.time()
            
            # 提取文本和图像信息
            text = ""
            image_descriptions = []
            
            if response.pages:
                # 处理文本内容
                text = response.pages[0].markdown
                
                # 处理图像
                if hasattr(response.pages[0], 'images') and response.pages[0].images:
                    for img_idx, img in enumerate(response.pages[0].images):
                        # 为每个图像添加描述
                        img_desc = f"\n[图像 {page_number}-{img_idx + 1}]\n"
                        if hasattr(img, 'description') and img.description:
                            img_desc += f"描述: {img.description}\n"
                        image_descriptions.append(img_desc)
            
            # 格式化文本
            text = self._format_text(text, page_number, image_descriptions)
            
            logger.info(f"成功完成第 {page_number} 页 OCR 文本识别")
            return text, image_descriptions
            
        except Exception as e:
            logger.error(f"OCR 处理失败: {e}")
            return None, []
    
    def _format_text(self, text: str, page_number: int, image_descriptions: List[str]) -> str:
        """
        格式化提取的文本
        
        Args:
            text: 原始文本
            page_number: 页面编号
            image_descriptions: 图像描述列表
            
        Returns:
            str: 格式化后的文本
        """
        # 添加页面分隔符
        formatted_text = f"\n--- 第 {page_number} 页 ---\n\n"
        
        # 处理标题
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#'):
                # 保持标题格式
                formatted_text += line + '\n'
            elif line.strip() and not line.startswith(' '):
                # 处理普通段落
                formatted_text += line + '\n'
            elif line.strip():
                # 处理缩进内容（如列表项）
                formatted_text += '  ' + line.strip() + '\n'
        
        # 添加图像描述
        if image_descriptions:
            formatted_text += '\n' + '\n'.join(image_descriptions) + '\n'
        
        return formatted_text
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        图像预处理
        
        Args:
            image: 原始图像
            
        Returns:
            Image.Image: 预处理后的图像
        """
        # 转换为灰度图像
        if image.mode != 'L':
            image = image.convert('L')
        
        # 增强对比度
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)  # 增强对比度
        
        # 增强亮度
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.5)  # 增强亮度
        
        return image 