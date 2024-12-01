from enum import Enum
import os
import shutil
import subprocess

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

    def __init__(self, output_folder,input_file_path):
        self.output_folder = output_folder
        self.input_file_path = input_file_path
        self.input_file = os.path.basename(input_file_path)
        self.input_file_base_name = os.path.splitext(self.input_file)[0]
        self.input_file_ext_name = os.path.splitext(self.input_file)[1]
    
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
        # 构建命令
        command = [
            'libreoffice', '--headless', '--convert-to', 'pdf:writer_pdf_Export', '--outdir', self.output_folder, self.input_file_path
        ]
        # 执行命令
        try:
            # 判断文件是否存在，存在则先删除文件
            if os.path.exists(self.output_file_path):
                os.remove(self.output_file_path)

            result = subprocess.run(command, check=True)
            print(f"转换成功: {self.input_file_path} -> { self.output_file_path}")
            return CommonResult(True,"转换成功",data={"file_path":self.output_file_path} )
            
        except Exception as e:
            print(e)
            return CommonResult(False, f"转换失败,错误原因: {e}")