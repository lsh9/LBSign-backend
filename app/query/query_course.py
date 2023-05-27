from dataclasses import asdict

from app.database import db
from app.database.models import Course


class QueryCourse:
    @staticmethod
    def add_course(**kwargs):
        course = Course(**kwargs)
        db.session.add(course)
        db.session.commit()
        return asdict(course)

    @staticmethod
    def set_course(data):
        affected_rows = db.session.query(Course).filter_by(courseId=data['courseId']).update(data)
        db.session.commit()
        return affected_rows != 0

    @staticmethod
    def delete_course(courseId):
        affected_rows = db.session.query(Course).filter_by(courseId=courseId).delete()
        db.session.commit()
        return affected_rows != 0

    @staticmethod
    def get_courses_by_userid(userid):
        courses = db.session.query(Course).filter_by(userid=userid).all()
        return [asdict(course) for course in courses]

    @staticmethod
    def get_course_by_courseId(courseId):
        course = db.session.query(Course).filter_by(courseId=courseId).first()
        return asdict(course) if course else None
