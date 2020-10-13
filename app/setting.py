#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 20:31
# @Author  : cxw
# @File    : setting
# @Software: PyCharm

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PWD = "111"
DB_NAME = "test"

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(DB_USER, DB_PWD, DB_HOST, DB_PORT,
                                                                                  DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True