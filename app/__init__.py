from flask import Flask
from app.api import test_bp, course_bp, sign_bp, user_bp, file_bp
from app.database.models import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config')
    app.config.from_pyfile("config.py", silent=True)
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(test_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(sign_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(file_bp)

    @app.route('/')
    def hello_world():
        return 'Hello World!'
    return app
