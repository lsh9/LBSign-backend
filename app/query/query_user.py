from dataclasses import asdict

from app.database import db
from app.database.models import User


class QueryUser:
    @staticmethod
    def get_user(**kwargs):
        user = db.session.query(User).filter_by(**kwargs).first()
        return asdict(user) if user else None

    @staticmethod
    def add_user(**kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return asdict(user)

    @staticmethod
    def set_user(data):
        affected_rows = db.session.query(User).filter_by(userid=data['userid']).update(data)
        db.session.commit()
        return affected_rows != 0
