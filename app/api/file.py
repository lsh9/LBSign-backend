import os.path

from flask import Blueprint, send_file

from app.utils import exception_handler

file_bp = Blueprint("file_bp", __name__)


@file_bp.route('/files/download/<filename>', methods=["GET"])
@exception_handler
def download_file(filename):
    try:
        # 返回文件给浏览器
        path = os.path.join("../files", filename + ".csv")
        return send_file(path, as_attachment=True)
    except FileNotFoundError as e:
        return {
            "msg": (e.filename + " not found").encode("utf-8").decode("latin-1")
        }
