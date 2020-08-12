#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-05-07 14:36
# @Author  : cxw
# @File    : base
# @Software: PyCharm

import json
from wtforms import Form
from wtforms.validators import Length, ValidationError, Regexp
from flask import request
from app.comm.error_code import *


class BaseForm(Form):
    def __init__(self):
        data_post = request.form.to_dict()
        # log.info("请求参数form： {}".format(request.form))
        # log.info("请求参数args： {}".format(request.args))
        # log.info("请求参数data： {}".format(request.data))
        try:
            data_json = request.json
            if data_json:
                pass
            else:
                text = str(request.data, encoding="utf-8")
                data_json = json.loads(text)
        except Exception as e:
            data_json = ""
            print(e)
        data_get = request.args.to_dict()
        if data_post:
            data = data_post
        elif data_json:
            data = data_json
        elif data_get:
            data = data_get
        else:
            data = None
        # log.info("请求参数：{}".format(data))
        # log.info(data)
        super(BaseForm, self).__init__(data=data)

    def check_param(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            data = {"msgtype": "text", "text":
                {
                    "content": {
                        "提示": "参数错误",
                        "url": request.base_url,
                        "param": self.data,
                        "errors": self.errors,
                    }
                }
                    }
            raise ParameFail(msg=self.errors)
        return self

class RegexpValidate(Regexp):
    '''
    正则验证
    '''
    def __call__(self, form, field, message=None):
        data = field.data and str(field.data) or ''
        match = self.regex.match(data)
        if not data:
            return match
        if not match:
            if message is None:
                if self.message is None:
                    message = field.gettext('Invalid input.')
                else:
                    message = self.message

            raise ValidationError(message)
        return match