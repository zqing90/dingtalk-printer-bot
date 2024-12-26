from flask import Blueprint, current_app, jsonify, request as flask_request
from app import g_cache,g_cache_lock
from app.utils.cache import Cache
from app.utils.dingtalk.message import DingTalkMessage

ding = Blueprint('dingtalk', __name__)




@ding.route('/get-bot-msg', methods=['POST'])
def get_bot_msg():
    # 获取POST请求中的JSON数据
    data = flask_request.json
    c =Cache(g_cache,g_cache_lock)
    root_path = root_path = current_app.root_path
    m = DingTalkMessage(data,root_path,c)
    result = m.handle_dingtalk_message()
    return jsonify(result.to_http_result().to_dict())



# @ding.route('/test', methods=['GET'])
# def test():
#     file_path = os.path.join(current_app.root_path, 'outputs', '1153490705886239.txt')
#     output_folder = os.path.join(current_app.root_path, 'outputs')

#     font_path = os.path.join(current_app.root_path,'fonts',Config.FONT['font_path'])
#     font_size = Config.FONT['font_size']
#     font_name = Config.FONT['font_name']
#     # 判断文件类型
#     file = ConvertFile(output_folder=output_folder,input_file_path=file_path)
#     file.set_font(font_name=font_name,font_path=font_path,font_size=font_size)
#     result = file.convert_to_pdf(FileType.TXT)
#     return jsonify(result.to_http_result().to_dict())
    

    
  

