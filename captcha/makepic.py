# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 12:34
# @Author  : jiangcheng
# @Email   : jiangcheng@ict.ac.cn
# @File    : makepic.py
# @Software: PyCharm
# /**
# 功能:    
# 特殊函数: 
#
# */
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pathlib
from random import sample


class MakePicture(object):
    def __init__(self, size=(120, 35), number=4, line_number=(1, 4), point_number=(30, 40),
                 font_type_path=r'E:\pythonwork\newspider\captcha\fonts',
                 pic_path=r"./"):
        # 字体路径列表
        self.fontlists = list(pathlib.Path(font_type_path).glob('*.TTF'))
        # 生成图片路径
        self.pic_path = pic_path
        # 验证码位数
        self.number = number
        # 验证码图片大小
        if size:
            assert type(size) == tuple, 'size必须是一个表示图片大小的元祖，不能是%s' % (type(size))
            self.size = size
            self.width = size[0]
            self.height = size[1]

        # 加入干扰线条数范围
        if line_number:
            assert type(line_number) == tuple or int, 'line_number必须是一个数字或者表示范围的元祖，不能是%s' % (type(line_number))
            self.line_number = line_number
        else:
            self.line_number = 0
        if point_number:
            assert type(point_number) == tuple or int, 'point_number必须是一个数字或者表示范围的元祖，不能是%s' % (type(point_number))
            self.point_number = point_number
        else:
            self.point_number = 0

    #  随机生成颜色
    @classmethod
    def gene_color(cls):
        return tuple(random.randint(0, 255) for _ in range(3))

    # 用来随机生成一个字符串
    def gene_text(self):
        source = list(string.letters + string.digits)
        return ''.join(random.sample(source, self.number))  # number是生成验证码的位数

    # 用来绘制干扰线
    def gene_line(self, draw, linecolor=None):
        if type(self.line_number) == tuple:
            line_count = random.randint(min(self.line_number), max(self.line_number) + 1)
        else:
            line_count = self.line_number
        for i in range(line_count):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=self.gene_color() if not linecolor else linecolor)

    def gene_point(self, draw, linecolor=None):
        if type(self.point_number) == tuple:
            point_number = random.randint(min(self.point_number), max(self.point_number) + 1)
        else:
            point_number = self.point_number
        # 画点
        for i in range(point_number):
            draw.point([random.randint(0, self.width), random.randint(0, self.height)],
                       fill=self.gene_color() if not linecolor else linecolor)
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.gene_color() if not linecolor else linecolor)

    # 生成验证码
    def gene_code(self, bgcolor=None, fontcolor=None):
        if not bgcolor:
            bgcolor = MakePicture.gene_color()

        width, height = self.size  # 宽和高
        image = Image.new('RGB', (width, height), bgcolor)  # 创建图片

        font_path = sample(self.fontlists, 1)  # 随机选择字体
        font = ImageFont.truetype(font_path[0].name, 25)  # 验证码的字体

        draw = ImageDraw.Draw(image)  # 创建画笔

        text = self.gene_text()  # 生成字符串
        font_width, font_height = font.getsize(text)
        for i, string in enumerate(text):
            draw.text(((width - 10) / self.number * i + 10, (height - font_height) / self.number), text=string,
                      font=font, fill=MakePicture.gene_color() if not fontcolor else fontcolor)  # 填充字符串
        # 增加噪声，包括点，线和形变
        self.gene_line(draw)
        self.gene_point(draw)

        y1 = round(random.uniform(-10.0 / self.width, 10.0 / self.width), 2)
        x2 = round(random.uniform(-5.0 / self.height, 5.0 / self.height), 2)
        c1 = round(random.uniform(-0.15, 0.15), 2)
        c2 = round(random.uniform(-0.15, -0.15), 2)
        image = image.transform((width + 20, height + 10), Image.AFFINE, (1, y1, c1, x2, 1, c2),
                                Image.BILINEAR)  # 创建扭曲,输出图像中的每一个像素（x，y），新值由输入图像的位置（x+y1y+c1, x2x+y+c2）
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
        image.save(self.pic_path + (text + '.png'))  # 保存验证码图片


a = MakePicture()
a.gene_code()
