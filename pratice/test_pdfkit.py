"""
    @author: magician
    @date: 2019/12/11
    @file: test_pdfkit.py
"""
import pdfkit


if __name__ == '__main__':
    url1 = 'baidu.com'
    pdfkit.from_string(url1, '../data/out.pdf')

