
import json
import os
from uuid import uuid4
import requests

from app.config import Config
from app.models.result import CommonResult

def download_save_file(file_download_url,file_path):
    # 下载文件
    response = requests.get(file_download_url)
    if response.status_code != 200:
        print(f"[Download File ERROR]: {response.text}")
        return CommonResult(status=False,message=f"[Download File ERROR]:{response.status_code}")

    if os.path.exists(file_path):
            os.remove(file_path)
    try:
        # 保存文件
        with open(file_path, 'wb') as f:
            f.write(response.content)
            print(f"File {file_download_url} saved")
        return CommonResult(status=True,data={'file_path':file_path})
    except Exception as e:
        return CommonResult(status=False,message=f"[Download File ERROR]: {e}")
    
def download_save_image(file_download_url,file_path_not_ext):
    # 下载文件
    response = requests.get(file_download_url)
    if response.status_code != 200:
        print(f"[Download File ERROR]: {response.text}")
        return CommonResult(status=False,message=f"[Download File ERROR]:{response.status_code}")
    # 获取文件头
    content_type = response.headers.get('Content-Type', '').lower()
    ext_name = '.jpg'
    if 'jpeg' in content_type or 'jpg' in content_type:
        ext_name = '.jpg'
    elif 'png' in content_type:
        ext_name = '.png'
    elif 'gif' in content_type:
        ext_name = '.gif'
    elif 'bmp' in content_type:
        ext_name =  '.bmp'
    else:
        return CommonResult(False,f"[Save Image Error]:未知的图片格式{content_type}")
    file_path =f'{file_path_not_ext}{ext_name}'
    if os.path.exists(file_path):
            os.remove(file_path)
    try:
        # 保存文件
        with open(file_path, 'wb') as f:
            f.write(response.content)
            print(f"File {file_download_url} saved")
        return CommonResult(status=True,data={'file_path':file_path})
    except Exception as e:
        return CommonResult(status=False,message=f"[Download File ERROR]: {e}")

class SimpleText():
    """钉钉文本消息
    """
    def __init__(self, content):
        self.content = content
    def get_message(self):
        return {
                "content": self.content
        }

class DingTak:
    app_key = ''
    app_secret = ''
    robot_code = ''
    def __init__(self,app_key=Config.DING_TALK['AppKey'],app_secret=Config.DING_TALK['AppSecret']):
        self.robot_code = self.app_key = app_key
        self.app_secret = app_secret
        
    def get_access_token(self,api_access_token_url=Config.DING_TALK['AccessTokenURL']):
        """获取钉钉access_token

        Returns:
            CommonResult: 返回结果
        """

        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "appKey": self.app_key,
            "appSecret": self.app_secret
        }

        response = requests.post(api_access_token_url, json=params, headers=headers)
    
        if response.status_code == 200:
            result = response.json()
            if result.get('accessToken'):
                return  CommonResult(status=True,data={'access_token':result['accessToken']})
            else:
                return CommonResult(status=False,message=f"Error: {result.get('message')}")
        else:
            print(f'[AccessToken Error]:{response.text}')
            return CommonResult(status=False,message=f"[AccessToken Error]:{response.status_code}")
        

    def get_file_download_url(self,download_code,api_file_download_url=Config.DING_TALK['DownloaFiledURL']):
        """获取钉钉下载文件链接

        Args:
            download_code (_type_): 下载代码
            api_download_url (_type_): 下载文件api地址

        Returns:
            CommonResult: _description_
        """
        # 获取access_token
        result = self.get_access_token()
        if result.status == False:
            return result
        access_token = result.data['access_token']

        headers = {
            "x-acs-dingtalk-access-token": access_token,
            "Content-Type": "application/json"
        }
        params = {
            "downloadCode": download_code,
            "robotCode":self.app_key
        }
        # 获取下载链接
        response = requests.post(api_file_download_url, headers=headers,json=params)
        if response.status_code == 200:
            result = response.json()
            print(response.headers)
            print(result)
            return CommonResult(status=True,data={'downloadUrl':result.get('downloadUrl')})
        else:
            print(f'[Download URL Error]:{response.text}')
            return CommonResult(status=False,message=f"[Download URL Error]: {response.status_code}")


    def download_save_file(self,file_download_url,file_path):
        return download_save_file(file_download_url,file_path)
    
    def download_save_image(self,file_download_url,file_folder):
        # 获取uuid作为名称
        uuid = str(uuid4())
        file_path_no_ext = os.path.join(file_folder,uuid)
        return download_save_image(file_download_url,file_path_no_ext)
        
    def send_dingtalk_message(self, user_ids,api_send_msg_url=Config.DING_TALK['SendMessageURL'], msg_key='sampleText',msg_param={"content": "xxxx"}):
        """钉钉机器人发送消息
        关联文档：https://open.dingtalk.com/document/orgapp/robot-message-types-and-data-format
        Args:
            api_send_msg_url (str): _description_
            access_token (str): _description_
            robot_code (str): _description_
            user_ids (array): _description_
            msg_key (str): sampleText-文本消息
            msg_param (dict): {"content": "xxxx"}-文本消息
        Returns:
            _type_: _description_
        """
        # 获取access_token
        result = self.get_access_token()
        if result.status == False:
            return result
        access_token = result.data['access_token']

        headers = {
            'x-acs-dingtalk-access-token': access_token,
            'Content-Type': 'application/json'
        }
        data = {
            "robotCode": self.robot_code,
            "userIds": user_ids,
            "msgKey": msg_key,
            "msgParam": json.dumps(msg_param)
        }
        response = requests.post(api_send_msg_url, headers=headers, json=data)
        
        
        if response.status_code == 200:
            print(f"发送消息成功:{data}")
            return CommonResult(status=True)
        else:
            print(f"发送消息失败: {response.text}")
            return CommonResult(status=False, message=f'[Seed Message Error]:{response.status_code}')
   