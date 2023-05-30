import time
from dataclasses import asdict

from app.database import db
from app.database.models import Sign
from app.query.query_user_sign import QueryUserSign
from app.utils import generate_random_string


class QuerySign:
    @staticmethod
    def get_valid_signCode():
        signCode = generate_random_string()  # 生成4位随机签到码
        while not QuerySign.is_free_signCode(signCode):
            signCode = generate_random_string()
        return signCode

    @staticmethod
    def is_free_signCode(signCode):
        """ 判断signCode是否可用，不存在或者到期为可用 """
        oldest_sign = QuerySign._get_latest_sign(signCode=signCode)
        if oldest_sign is None or oldest_sign.endTimeStamps < time.time():
            # signCode不存在或者可用（即已到期）
            return True
        return False

    @staticmethod
    def add_sign(**kwargs):
        sign = Sign(**kwargs)
        db.session.add(sign)
        db.session.commit()
        sign_dict = asdict(sign)
        sign_dict['course'] = asdict(sign.course)
        return sign_dict

    @staticmethod
    def set_sign(data):
        affected_rows = db.session.query(Sign).filter_by(signId=data['signId']).update(data)
        db.session.commit()
        return affected_rows != 0

    @staticmethod
    def get_sign_by_signCode(signCode):
        if QuerySign.is_free_signCode(signCode):
            print("signCode不存在或者已到期")
            return None
        sign = QuerySign._get_latest_sign(signCode=signCode)
        print(sign)
        if sign:
            sign_count = QueryUserSign.get_sign_count_by_signId(sign.signId)
            sign_dict = asdict(sign)
            sign_dict['course'] = asdict(sign.course)
            sign_dict['signCount'] = sign_count
            return sign_dict
        return None

    @staticmethod
    def get_signs_by_courseId(courseId, count=True, desc=True):
        if desc:
            signs = db.session.query(Sign).filter_by(courseId=courseId).order_by(db.desc(Sign.signId)).all()
        else:
            signs = db.session.query(Sign).filter_by(courseId=courseId).order_by(db.asc(Sign.signId)).all()
        sign_list = []
        for sign in signs:
            sign_dict = asdict(sign)
            if count:
                sign_dict['signCount'] = QueryUserSign.get_sign_count_by_signId(sign.signId)
            sign_list.append(sign_dict)
        return sign_list

    @staticmethod
    def _get_latest_sign(**kwargs):
        """ 根据签到码获取结束最晚的签到 """
        oldest_sign = db.session.query(Sign).filter_by(**kwargs).order_by(db.desc(Sign.endTimeStamps)).first()
        return oldest_sign

    @staticmethod
    def delete_sign(signId):
        affected_rows = db.session.query(Sign).filter_by(signId=signId).delete()
        db.session.commit()
        return affected_rows != 0

    @staticmethod
    def get_sign_by_signId(signId):
        sign = db.session.query(Sign).filter_by(signId=signId).first()
        if sign:
            sign_dict = asdict(sign)
            sign_dict['course'] = asdict(sign.course)
            sign_dict['signCount'] = QueryUserSign.get_sign_count_by_signId(sign.signId)
            return sign_dict
        return None
