#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-06-03 12:02
# @Author  : cxw
# @File    : imgs
# @Software: PyCharm

from app import db
from datetime import datetime
from app.comm import utils

class Imgs(db.Model):
    __tablename__ ='imgs'

    id = db.Column(db.Integer,autoincrement=True,primary_key=True,nullable=False,comment="id")
    img = db.Column(db.String(255),nullable=False,default='',comment='图片')
    img1 = db.Column(db.String(255),nullable=False,default='',comment='图片1')
    img2 = db.Column(db.String(255),nullable=False,default='',comment='图片2')
    img3 = db.Column(db.String(255),nullable=False,default='',comment='图片3')
    history_id =db.Column(db.Integer, db.ForeignKey('history.id'),  nullable=True)


    def __init__(self, img, img1,img2,img3,history_id):
        self.img = img
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3
        self.history_id = history_id

    def to_dict(self):
        return {
            "id":self.id,
            "img": self.img,
            "history_id": self.history_id
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
