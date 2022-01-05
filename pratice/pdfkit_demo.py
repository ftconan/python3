"""
    @author: magician
    @date: 2019/12/11
    @file: pdfkit_demo.py
"""
import os.path

import pdfkit


if __name__ == '__main__':
    url1 = 'baidu.com'
    pdfkit.from_string(url1, '../data/out.pdf')
    # with open('/Users/magician/Downloads/2h_全四册新概念英语笔记.pdf') as f:
    #     pdfkit.from_file('/Users/magician/Downloads/2h_全四册新概念英语笔记.pdf', '../data/out1.pdf')
