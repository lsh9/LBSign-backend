from dataclasses import dataclass

from app.database import db


@dataclass
class User(db.Model):
    __tablename__ = "user"
    userid: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid: str = db.Column(db.String(255), nullable=False, unique=True)
    userName: str = db.Column(db.String(255))
    userNumber: str = db.Column(db.String(255))
    userIdentity: str = db.Column(db.String(255), server_default="student")
    defaultCourseId: int = db.Column(db.Integer)
    avatarUrl: str = db.Column(db.String(255))


@dataclass
class Course(db.Model):
    __tablename__ = "course"
    courseId: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid: int = db.Column(db.Integer, db.ForeignKey("user.userid"), nullable=False)
    courseName: str = db.Column(db.String(255), nullable=False)
    courseDescription: str = db.Column(db.String(255))
    courseLocationName: str = db.Column(db.String(255))
    courseLocationAddress: str = db.Column(db.String(255))
    courseLongitude: int = db.Column(db.Integer)
    courseLatitude: int = db.Column(db.Integer)
    validDistance: float = db.Column(db.Float, server_default="0")

    user = db.relationship("User", backref="course")


@dataclass
class Sign(db.Model):
    __tablename__ = "sign"
    signId: int = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    signName: str = db.Column(db.String(255), nullable=False)
    courseId: int = db.Column(db.Integer, db.ForeignKey("course.courseId"), nullable=False)
    startTimeStamps: int = db.Column(db.Integer, nullable=False, index=True)
    endTimeStamps: int = db.Column(db.Integer, nullable=False, index=True)
    signLongitude: int = db.Column(db.Integer)
    signLatitude: int = db.Column(db.Integer)
    validDistance: float = db.Column(db.Float, server_default="0")
    signCode: str = db.Column(db.String(255), nullable=False, index=True)

    course = db.relationship("Course", backref="sign")


@dataclass
class UserSign(db.Model):
    __tablename__ = "user_sign"
    userSignId: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid: int = db.Column(db.Integer, db.ForeignKey("user.userid"), nullable=False)
    signId: int = db.Column(db.Integer, db.ForeignKey("sign.signId"), nullable=False)
    signTimeStamps: int = db.Column(db.Integer, index=True)
    signUserName: str = db.Column(db.String(255))
    signUserNumber: str = db.Column(db.String(255))
    signLongitude: int = db.Column(db.Integer)
    signLatitude: int = db.Column(db.Integer)
    actualDistance: float = db.Column(db.Float)

    # 关联
    sign = db.relationship("Sign", backref="user_sign")
    user = db.relationship("User", backref="user_sign")
