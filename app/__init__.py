#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 20:30
# @Author  : cxw
# @File    : __init__.py
# @Software: PyCharm

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db =SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app, resources=r'/*')
    app.config.from_object("app.setting")

    # 注册ORM
    db.init_app(app)

    # 注册蓝图
    from app.service import terminal_router
    app.register_blueprint(terminal_router, url_prefix="/terminal")


    return app