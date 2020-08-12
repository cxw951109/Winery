#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-05-07 14:44
# @Author  : cxw
# @File    : error_base
# @Software: PyCharm

from werkzeug.exceptions import HTTPException
from flask import json
from app.comm.log import *


class APIException(HTTPException):

    code = -1
    msg = "请求系统错误"
    data = []

    def __init__(self, code=None, msg=None, data=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            code=self.code,
            msg=self.msg,
            data=self.data
        )
        # log.info(body)
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]