import os
from flask import Blueprint, current_app, jsonify, render_template, request
from app.config import Config
from app.models.result import HTTPResult
from app.utils.printers.printer import print_file
from app.utils.libreoffice.libreoffice import ConvertFile, FileType
printers = Blueprint('printer', __name__)


@printers.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'success':False,'msg': 'No file part'}), 
        
        file = request.files['file']
        if file:
            filename = file.filename
            if filename == '':
                http_result = HTTPResult(False,'文件未选择')
                return jsonify(http_result.to_dict())

            file_path = os.path.join(current_app.root_path, 'uploads', filename)
            try:
                # 判断文件是否存在，存在则删除
                if os.path.exists(file_path):
                    os.remove(file_path)
                file.save(file_path)
                http_result = HTTPResult(True,'文件上传成功')
                return jsonify(http_result.to_dict())
            except Exception as e:
                print(e)
                return jsonify(HTTPResult(False,'文件上传失败').to_dict())
        else:
            return jsonify(HTTPResult(False,'文件未选择').to_dict())



@printers.route('/convert/<filename>', methods=['GET'])
def convert_file(filename):
    # 判断filename参数
    if not filename:
        return jsonify(HTTPResult(False,'filename参数未传').to_dict())

    
    file_path = os.path.join(current_app.root_path, 'uploads',filename)
    # 判断文件是否存在
    if not os.path.exists(file_path):
        return jsonify(HTTPResult(False,'文件不存在').to_dict())

    output_folder = os.path.join(current_app.root_path,'outputs')
    file = ConvertFile(output_folder,file_path)
    # 判断类型
    file_type = file.get_file_type()
    if file_type == FileType.Other:
        return jsonify(HTTPResult(False,"文件类型不支持").to_dict())
    # 转换文件
    result = file.convert_to_pdf(file_type).to_http_result()
    return jsonify(result.to_dict())
@printers.route('/list_upload_files', methods=['GET'])
def list_upload_files():
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    files = os.listdir(upload_folder)
    return files

@printers.route('/list_convert_files', methods=['GET'])
def list_convert_files():
    convert_folder = os.path.join(current_app.root_path,'outputs')
    files = os.listdir(convert_folder)
    return files

@printers.route('/delete_upload_files', methods=['GET'])
def delete_upload_files():
    try:
        upload_folder = os.path.join(current_app.root_path, 'uploads')
        files = os.listdir(upload_folder)
        for file in files:
            file_path = os.path.join(upload_folder, file)
            os.remove(file_path)
        return jsonify(HTTPResult(success=True,message="delete success").to_dict())
    except Exception as e:
        print(e)
        return jsonify(HTTPResult(success=False,message=str(e)).to_dict())
    
@printers.route('/delete_convert_files', methods=['GET'])
def delete_convert_files():
    try:
        upload_folder = os.path.join(current_app.root_path, 'outputs')
        files = os.listdir(upload_folder)
        for file in files:
            file_path = os.path.join(upload_folder, file)
            os.remove(file_path)
        return jsonify(HTTPResult(success=True,message="delete success").to_dict())
    except Exception as e:
        print(str(e))
        return jsonify(HTTPResult(success=False,message=str(e)).to_dict())
    

@printers.route('/printfile/<filename>', methods=['GET'])
def printfile(filename):
    # 判断filename参数
    if not filename:
        return jsonify(HTTPResult(success=False,message="filename is empty").to_dict())
    
    file_path = os.path.join(current_app.root_path, 'outputs',filename)
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return jsonify(HTTPResult(success=False,message="file not found").to_dict())

    
    printer = Config.PRINTER
    results = print_file(file_path,printer_name=printer["name"],print_options=printer["options"])
    return jsonify(results.tohttp_result().to_dict())   
    