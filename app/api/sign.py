import os
import time

from flask import Blueprint, request, current_app

from app.query import QuerySign, QueryUserSign
from app.utils import exception_handler, md5

sign_bp = Blueprint("sign_bp", __name__)


@sign_bp.route('/sign/create', methods=["POST"])
@exception_handler
def create_sign():
    data = request.get_json()
    signCode = QuerySign.get_valid_signCode()
    data['signCode'] = signCode
    sign = QuerySign.add_sign(**data)
    return {
        "success": True,
        "sign": sign,
    }


@sign_bp.route('/sign/edit', methods=["POST"])
@exception_handler
def edit_sign():
    data = request.get_json()
    return {
        "success": QuerySign.set_sign(data)
    }


@sign_bp.route('/sign/get_sign_by_signCode', methods=["POST"])
@exception_handler
def get_sign_by_signCode():
    data = request.get_json()
    signCode = data['signCode']
    sign = QuerySign.get_sign_by_signCode(signCode)
    return {
        "success": True,
        "sign": sign
    }


@sign_bp.route('/sign/participate', methods=["POST"])
@exception_handler
def participate_sign():
    data = request.get_json()
    # 检查是否已经签到
    userSign = QueryUserSign.get_userSign_by_signId_and_userid(data['signId'], data['userid'])
    if userSign is not None:
        # 更新签到信息
        data['userSignId'] = userSign['userSignId']
        QueryUserSign.set_userSign(data)
    else:
        QueryUserSign.add_userSign(**data)
    sign = QuerySign.get_sign_by_signId(data['signId'])
    return {
        "success": True,
        "sign": sign
    }


@sign_bp.route('/sign/modify_userSign', methods=["POST"])
@exception_handler
def modify_userSign():
    data = request.get_json()
    sign = QueryUserSign.set_userSign(data)
    return {
        "success": True,
    }


# 删除签到
@sign_bp.route('/sign/delete', methods=["POST"])
@exception_handler
def delete_sign():
    data = request.get_json()
    return {
        "success": QuerySign.delete_sign(data['signId'])
    }


# 下载签到文件
@sign_bp.route('/sign/download_sign_file', methods=["POST"])
@exception_handler
def download_sign_file():
    data = request.get_json()
    userid = data['userid']
    signId = data['signId']
    user_signs = QueryUserSign.get_userSigns(signId=signId)
    # 根据用户Id和签到Id生成加密文件名
    filename = md5(str(userid) + " " + str(signId)) + '.csv'
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file = open(filepath, "w", encoding="utf-8")
    file.write(f"用户id,签到姓名,签到学号,签到时间\n")
    for user_sign in user_signs:
        signTime = int(user_sign['signTimeStamps'])
        # 将时间戳转时间
        signTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(signTime))
        file.write(f"{md5(str(user_sign['userid']))},{user_sign['signUserName']},{user_sign['signUserNumber']},{signTime},\n")
    file.close()
    # 返回文件路径
    url = os.path.join("/data/", filename)
    return {
        "success": True,
        "url": url
    }
