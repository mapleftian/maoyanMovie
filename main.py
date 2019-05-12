#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     main.py
   Author:        fynn-PC
   date:          2019/5/8 23:34
   Software:      PyCharm
-------------------------------------------------
"""
import saveSql as ssql
import DownData as dd
import draw


def run():
    down = dd()
    down.run()
    ssql.run()
    draw.run()


if __name__ == '__main__':
    run()
