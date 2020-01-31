from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

from web_chatroom.model.models import *
from web_chatroom.auth import auth
from web_chatroom.chat import chat

login_manager.blueprint_login_views='auth.login'
# from web_chatroom.chat import chat


# 用于从缓存中得到存在用户登录
@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return db.session.query(User).filter(User.id == user_id).first()


# @login_manager.user_loader
# def login_user(user_id):
#     print(db.session.query(User).filter(User.id == user_id).first())
#     if db.session.query(User).filter(User.id == user_id).first():
#         return redirect(url_for('chat.chat'))
#     else:
#         return redirect(url_for('auth.login'))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.register_blueprint(chat)
    # 添加配置
    app.config.from_object('web_chatroom.settings.Config')
    # 读取配置
    db.init_app(app)
    login_manager.init_app(app)
    CSRFProtect(app)

    return app
