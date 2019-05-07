# **爬取并分析猫眼电影票房数据**

## 一、背景

​		目前电影已经是中国人的一种主要的娱乐休闲方式。特别是今年，有着《流浪地球》和《复仇者联盟4-终局之战》等优秀电影。本篇通过爬取猫眼电影19年数据，分析电影市场。

## 二、数据准备

  + 爬虫环境筛选

    通过查询发现，猫眼提供了两种方式查看当日票房信息，为专业版票房榜和常规版票房榜。通过对比发现，常规版票房在爬取过程中，存在一定的难度，比如有字体反扒技术，需要解析字体。对历史数据的爬取也不是很友好。因此我们选取更为友好的专业版票房榜。

  + 爬虫过程分析

    当前，专业版票房的URL为：[猫眼专业版```https://piaofang.maoyan.com/dashboard```](https://piaofang.maoyan.com/dashboard)。

    补充详细的headers信息后，先使用request模板直接爬取该网站，再通过BS4.BeautifulSoup解析后发现，票房信息是放在动态json中的，直接爬取网页无法获取票房信息。

    于是我们通过浏览器检查网页，选择Network，刷新网页，对当前加载项内容进行分析。

    选择second.json这个文件，它的response中正好包含了票房榜的全部数据。同时他的Request Url指向的是：```https://box.maoyan.com/promovie/api/box/second.json```。进入这个地址，果然藏得就是当天的票房信息，还是Json格式的。图片如下：

    ![分析]([https://raw.githubusercontent.com/mapleftian/github-img/master/%E7%8C%AB%E7%9C%BC%E7%94%B5%E5%BD%B1%E7%A5%A8%E6%88%BF%E7%88%AC%E5%8F%96/%E5%9B%BE2-1.PNG?token=ACCT2I5QN5IJBKIHVGFBYVK42G56O](https://raw.githubusercontent.com/mapleftian/github-img/master/猫眼电影票房爬取/图2-1.PNG?token=ACCT2I5QN5IJBKIHVGFBYVK42G56O))

    ![json页面](https://github.com/mapleftian/github-img/blob/master/%E7%8C%AB%E7%9C%BC%E7%94%B5%E5%BD%B1%E7%A5%A8%E6%88%BF%E7%88%AC%E5%8F%96/%E5%9B%BE2-2.PNG?raw=true)

    由于获取的Json文件不包含日期字段，无法获取其他时间的票房信息。我们先退回到票房榜页面。页面左下角有一个时间日期选项，我们先清空下右侧信息（按两次F12键），选取到4月23（复联4上映时间）。发现有一个包含有日期的second.json。

    ![日期分析](https://github.com/mapleftian/github-img/blob/master/%E7%8C%AB%E7%9C%BC%E7%94%B5%E5%BD%B1%E7%A5%A8%E6%88%BF%E7%88%AC%E5%8F%96/%E5%9B%BE2-3.PNG?raw=true)

    点击json文件，跳转到一个地址为[```<https://box.maoyan.com/promovie/api/box/second.json?beginDate=20190423>```](<https://box.maoyan.com/promovie/api/box/second.json?beginDate=20190423>)的地址。正好是我们需要的4月23号信息。我们随便调整下日期，发现数据也随着日期进行变化。OK，此时我们就得到了应该爬取的地址了。

    ![图2-4](https://github.com/mapleftian/github-img/blob/master/%E7%8C%AB%E7%9C%BC%E7%94%B5%E5%BD%B1%E7%A5%A8%E6%88%BF%E7%88%AC%E5%8F%96/%E5%9B%BE2-4.PNG?raw=true)

    测试一下

    ```python
    date = datetime.datetime(2019,4,23)
    url = "https://box.maoyan.com/promovie/api/box/second.json?beginDate="
    date_url = url + date.strftime('%Y%m%d')
    data = requests.get(date_url,headers=headers)
    soup = BeautifulSoup(data.text,'lxml')
    ###注意，原网页是有<html><p>这两个标签的，我们使用bs将其过滤掉
    print(soup.p.string)
    with open("%s.txt" %(date.strftime('%Y%m%d')),'w+',encoding='utf8') as fp:
    	fp.write(str(soup.p.string))
    ```

    查看20190423.txt，输出的正好是刚刚看到的Json信息。自此我们爬取数据成功。

    通过循环我们可以爬取自20190101至20190507的每日数据。

  + 源码展示：

    ```python
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
            #将数据保存到与该程序同目录的data文件夹下，并按照时间进行命名
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
    
    ```

    

## 三、MySql数据存储与读取

+ 存储数据：
+ 读取数据：
+ 源码展示：

## 四、Pandas分析