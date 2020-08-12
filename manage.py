#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-06-02 01:23
# @Author  : cxw
# @File    : manage
# @Software: PyCharm

from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.model import *

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()