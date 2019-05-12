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
import numpy as np


def run():
    fileList = []
    for root, dir, files in os.walk(os.path.join(os.getcwd(), 'data')):
        fileList = files

    # 数据库存储
    conn = create_engine(
        'mysql+mysqlconnector://root:1231@localhost:3306/self_ind?charset=utf8&auth_plugin=mysql_native_password')

    # 也可以循环读取，单次写入
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
        # 这里由于仅是一条数据，所以需要加一个索引
        day_total_box = pd.DataFrame(day_total_box_tmp, index=[i])
        # 格式转换
        dayBox['queryDate'] = file.split('.')[0]
        dayBox['splitBoxInfo'] = dayBox['splitBoxInfo'].astype(np.float)
        dayBox['boxInfo'] = dayBox['boxInfo'].astype(np.float)
        dayBox['avgViewBox'] = dayBox['avgViewBox'].astype(np.float)
        dayBox['showInfo'] = dayBox['showInfo'].astype(np.float)
        dayBox['queryDate'] = pd.to_datetime(dayBox['queryDate'])
        day_total_box['maoyanViewInfo'] = day_total_box['maoyanViewInfo'].astype(
            np.float)
        day_total_box['viewInfo'] = day_total_box['viewInfo'].astype(np.float)
        # 莫名出错
        # day_total_box["onlineViewInfo"] = day_total_box["onlineViewInfo"].astype(np.float)
        day_total_box['totalBox'] = day_total_box['totalBox'].astype(np.float)
        day_total_box['queryDate'] = pd.to_datetime(day_total_box['queryDate'])

        pd.io.sql.to_sql(dayBox, 'daybox', conn, if_exists='append',)
        pd.io.sql.to_sql(
            day_total_box,
            'day_total_box',
            conn,
            if_exists='append')
    print('sql save end')
