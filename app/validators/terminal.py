#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-05-07 14:33
# @Author  : cxw
# @File    : terminal
# @Software: PyCharm
from .base import BaseForm, RegexpValidate
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class ListForm(BaseForm):
    page_index = IntegerField(validators=[
        RegexpValidate(regex="^[0-9]+$", message="page_index只能传数字")
    ], default=1)
    page_size = IntegerField(validators=[
        RegexpValidate(regex="^[0-9]+$", message="page_index只能传数字")
    ], default=8)
    date = StringField(validators=[])
    type = StringField(validators=[])
    input = StringField(validators=[])

class ChartForm(BaseForm):
    date = StringField(validators=[])

class Real_time(BaseForm):
    machine_id = StringField(validators=[])
    timestamp = StringField(validators=[])
    img = StringField(validators=[])