#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR 处理器测试脚本
"""

import os
import sys
from pathlib import Path
from PIL import Image
import fitz  # PyMuPDF
from ocr_processor import OCRProcessor

def convert_pdf_to_images(pdf_path: Path) -> list:
    """
    将 PDF 转换为图像列表
    
    Args:
        pdf_path: PDF 文件路径
        
    Returns:
        list: PIL Image 对象列表
    """
    images = []
    try:
        # 打开 PDF 文件
        doc = fitz.open(pdf_path)
        
        # 遍历每一页
        for page_num in range(len(doc)):
            # 获取页面
            page = doc[page_num]
            
            # 将页面转换为图像
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2倍分辨率
            
            # 转换为 PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
            
        doc.close()
        return images
    except Exception as e:
        print(f"PDF 转换失败: {e}")
        return []

def main():
    # 获取 PDF 文件路径
    pdf_path = Path("/Users/daiyi/Documents/Cursor/BGATranslatehelper/data/games/Propuh/rules/original.pdf")
    if not pdf_path.exists():
        print(f"错误：PDF 文件不存在: {pdf_path}")
        return
    
    try:
        # 将 PDF 转换为图像
        images = convert_pdf_to_images(pdf_path)
        if not images:
            print("PDF 转换失败")
            return
        
        print(f"成功加载 PDF 文件，共 {len(images)} 页")
        
        # 初始化 OCR 处理器
        processor = OCRProcessor()
        print("OCR 处理器初始化成功")
        
        # 处理每一页
        all_text = []
        for i, image in enumerate(images, 1):
            print(f"\n处理第 {i} 页...")
            text, image_descriptions = processor.process_image(image, page_number=i)
            
            if text is None:
                print(f"第 {i} 页 OCR 处理失败")
                continue
            
            all_text.append(text)
            
            if image_descriptions:
                print(f"\n第 {i} 页图像描述:")
                for desc in image_descriptions:
                    print(desc)
        
        # 保存所有结果到文件
        output_path = Path("data/games/Propuh/rules/extracted.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# 规则书文本\n\n")
            f.write("\n".join(all_text))
        print(f"\n结果已保存到: {output_path}")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")

if __name__ == "__main__":
    main() 