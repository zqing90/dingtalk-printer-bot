
import os
from platform import platform
from app.models.result import CommonResult
from app.utils.printers.cups import print_file as print_file_cups
from app.utils.printers.win32 import print_file as print_file_windows


def print_file(file_path):
    # 判断文件是否存在
    if not os.path.exists(file_path):
        return CommonResult(False,f'打印文件Error：文件不存在，{file_path}')
    # 判断操作系统，是windows还是linux
    if platform.system() == 'Linux':
        return print_file_cups(file_path)
    else:
        return print_file_windows(file_path)
    
        