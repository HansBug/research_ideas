#!/usr/bin/env python3
"""
PDF文本提取工具
支持两种模式：
- text: 直接提取PDF中的文本内容（快速）
- ocr: 使用OCR识别PDF中的文字（适用于扫描件）
"""

import argparse
import sys
from pathlib import Path


def extract_text_mode(pdf_path: str, output_path: str):
    """使用文字方式提取PDF文本"""
    import PyPDF2

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = []

        for page_num, page in enumerate(pdf_reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                text_content.append(f"--- Page {page_num} ---\n{text}\n")

        full_text = '\n'.join(text_content)

        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(full_text)

        print(f"成功提取 {len(pdf_reader.pages)} 页内容到 {output_path}")


def extract_ocr_mode(pdf_path: str, output_path: str):
    """使用OCR方式提取PDF文本"""
    import pdf2image
    import pytesseract
    from PIL import Image

    # 将PDF转换为图片
    images = pdf2image.convert_from_path(pdf_path)
    text_content = []

    for page_num, image in enumerate(images, 1):
        # 使用OCR识别文字
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        if text.strip():
            text_content.append(f"--- Page {page_num} ---\n{text}\n")
        print(f"已处理第 {page_num}/{len(images)} 页")

    full_text = '\n'.join(text_content)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(full_text)

    print(f"成功提取 {len(images)} 页内容到 {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='从PDF文件中提取文本内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用文字模式提取
  python -m tools.pdf_extractor -i document.pdf -o output.txt -m text

  # 使用OCR模式提取（适用于扫描件）
  python -m tools.pdf_extractor -i scanned.pdf -o output.txt -m ocr
        """
    )

    parser.add_argument('-i', '--input', required=True, help='输入PDF文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出文本文件路径')
    parser.add_argument('-m', '--mode', choices=['text', 'ocr'], default='text',
                        help='提取模式: text=文字提取(快速), ocr=OCR识别(适用于扫描件)')

    args = parser.parse_args()

    # 检查输入文件是否存在
    if not Path(args.input).exists():
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 检查输入文件是否为PDF
    if not args.input.lower().endswith('.pdf'):
        print(f"警告: 输入文件可能不是PDF格式: {args.input}", file=sys.stderr)

    try:
        if args.mode == 'text':
            extract_text_mode(args.input, args.output)
        elif args.mode == 'ocr':
            extract_ocr_mode(args.input, args.output)
    except ImportError as e:
        print(f"错误: 缺少必要的依赖库。请运行: pip install -r requirements.txt", file=sys.stderr)
        print(f"详细错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
