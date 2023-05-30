import os.path

from flask import Blueprint, send_file, request, current_app

from app.utils import exception_handler

file_bp = Blueprint("file_bp", __name__)


@file_bp.route('/files/download/<filename>', methods=["GET"])
@exception_handler
def download_file(filename):
    try:
        # 返回文件给浏览器
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        return send_file(path, as_attachment=True)
    except FileNotFoundError as e:
        return {
            "msg": (e.filename + " not found").encode("utf-8").decode("latin-1")
        }


@file_bp.route('/files/upload', methods=["POST"])
@exception_handler
def upload_file():
    file = request.files.get("file")
    filename = file.filename
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    file.save(file_path)
    url = os.path.join("/data/", filename)
    return {
        "success": True,
        "url": url
    }
