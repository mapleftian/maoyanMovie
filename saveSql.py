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

fileList = []
for root,dir,files in os.walk(os.getcwd()):
    fileList = files

#转为pandas进行处理
with open('data/20190501.txt','r',encoding='utf8') as fp:
    tmp = json.loads(fp.read())
curBox_tmp = tmp['data'].pop('list')
dayBox = pd.DataFrame(curBox_tmp)
dayBox['queryDate'] = '20190501'
#由于crystal字段又是一个字典，在这里进行合并
day_total_box_tmp = tmp['data'].pop('crystal')
day_total_box_tmp.update(tmp['data'])
day_total_box = pd.DataFrame(day_total_box_tmp,index=[0])

conn = create_engine()



