import os

from flask import Blueprint, request, current_app

from app.query import QueryCourse, QuerySign, QueryUserSign
from app.utils import exception_handler, md5

course_bp = Blueprint("course_bp", __name__)


@course_bp.route('/course/create', methods=["POST"])
@exception_handler
def create_course():
    data = request.get_json()
    course = QueryCourse.add_course(**data)
    return {
        "success": True,
        "courseId": course["courseId"]
    }


@course_bp.route('/course/edit', methods=["POST"])
@exception_handler
def edit_course():
    data = request.get_json()
    return {
        "success": QueryCourse.set_course(data)
    }


@course_bp.route('/course/delete', methods=["POST"])
@exception_handler
def delete_course():
    data = request.get_json()
    return {
        "success": QueryCourse.delete_course(data['courseId'])
    }


@course_bp.route('/course/get_course_signs', methods=["POST"])
@exception_handler
def get_course_signs():
    data = request.get_json()
    courseId = data['courseId']
    signs = QuerySign.get_signs_by_courseId(courseId)
    return {
        "success": True,
        "signs": signs
    }


@course_bp.route('/course/get_course_by_courseId', methods=["POST"])
@exception_handler
def get_course_by_courseId():
    data = request.get_json()
    courseId = data['courseId']
    course = QueryCourse.get_course_by_courseId(courseId)
    return {
        "success": True,
        "course": course
    }


@course_bp.route('/course/download_course_file', methods=["POST"])
@exception_handler
def download_course_file():
    data = request.get_json()
    courseId = data['courseId']
    signs = QuerySign.get_signs_by_courseId(courseId, count=False, desc=False)
    userSigns = {}
    records = dict()
    for sign in signs:
        signId = sign['signId']
        userSigns[signId] = QueryUserSign.get_userSigns(signId=signId)
        for user_sign in userSigns[signId]:
            userid = user_sign['userid']
            if userid not in records:
                records[userid] = {
                    "signUserName": user_sign['signUserName'],
                    "signUserNumber": user_sign['signUserNumber'],
                    "count": 1
                }
            else:
                records[userid]['count'] += 1
    # 统计所有学生的签到次数，写入文件
    filename = md5(str(courseId)) + '.csv'
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file = open(filepath, "w", encoding="utf-8")
    file.write(f"用户id,签到姓名,签到学号,签到次数\n")
    for userid in records:
        record = records[userid]
        file.write(f"{md5(str(userid))},{record['signUserName']},{record['signUserNumber']},{record['count']},\n")
    file.close()
    # 返回文件路径
    url = os.path.join("/data/", filename)
    return {
        "success": True,
        "url": url
    }


