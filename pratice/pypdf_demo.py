"""
# @author: magician
# @file:   pypdf_demo.py
# @date:   2023/6/21
"""


def compress_pdf(input_path, output_path):

    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for page in writer.pages:
        # ⚠️ This has to be done on the writer, not the reader!
        page.compress_content_streams()  # This is CPU intensive!

    # writer.remove_images()

    with open(output_path, "wb") as f:
        writer.write(f)


def pdf2img(input_path, output_path):
    """
    pdf2img
    """
    from pdf2image import convert_from_path, convert_from_bytes

    # 从文件路径转换
    # images = convert_from_path(input_path, size=(1654, 2339))
    images = convert_from_path(input_path)
    # images = convert_from_path(input_path, size=(800, 1080))
    # images = convert_from_path(input_path)

    # 或从字节流转换
    # with open('input.pdf', 'rb') as file:
    #     images = convert_from_bytes(file.read())

    # 保存图像
    for i, image in enumerate(images):
        image.save(f'{output_path}/{i}.jpg', 'JPEG')


def create_pdf(images, output_path):

    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(output_path, pagesize=letter)

    for image in images:
        c.drawImage(image, 0, 0, width=letter[0], height=letter[1])

        # 添加新页面
        c.showPage()

    c.save()


def traverse_folder(folder_path):
    import os

    image_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # 处理文件
            # print(file_path)  # 在这里替换为你要进行的操作
            image_paths.append(file_path)

    return image_paths


if __name__ == '__main__':
    # 示例用法
    # input_path = '/Users/magician/Projects/github/python3/data/180100170542.pdf'  # 输入PDF文件路径
    # output_path = '/Users/magician/Projects/github/python3/data/output1.pdf'  # 压缩后的PDF文件路径
    # compress_pdf(input_path, output_path)
    # #
    # pdf -> img
    # input_path = '/Users/magician/Projects/github/python3/data/高中英语语法专练292.pdf'  # 输入PDF文件路径
    # output_path1 = '/Users/magician/Projects/github/python3/data/pdfimg'
    # pdf2img(input_path, output_path1)
    #
    # 创建PDF
    # 遍历文件夹
    input_path1 = '/Users/magician/Projects/github/python3/data/pdfimg'
    output_path = '/Users/magician/Projects/github/python3/data/高中英语语法专练.pdf'
    image_paths1 = traverse_folder(input_path1)
    image_paths = sorted(image_paths1, key=lambda x: int(
        x.replace('/Users/magician/Projects/github/python3/data/pdfimg/', '').replace('.jpg', '')))
    create_pdf(image_paths, output_path)
