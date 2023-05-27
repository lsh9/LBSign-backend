from dataclasses import asdict

from app.database import db
from app.database.models import UserSign


class QueryUserSign:
    @staticmethod
    def get_userSigns(**kwargs):
        instances = db.session.query(UserSign).filter_by(**kwargs).all()
        instances_dict = [asdict(instance) for instance in instances]
        for i, instance in enumerate(instances):
            sign = instance.sign
            course = sign.course
            instances_dict[i]['sign'] = asdict(sign)
            instances_dict[i]['sign']['course'] = asdict(course)
        return instances_dict

    @staticmethod
    def add_userSign(**kwargs):
        userSign = UserSign(**kwargs)
        db.session.add(userSign)
        db.session.commit()
        return userSign

    @staticmethod
    def set_userSign(data):
        affected_rows = db.session.query(UserSign).filter_by(userSignId=data["userSignId"]).update(data)
        db.session.commit()
        return affected_rows != 0

    @staticmethod
    def get_userSign_by_signId_and_userid(signId, userid):
        userSign = db.session.query(UserSign).filter_by(signId=signId, userid=userid).first()
        return asdict(userSign) if userSign else None

    @staticmethod
    def get_sign_count_by_signId(signId):
        count = db.session.query(UserSign).filter_by(signId=signId).count()
        return count
