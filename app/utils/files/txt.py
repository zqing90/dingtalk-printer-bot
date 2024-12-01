
import os

from app.models.result import CommonResult


class TXTFile:

    file_path = ''
    def __init__(self, file_path):
        self.file_path = file_path

    def write_text_append(self, text):
        try:
            # 判断文件是否存在，不存在则创建并写入
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    file.write(text)
            else:
                # 否则追加文本内容
                with open(self.file_path, 'a', encoding='utf-8') as file:
                    # 增加换行,3行
                    file.write('\n\n\n')
                    file.write(text)
            return CommonResult(status=True,message="写入成功")
        except Exception as e:
            return CommonResult(status=False,message=f"Error: {e}")
    
    def write_text_overwite(self,text):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            return CommonResult(status=True,message="写入成功")
        except Exception as e:
            return CommonResult(status=False,message=f"Error: {e}")
