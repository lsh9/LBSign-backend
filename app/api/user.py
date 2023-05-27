import requests
from flask import Blueprint, request, current_app

from app.query import QueryUser, QueryCourse, QueryUserSign
from app.utils import exception_handler

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/user/login', methods=["POST"])
@exception_handler
def login():
    data = request.get_json()
    js_code = data['code']
    # 从wx接口获取openid
    response = requests.get(
        f"https://api.weixin.qq.com/sns/jscode2session?appid={current_app.config['WX_APP_ID']}&secret={current_app.config['WX_APP_SECRET']}&js_code={js_code}&grant_type=authorization_code")
    openid = response.json()['openid']
    user = QueryUser.get_user(openid=openid)
    if user is None:
        user = QueryUser.add_user(openid=openid)
        course = {
            "courseName": "Default",
            "courseDescription": "默认签到归档",
            "userid": user["userid"]
        }
        course = QueryCourse.add_course(**course)
        QueryUser.set_user({
            "userid": user["userid"],
            "openid": openid,
            "defaultCourseId": course["courseId"]
        })
        user["defaultCourseId"] = course["courseId"]
    return {
        "success": True,
        "user": user
    }


@user_bp.route('/user/edit', methods=["POST"])
@exception_handler
def edit_user():
    data = request.get_json()
    return {
        "success": QueryUser.set_user(data)
    }


@user_bp.route('/user/get_my_courses', methods=["POST"])
@exception_handler
def get_my_courses():
    data = request.get_json()
    userid = data["userid"]
    courses = QueryCourse.get_courses_by_userid(userid=userid)
    return {
        "success": True,
        "courses": courses
    }


@user_bp.route('/user/get_my_signs', methods=["POST"])
@exception_handler
def get_my_signs():
    data = request.get_json()
    userid = data["userid"]
    userSigns = QueryUserSign.get_userSigns(userid=userid)
    return {
        "success": True,
        "userSigns": userSigns
    }
