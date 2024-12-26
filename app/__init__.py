from flask import Flask
from .config import Config
import threading

g_cache= {}
g_cache_lock = threading.Lock()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 注册 Blueprint
    from app.blueprints.printers import printers
    app.register_blueprint(printers, url_prefix='/printer')

    from app.blueprints.dingtalk import ding
    app.register_blueprint(ding, url_prefix='/ding')

    from app.blueprints.home import home
    app.register_blueprint(home)

    from app.jobs.job_deletefiles import job_deletefiles
    app.register_blueprint(job_deletefiles)

    # 使用stream模式时，注册stream
    if Config.DING_TALK['Mode'] == 'stream':
        from app.utils.dingtalk.stream import initialize_dingtalk_stream
        initialize_dingtalk_stream()

    return app