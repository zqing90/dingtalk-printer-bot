import os
from app.models.result import CommonResult
from app.config import Config
from app.utils.dingtalk.http import DingTak, SimpleText
from app.utils.files.txt import TXTFile
from app.utils.libreoffice.libreoffice import ConvertFile, FileType
from app.utils.printers.cups import print_file


class DingTalkMessage:
    data = None
    root_path = ''
    cache = None
    def __init__(self, data,root_path,cache):
        self.data = data
        self.root_path = root_path
        self.cache = cache
    def handle_dingtalk_message(self):
        """处理钉钉消息

        Args:
            data (dict): 钉钉消数据

        Returns:
            _type_: result
        """
        print(self.data)
        # 检查是否包含错误信息
        if 'errorMessage' in self.data:
            error_code = self.data.get('errorCode')
            error_message = self.data.get('errorMessage')
            print(f"Error {error_code}: {error_message}")
            result = CommonResult(status=False,message=f"Error {error_code}: {error_message}")
            return result

        # 解析消息类型
        msg_type = self.data.get('msgtype')
        # 发送人
        sender_staff_id = self.data.get('senderStaffId')
        # 根据消息类型调用相应的处理函数
        if msg_type == 'text':
            result = self.handle_text_message(sender_staff_id)
        elif msg_type == 'picture':
            result = self.handle_picture_message()
        elif msg_type == 'file':
            result = self.handle_file_message()
        else:
            result = CommonResult(status=False,message=result)
        
        dt = DingTak()
        msg = SimpleText(result.message)
        dt.send_dingtalk_message(user_ids=[sender_staff_id],msg_param=msg.get_message())
        return result

    def handle_text_message(self,sender_staff_id):
        """文本消息处理函数

        Args:
            data (dict): data

        Returns:
            _type_: _description_
        """
        content = self.data['text']['content']
        print(f"Received text message: {content}")
        file_path = os.path.join(self.root_path, 'outputs',f'{sender_staff_id}.txt')
        txt_file = TXTFile(file_path)
        output_folder = os.path.join(self.root_path, 'outputs')

        # 仅文本打印模式使用
        font_path = os.path.join(self.root_path,'fonts',Config.FONT['font_path'])
        font_size = Config.FONT['font_size']
        font_name = Config.FONT['font_name']

        # 启动连续输入模式
        if content == '+++':
            # 清空文档内容
            if os.path.exists(file_path):
                os.remove(file_path)
            self.cache.set_cache_key(sender_staff_id, True)
            return CommonResult(status=True,message="启动连续输入模式！\n1、结束并打印：###\n2、取消：---")
        
        # 结束并打印文件
        if content == '###':
            self.cache.set_cache_key(sender_staff_id, False)
            
            # 判断文件类型
            file = ConvertFile(output_folder=output_folder,input_file_path=file_path)
            file.set_font(font_name=font_name,font_path=font_path,font_size=font_size)
            result = file.convert_to_pdf(FileType.TXT)
            if result.status == False:
                result.message = f"[连续输入模式ERROR]:{result.message}"
                return result
            
            output_file_path = result.data['file_path']
            result = print_file(output_file_path)
            result.message = f"[连续输入模式]完成。\n{result.message}"
            return result
        
        # 取消
        if content == '---':
            self.cache.set_cache_key(sender_staff_id, False)
            # 删除文件
            if os.path.exists(file_path):
                os.remove(file_path)
            return CommonResult(status=True,message="[连续输入模式]取消成功！")
        
        txt_mode = self.cache.get_cache_key(sender_staff_id)
        if txt_mode is None:
            txt_mode = False

        # 连续模式输入
        if txt_mode == True:
            result = txt_file.write_text_append(content)
            if result == False:
                result.message = f'[连续输入模式ERROR]:{result.message}'
                return result
            result.message = f'[连续输入模式]:接受信息成功，请继续输入。\n1、结束并打印：###\n2、取消打印：---'
            return result
        
        # 普通模式输入
        result =  txt_file.write_text_overwite(content)
        if result == False:
            result.message = f'[普通模式ERROR]:{result.message}'
            return result
        
        # 判断文件类型
        file = ConvertFile(output_folder=output_folder,input_file_path=file_path)
        file.set_font(font_name=font_name,font_path=font_path,font_size=font_size)
        result = file.convert_to_pdf(FileType.TXT)
        if result.status == False:
            result.message = f'[普通模式ERROR]:{result.message}'
            return result
        
        output_file_path = result.data['file_path']
        result = print_file(output_file_path)
        result.message = f'[普通输入模式]:完成。\n{result.message}\nTips：多文本可使用连续输入模式\n开启指令：+++'
        # result = CommonResult(True,"handle_text_message OK")
        return result

    def handle_picture_message(self):
        download_code = self.data['content']['downloadCode']
        dt = DingTak()
        
        # 获取文件临时下载链接
        result = dt.get_file_download_url(download_code)
        if result.status == False:
            return result
        download_url = result.data['downloadUrl']
        output_folder = os.path.join(self.root_path, 'uploads')
        # 下载并保存文件
        result = dt.download_save_image(download_url,output_folder)
        if result.status == False:
            return result
        file_path = result.data['file_path']

        result = print_file(file_path)
        # result = CommonResult(True,"handle_picture_message OK")
        return result


    def handle_file_message(self):
        """文件消息处理函数

        Args:
            data (dict): data

        Returns:
            CommonResult: _description_
        """
        download_code = self.data['content']['downloadCode']
        file_name = self.data['content']['fileName']
        file_path = os.path.join(self.root_path, 'uploads', file_name)

        dt = DingTak()
        
        # 获取文件临时下载链接
        result = dt.get_file_download_url(download_code)
        if result.status == False:
            return result
        download_url = result.data['downloadUrl']
        
        # 下载并保存文件
        result = dt.download_save_file(download_url,file_path)
        if result.status == False:
            return result
        
        output_folder = os.path.join(self.root_path, 'outputs')
        # 判断文件类型
        file = ConvertFile(output_folder=output_folder,input_file_path=file_path)
        file_type = file.get_file_type()
        if file_type == FileType.Other:
            return CommonResult(False,"file type is not supported")
        
        # 转换文件
        result = file.convert_to_pdf(file_type)
        if result.status == False:
            return result
        output_file_path = result.data['file_path']

        result = print_file(output_file_path)
        # result = CommonResult(True,"handle_file_message OK")
        return result
