from enum import Enum
import os
import shutil
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from app.models.result import CommonResult

class FileType(Enum):
    Office = 1
    PDF = 2
    TXT = 3
    PICUTRE = 4
    Other = 0

class ConvertFile:
    
    input_file_path = ''
    input_file = ''

    input_file_ext_name = ''
    input_file_base_name = ''

    output_file = ''
    output_folder = ''
    output_file_path = ''
    font_size = 14
    font_name = 'Helvetica'
    font_path = ''

    def __init__(self, output_folder,input_file_path):
        self.output_folder = output_folder
        self.input_file_path = input_file_path
        self.input_file = os.path.basename(input_file_path)
        self.input_file_base_name = os.path.splitext(self.input_file)[0]
        self.input_file_ext_name = os.path.splitext(self.input_file)[1]
    
    def set_font(self,font_name,font_path,font_size=14):
        self.font_name = font_name
        self.font_path = font_path
        self.font_size = font_size
        

    def get_file_type(self):
        """获取文件类型

        Returns:
            FileType: 文件类型
        """
        # 文件类型支持 PPT、Word Excel txt pdf
        if self.input_file_ext_name.lower() in ['.ppt','.pptx', '.doc','.docx', '.xls','.xlsx']:
            return FileType.Office
        elif self.input_file_ext_name.lower() in ['.txt']:
            return FileType.TXT
        elif self.input_file_ext_name.lower() in ['.pdf']:
            return FileType.PDF
        elif self.input_file_ext_name.lower() in ['.jpg','.jpeg','.png','.bmp']:
            return FileType.PICUTRE
        else:
            return FileType.Other



    def convert_to_pdf(self,filetype):
        """转换文件到pdf

        Args:
            filetype (FileType): 文件类型

        Returns:
            CommonResult: _description_
        """
        if filetype == FileType.Other: 
            return CommonResult(False, "不支持的文件类型")
       
        # if filetype == FileType.PDF or filetype == FileType.TXT or filetype == FileType.PICUTRE:
        if filetype == FileType.PDF or filetype == FileType.PICUTRE:
            try:
                self.output_file_path = os.path.join(self.output_folder, self.input_file)
                # 判断文件是否存在，存在则先删除文件
                if os.path.exists(self.output_file_path):
                    os.remove(self.output_file_path)
                # 复制文件
                shutil.copy(self.input_file_path, self.output_file_path)
                return CommonResult(True, "无需转换，复制到目标文件夹成功",data={'file_path':self.output_file_path})
            except Exception as e:
                print(e)
                return CommonResult(False, f"转换失败,错误原因: {e}")

        
        # 获取文件名和扩展名
        base_name = os.path.splitext(os.path.basename(self.input_file_path))[0]
        self.output_file = f"{base_name}.pdf"
        self.output_file_path = os.path.join(self.output_folder, self.output_file)

        try:
             # 判断文件是否存在，存在则先删除文件
            if os.path.exists(self.output_file_path):
                os.remove(self.output_file_path)
        except Exception as e:
            print(e)
            return CommonResult(False, f"转换失败,错误原因: {e}")
        
        if filetype == FileType.Office:
            return self.convert_office_to_pdf()
        elif filetype == FileType.TXT:
            return self.convert_txt_to_pdf()
        
    def convert_office_to_pdf(self):
        # 构建命令
        command = [
            'libreoffice', '--headless', '--convert-to', 'pdf:writer_pdf_Export', '--outdir', self.output_folder, self.input_file_path
        ]
        # 执行命令
        try:
            result = subprocess.run(command, check=True)
            print(f"转换成功: {self.input_file_path} -> { self.output_file_path}")
            return CommonResult(True,"转换成功",data={"file_path":self.output_file_path} )
            
        except Exception as e:
            print(e)
            return CommonResult(False, f"转换失败,错误原因: {e}")

    def convert_txt_to_pdf(self):
        try:
            # 注册中文字体
            if self.font_path != "":
                pdfmetrics.registerFont(TTFont(self.font_name, self.font_path))

            # 设置文档模板和样式
            doc = SimpleDocTemplate(self.output_file_path, pagesize=A4,
                                    rightMargin=inch/2, leftMargin=inch/2,
                                    topMargin=inch, bottomMargin=inch)

            # 定义段落样式
            style = ParagraphStyle(
                name='Normal',
                fontName=self.font_name,
                fontSize=self.font_size,
                leading=self.font_size * 1.3,  # 行距，通常为字体大小的1.2-1.5倍
                spaceBefore=6,  # 段前间距
                spaceAfter=6,   # 段后间距
            )

            # 准备故事板
            story = []

            with open(self.input_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    p = Paragraph(line.strip(), style)
                    story.append(p)

            # 构建PDF文档
            doc.build(story)

            return CommonResult(True, "转换成功", data={"file_path": self.output_file_path})
        except Exception as e:
            print(e)
            return CommonResult(False, f"转换失败,错误原因: {e}")