#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import datetime
from bs4 import BeautifulSoup
"""
-------------------------------------------------
   File Name:     DownData.py
   Author:        fynn-PC
   date:          2019/5/6 22:26
   Software:      PyCharm
-------------------------------------------------
"""
'''
此部分用于下载数据
'''


class downData():

    def __init__(self):
        '''
        :param year: 爬虫开始年份
        :param month: 爬虫开始月份
        :param day: 爬虫开始天数
        '''
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }
        self.year = 2019
        self.month = 1
        self.day = 2

    def run(self):
        year = self.year
        month = self.month
        day = self.day
        beginDate = datetime.datetime(self.year, self.month, self.day)
        while beginDate.strftime('%Y%m%d') < time.strftime("%Y%m%d", time.localtime()):
            self._download(beginDate.strftime('%Y%m%d'))
            #休息两秒
            print(f"已完成{beginDate.strftime('%Y%m%d')}文件的下载。")
            time.sleep(2)
            beginDate += datetime.timedelta(days=1)

    def _download(self, date):
        '''
        内部函数
        :param date: 内部参数，爬取当天的日期
        :return: 保存数据
        '''
        url = f"https://box.maoyan.com/promovie/api/box/second.json?beginDate={date}"
        data = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(data.text, 'lxml')
        with open(f"data/{date}.txt", 'w+', encoding='utf8') as fp:
            fp.write(str(soup.p.string))


if __name__ == '__main__':
    year = 2019
    month = 1
    day = 1
    d = downData()
    d.year = year
    d.month = month
    d.day = day
    d.run()
    print("end")
