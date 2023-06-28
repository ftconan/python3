"""
# @author: magician
# @file:   compress_image_demo.py
# @date:   2023/6/28
"""
from PIL import Image
import os


def compress_image(input_path, output_path, quality=95):
    """
    压缩图片，将输入路径的图片保存为指定质量的图片到输出路径
    :param input_path: 输入图片的路径
    :param output_path: 输出压缩图片的路径
    :param quality: 压缩质量（0-100），默认为 95
    """
    image = Image.open(input_path)
    image.save(output_path, optimize=True, quality=quality)


def compress_image1(input_path, output_path, max_size):
    """
    有损压缩图片，将输入路径的图片保存为指定大小以下的图片到输出路径
    :param input_path: 输入图片的路径
    :param output_path: 输出压缩图片的路径
    :param max_size: 最大允许的文件大小（字节数）
    """
    image = Image.open(input_path)

    # 获取原始图片的尺寸
    width, height = image.size

    # 根据指定的最大文件大小计算压缩质量
    quality = 95
    while os.path.isfile(output_path) and os.path.getsize(output_path) > max_size and quality > 10:
        image.save(output_path, optimize=True, quality=quality)
        quality -= 5

    # 调整尺寸
    image.thumbnail((width, height))

    # 保存压缩后的图片
    image.save(output_path, optimize=True, quality=quality)


if __name__ == '__main__':
    # 示例用法
    input_image_path = '/Users/magician/Projects/github/python3/data/pdfimg/0.jpg'  # 输入图片的路径
    output_image_path = '/Users/magician/Projects/github/python3/data/output.jpg'  # 输出压缩图片的路径
    output_image_path1 = '/Users/magician/Projects/github/python3/data/output1.jpg'  # 输出压缩图片的路径

    # 无损压缩图片
    compress_image(input_image_path, output_image_path, quality=60)
    # 有损压缩图片
    compress_image1(input_image_path, output_image_path1, max_size=500*500)
