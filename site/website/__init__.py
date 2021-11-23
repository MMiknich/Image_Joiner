from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# from flask_migrate import Migrate


UPLOAD_FOLDER = 'website/static/uploads/'
db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://admin:admin@db:5432/sitedb'
    db.init_app(app)
    
    from .models import User, Files
    
    # db.drop_all(app=app)
    db.create_all(app=app)

    from .views import views
    from .auth import auth
    from .share import share

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(share, url_prefix='/')



    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app




        
