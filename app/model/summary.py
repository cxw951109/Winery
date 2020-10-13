#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-06-03 12:02
# @Author  : cxw
# @File    : summary
# @Software: PyCharm

from app import db
from datetime import datetime
from app.comm import utils

class Summary(db.Model):
    __tablename__ ='summary'

    id = db.Column(db.Integer,autoincrement=True,primary_key=True,nullable=False,comment="id")
    all_num = db.Column(db.Integer,nullable=False,default=0,comment='总检测数')
    today_num = db.Column(db.Integer, nullable=False, default=0, comment='今日检测数')
    all_impuritynum = db.Column(db.Integer,nullable=False,default=0,comment='总杂质数')
    today_impuritynum = db.Column(db.Integer,nullable=False,default=0,comment='今日杂质数')
    created_at = db.Column(db.DateTime,default=datetime.now,nullable=False,comment='时间')


    def __init__(self,all_num, today_num, all_impuritynum,today_impuritynum):
        self.all_num = all_num
        self.today_num = today_num
        self.all_impuritynum = all_impuritynum
        self.today_impuritynum = today_impuritynum

    def to_dict(self):
        return {
            "id":self.id,
            "all_num": self.all_num,
            "today_num": self.today_num,
            "all_impurity_num": self.all_impuritynum,
            "today_impurity_num": self.today_impuritynum
        }

    @classmethod
    def add(cls, data):
        db.session.add(data)
        return cls

    @classmethod
    def flush(cls):
        db.session.flush()
        return cls

    @classmethod
    def update(cls):
        return cls.session_commit()

    @classmethod
    def session_commit(cls):
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    @classmethod
    def add_all(cls, list_data):
        db.session.add_all(list_data)

    @classmethod
    def get_(cls):
        query = cls.query.filter().first()
        return query

    @classmethod
    def get_mes(cls):
        query = cls.query.filter().first()
        if query:
            result ={
                "today_num": query.today_num,
                "today_good_num":query.today_num - query.today_impuritynum,
                "today_impurity_num": query.today_impuritynum,
            }
        else:
            result ={
                "today_num": 0,
                "today_good_num": 0,
                "today_impurity_num": 0,
            }
        return result