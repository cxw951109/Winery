#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-07-09 15:20
# @Author  : cxw
# @File    : config
# @Software: PyCharm


import json

with open("config.json") as f:
    parameters = json.load(f)

udp_ip = parameters['udp_ip']
udp_port = parameters['udp_port']
belt_group = parameters["belt_group"]
machine_id_list = parameters["machine_id_list"]
machine_ip_list = parameters["machine_ip_list"]
drop_id_list = parameters["drop_id_list"]

del parameters