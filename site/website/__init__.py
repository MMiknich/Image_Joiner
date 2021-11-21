from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin
from sqlalchemy.sql import func


UPLOAD_FOLDER = '/site/uploads/'
db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://flowMaster:Dat_assword@localhost/sitedb'
    # db = SQLAlchemy(app)
    # db.create_all(app=app)

    from .views import views
    from .auth import auth
    # from .share import share

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(share, url_prefix='/')



    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

    return app



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
        
class Files(db.Model):
    gif_ig = db.Column(db.Integer, primary_key=True)
    gif_url = db.Column(db.String(150))
    gif_name = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        
