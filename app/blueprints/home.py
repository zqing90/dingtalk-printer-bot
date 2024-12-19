import os
from flask import Blueprint, current_app, jsonify, render_template, request as flask_request, send_from_directory
from app.config import Config
home= Blueprint('home', __name__)


@home.route('/static/<path:filename>')
def blueprint_static(filename):
    return send_from_directory(os.path.join(current_app.root_path,'static'), filename)
@home.route('/', methods=['GET'])
def index():
    printer = Config.PRINTER
    cups = Config.CUPS
    ding =Config.DING_TALK
    font = Config.FONT
    return render_template('index.html',printer = printer,cups=cups,ding=ding,font=font )