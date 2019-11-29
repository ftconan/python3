"""
    @author: magician
    @date: 2019/11/29
    @file: test_xhtml2pdf.py
"""
import os

from xhtml2pdf import pisa
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xhtml2pdf.default import DEFAULT_FONT

from static import static_dir

pdfmetrics.registerFont(TTFont('yh', os.path.join(static_dir, "微软雅黑.ttf")))
DEFAULT_FONT['helvetica'] = 'yh'


def convert_html2pdf(html, output_path):
    """
    html -> pdf
    :param html:    html path
    :param output_path:  output path
    :return:
    """
    # open output file for writing (truncated binary)
    with open(output_path, "wb+") as output_file:
        # convert HTML to PDF
        with open(html, 'rb') as html_file:
            pisa_status = pisa.CreatePDF(html_file.read(), dest=output_file, encoding='utf-8')

    # return True on success and False on errors
    return pisa_status.err


if __name__ == '__main__':
    base_path = '/home/magician/Project/python3/data'
    html_path = base_path + '/test.html'
    out_path = base_path + '/test.pdf'

    convert_html2pdf(html_path, out_path)
