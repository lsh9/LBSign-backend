from dataclasses import asdict

from app.database import db
from app.database.models import UserSign, Sign, Course


class Query:
    @staticmethod
    def query_Sign_by_signId(signId):
        return db.session.query(Sign).filter_by(signId=signId).first()

    @staticmethod
    def query_Course_by_courseId(courseId):
        return db.session.query(Course).filter_by(courseId=courseId).first()

    @staticmethod
    def query_Sign_by_courseId(courseId):
        pass

    @staticmethod
    def query_userSign_by_signId(signId):
        return db.session.query(UserSign).filter_by(signId=signId).all()
