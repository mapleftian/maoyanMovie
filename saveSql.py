#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     saveSql.py
   Author:        Fynn-mac
   date:          2019-05-08 16:52
   Software:      PyCharm
-------------------------------------------------
"""

import json
import pandas as pd
import os
from sqlalchemy import create_engine


def run():
    fileList = []
    for root, dir, files in os.walk(os.path.join(os.getcwd(), 'data')):
        fileList = files

    for i, file in enumerate(fileList):
        # 转为pandas进行处理
        with open(f'data/{file}', 'r', encoding='utf8') as fp:
            tmp = json.loads(fp.read())
        curBox_tmp = tmp['data'].pop('list')
        dayBox = pd.DataFrame(curBox_tmp)
        dayBox['queryDate'] = file.split('.')[0]
        # 由于crystal字段又是一个字典，在这里进行合并
        day_total_box_tmp = tmp['data'].pop('crystal')
        day_total_box_tmp.update(tmp['data'])
        day_total_box = pd.DataFrame(day_total_box_tmp, index=[i])
        # 数据库存储
        conn = create_engine(
            'mysql+mysqlconnector://root:1231@localhost:3306/self_ind?charset=utf8&auth_plugin=mysql_native_password')
        pd.io.sql.to_sql(dayBox, 'daybox', conn, if_exists='append')
        pd.io.sql.to_sql(
            day_total_box,
            'day_total_box',
            conn,
            if_exists='append')
    print('sql save end')
