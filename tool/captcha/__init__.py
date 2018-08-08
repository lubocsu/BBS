import random
import string
#Image：一个画布
#ImageDraw:一个画笔
#ImageFont:画笔的字体
from PIL import Image,ImageDraw,ImageFont

#Captcha验证码

class Captcha(object):
    #生成几位验证码
    number = 4
    #验证码图片的宽度和高度
    size = (100,30)
    #验证码字体大小
    fontsize = 25
    #加入干扰线的条数
    line_number = 2
    # 构建一个验证码源文件
    SOURCE = list(string.ascii_letters)
    for index in range(0,10):
        SOURCE.append(str(index))
    #随机生成颜色
    @classmethod
    def __gene_random_color(cls,start=0,end=255):
        random.seed()
        return (random.randint(start,end),random.randint(start,end),random.randint(start,end))

    #随机产生一个字体
    @classmethod
    def __gene_random_font(cls):
        fonts=[
            'cambriaz.ttf',
            'consola.ttf',
            # 'modern.fon',
            # 'smalle.fon'
        ]
        #随机从列表中取一个元素
        font = random.choice(fonts)
        return 'tool/captcha/'+font

    #随机生成一个字符串（包括英文和数字）
    @classmethod
    def gene_text(cls,number):
        #number是生成验证码的位数
        return ''.join(random.sample(cls.SOURCE,number))

    #生成干扰线
    @classmethod
    def __gene_line(cls,draw,width,height):
        begin = (random.randint(0,width),random.randint(0,height))
        end = (random.randint(0,width),random.randint(0,height))
        draw.line([begin,end],fill=cls.__gene_random_color(),width=2)

    #绘制干扰点
    @classmethod
    def __gene_points(cls,draw,point_chance,width,height):
        chance = min(100,max(0,int(point_chance))) #大小限制在[0,100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0,100)
                if tmp > 100 - chance:
                    draw.point((w,h),fill=cls.__gene_random_color())

    #生成验证码
    @classmethod
    def gene_captcha(cls):
        #验证码图片的宽和高
        width,height = cls.size
        #创建图片(画板)
        image = Image.new('RGBA',(width,height),cls.__gene_random_color(0,100))
        #验证码的字体
        font = ImageFont.truetype(cls.__gene_random_font(),cls.fontsize)
        #创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串
        text = cls.gene_text(cls.number)
        #获取字体的尺寸
        font_width,font_height = font.getsize(text)
        #填充字符串
        draw.text(((width - font_width) / 2,(height - font_height) / 2),text,font=font,fill=cls.__gene_random_color(150,255))
        #绘制干扰线
        for x in range(0,cls.line_number):
            cls.__gene_line(draw,width,height)
        #绘制噪点
        cls.__gene_points(draw,10,width,height)
        # with open('captcha.png','wb') as fp:
        #     image.save(fp)
        return (image,text)