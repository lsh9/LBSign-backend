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
        oldest_sign = QuerySign._get_oldest_sign(signCode=signCode)
        if oldest_sign is None or oldest_sign.endTimeStamps > time.time():
            # signCode不存在或者不可用（即未到期）
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
        if not QuerySign.is_free_signCode(signCode):
            return None
        sign = QuerySign._get_oldest_sign(signCode=signCode)
        # 检查关联是否成功
        if sign:
            sign_count = QueryUserSign.get_sign_count_by_signId(sign.signId)
            sign_dict = asdict(sign)
            sign_dict['course'] = asdict(sign.course)
            sign_dict['signCount'] = sign_count
            return sign_dict
        return None

    @staticmethod
    def get_signs_by_courseId(courseId):
        signs = db.session.query(Sign).filter_by(courseId=courseId).order_by(db.desc(Sign.signId)).all()
        sign_list = []
        for sign in signs:
            sign_dict = asdict(sign)
            sign_dict['signCount'] = QueryUserSign.get_sign_count_by_signId(sign.signId)
            sign_list.append(sign_dict)
        return sign_list

    @staticmethod
    def _get_oldest_sign(**kwargs):
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
