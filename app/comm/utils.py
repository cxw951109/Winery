#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-05-07 14:14
# @Author  : cxw
# @File    : utils
# @Software: PyCharm

import os
import datetime
import math

def true_return(code=200, data="", msg="请求成功"):
    return {
        "code": code,
        "data": data,
        "msg": msg
    }


def false_return(code=-1, data="", msg="请求失败"):
    return {
        "code": code,
        "data": data,
        "msg": msg
    }


def special_pagination(query, page, page_size):
    import math
    length_query = len(query)
    # 页数
    total_count = math.ceil(length_query / page_size)
    data = query[(page - 1) * page_size: page * page_size]
    pagination = {
        'pagination': {
            'total_count': length_query,
            'page_count': total_count,
            'count': page_size,
            "page_index": int(page),
        },
        "data": data
    }
    return pagination


def func(today, date_list=[], count=0):
    target = (today - datetime.timedelta(days=1))
    target_res = target.strftime("%Y-%m-%d")
    date_list.append(target_res)
    count += 1
    if count >= 7:
        pass
    else:
        func(target, date_list, count)
    return date_list


def func_(today, date_list=[], count=0):
    target = (today - datetime.timedelta(days=1))
    target_res = target.strftime("%Y-%m-%d")
    date_list.append(target_res)
    count += 1
    if count >= 29:
        pass
    else:
        func_(target, date_list, count)
    return date_list


def func_days(start,end,date_list = []):
    start_time = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end_time = datetime.datetime.strptime(end, "%Y-%m-%d").date()
    target = (end_time - datetime.timedelta(days=1))
    date_list.append(str(end_time))
    if start_time == end_time:
        return date_list
    else:
        if target == start_time:
            date_list.append(str(target))
        else:
            func_days(start,str(target), date_list)
    return date_list