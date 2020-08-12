#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 20:56
# @Author  : cxw
# @File    : __init__.py
# @Software: PyCharm

from flask import Blueprint


terminal_router = Blueprint("terminal", __name__)

from . import terminal