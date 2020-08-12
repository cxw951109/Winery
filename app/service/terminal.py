#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-31 01:05
# @Author  : cxw
# @File    : terminal
# @Software: PyCharm

import math
from . import terminal_router
from app.model.history import History
from app.comm.utils import *
from flask import jsonify
from app.validators.terminal import ListForm,ChartForm,Real_time

@terminal_router.route('/meslist',methods=["POST"])
def meslist():
    form = ListForm().check_param()
    query =History.get_mes(form)
    page = int(form.page_index.data)
    page_size = form.page_size.data
    result= [x.to_dict() for x in query.items]
    length_query = query.total
    total_count = math.ceil(length_query / page_size)
    pagination = {
        'pagination': {
            'total_count': length_query,
            'page_count': total_count,
            'count': page_size,
            "page_index": int(page),
        },
    }
    if result:
        return jsonify(true_return(msg="请求成功",data={"pagination":pagination["pagination"],"data":result}))
    else:
        return jsonify(false_return(msg="请求失败"))


@terminal_router.route('today_detection',methods=["POST"])
def today_detection():
    today =datetime.date.today()
    query  = History.get_today(today.__str__())
    return jsonify(true_return(msg="请求成功",data=query))



@terminal_router.route('/chart',methods=["POST"])
def chart():
    form =ChartForm().check_param()
    if form.date.data:
        start =form.date.data[0][:10]
        end =form.date.data[1][:10]
        date_list = []
        date_list = func_days(start, end, date_list)[::-1]
        result, result1, result2 = History.get_chat(date_list)
    else:
        today = datetime.date.today()
        date_list=[x for x in range(24)]
        # date_list = [today.__str__()]
        # date_list = func(today, date_list)[::-1]
        result,result1,result2 = History.get_chat1(today.__str__())
    if result:
        return jsonify(true_return(msg="请求成功",data={"data":result,"date_list":date_list,"data1":result1,"data2":result2}))
    else:
        return jsonify(false_return(msg="请求失败"))










