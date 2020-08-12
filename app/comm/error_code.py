#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-05-07 14:45
# @Author  : cxw
# @File    : error_code
# @Software: PyCharm

from app.comm.error_base import *


class ParameFail(APIException):

    code = 401
    data = []
    msg = "参数验证失败"


class ResultFail(APIException):

    code = 402
    data = []
    msg = "请求数据失败"


class ResultSuccess(APIException):

    code = 200
    data = []
    msg = "请求数据成功"