from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # from app import db
        # db.drop_all()
        # db.create_all()
        pass

    app.run(port=app.config['APP_PORT'], host=app.config['APP_HOST'])
