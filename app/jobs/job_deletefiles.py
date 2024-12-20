import atexit
import os
from pathlib import Path
import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Blueprint

job_deletefiles = Blueprint('job_deletefiles', __name__)
def delete_files_min_modifytime(path,modify_time):
    files = os.listdir(path)
    # 找出文件最后修改时间 小于 last_modify_time的文件名
    for file in files:
        file_path = os.path.join(path,file)
        file_modify_time = os.path.getmtime(file_path)
        if file_modify_time < modify_time:
            #删除文件
            print(f'delete files{file_path}')
            os.remove(file_path)


def delete_files():
    print("start job : delete files")
    # 获取当前时间戳
    current_time = time.time()
    befor_7_day = current_time - 7 * 24 * 60 * 60
    root_path = Path(__file__).resolve().parent.parent
    outputs_path = os.path.join(root_path,'outputs')
    uploads_path = os.path.join(root_path,'uploads')

    # 删除转换文件&上传文件
    delete_files_min_modifytime(uploads_path,befor_7_day)
    delete_files_min_modifytime(outputs_path,befor_7_day)

scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_files,trigger='cron',hour=2,minute=0)
# scheduler.add_job(func=delete_files,trigger='interval',seconds=5)

scheduler.start()

# 注册一个函数来优雅地关闭调度器，当应用停止时调用
atexit.register(lambda: scheduler.shutdown())