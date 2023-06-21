"""
# @author: magician
# @file:   pypdf_demo.py
# @date:   2023/6/21
"""
from pypdf import PdfReader, PdfWriter


def compress_pdf(input_path, output_path):

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for page in writer.pages:
        # ⚠️ This has to be done on the writer, not the reader!
        page.compress_content_streams()  # This is CPU intensive!

    writer.remove_images()

    with open(output_path, "wb") as f:
        writer.write(f)


if __name__ == '__main__':
    # 示例用法
    input_path = '/Users/magician/Projects/github/python3/data/9664100169510.pdf'  # 输入PDF文件路径
    output_path = '/Users/magician/Projects/github/python3/data/output.pdf'  # 压缩后的PDF文件路径
    compress_pdf(input_path, output_path)
