from flask import Blueprint, request

from app.query import QueryCourse, QuerySign
from app.utils import exception_handler

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
