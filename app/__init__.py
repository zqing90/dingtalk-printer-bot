from flask import Flask
from .config import Config

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

    return app