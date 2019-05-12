#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from matplotlib import ticker as mticker
from matplotlib import dates as mdate
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
from pandas.plotting import register_matplotlib_converters as rmc
from matplotlib.ticker import FuncFormatter
from wordcloud import WordCloud
from PIL import Image

"""
-------------------------------------------------
   File Name:     draw.py
   Author:        fynn-PC
   date:          2019/5/9 22:51
   Software:      PyCharm
-------------------------------------------------
"""
'''
1、从1月1日到5月7日每日票房曲线
2、从1月1日到5月7日观影人数最多20天
3、总购票数、在线购票、猫眼购票信息对比
4、电影票购买渠道分布
5、词云
'''


def drawWordCloud(data):
    boxInfo = []
    data.drop_duplicates(subset='movieName', keep='last', inplace=True)
    for i in data['sumBoxInfo']:
        if i[-1] == '万':
            boxInfo.append(eval(i[:-1]))
        else:
            boxInfo.append(eval(i[:-1]) * 10000)
    data['boxInfo'] = boxInfo
    tmp = data.sort_values(
        by='boxInfo',
        axis=0,
        ascending=False).drop(
        'sumBoxInfo',
        axis=1)
    t_dict = {}
    for i in range(len(tmp)):
        t_dict[tmp.iloc[i, 0]] = tmp.iloc[i, 1]
    # 加载背景图片
    cloud_mask = np.array(Image.open("img/python.jpg"))
    # 生成wordcloud对象
    wc = WordCloud(background_color="white",
                   font_path="C:\\Windows\\Fonts\\simkai.ttf",
                   mask=cloud_mask,
                   max_words=2000,
                   min_font_size=10,
                   max_font_size=60,
                   random_state=40,)
    wc.generate_from_frequencies(t_dict)
    wc.to_file("img/最热门电影.png")
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def drawBuyInfo(data):

    plt.rcParams['font.sans-serif'] = ['SimHei']
    # pandas要求注册mat时使用，消除警告
    rmc(explicit=True)
    fig = plt.figure()
    font = {'size': 12}
    ax = fig.add_subplot(111)
    ax.set_title('购票方式占比', font)
    ax.set_ylabel('票房', font)
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%m/%d'))
    ax.xaxis.set_major_locator(mticker.MultipleLocator(14))
    ax.plot(
        data.index,
        data['maoyanViewInfo'] /
        data['onlineViewInfo'],
        'y-',
        label='猫眼占网络渠道比列')
    ax.plot(
        data.index,
        data['maoyanViewInfo'] /
        data['viewInfo'],
        'g--',
        label='猫眼占总渠道比例')
    ax.plot(
        data.index,
        data['onlineViewInfo']/
        data['viewInfo'],
        'r-',
        label='网购占总渠道比例')
    plt.legend(loc='best')

    # 用于处理Y轴百分比
    def to_percent(temp, position):
        return '%1.0f' % (100 * temp) + '%'

    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    plt.savefig("img/购票方式占比.png")
    plt.show()


def drawViewInfo(data):

    plt.rcParams['font.sans-serif'] = ['SimHei']
    data.index = data.index.strftime('%m-%d')
    tmp = data.drop('totalbox', axis=1)
    font = {'size': 12}
    tmp.plot.area()
    plt.title('电影票购买渠道', font)
    plt.ylabel('电影票数', font)
    plt.savefig("img/电影票购买渠道.png")
    plt.show()


def drawTop20Day(data):
    '''
    绘制票房前20的天数
    :param data:
    :return: None
    '''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    data.index = data.index.strftime('%m-%d')
    font = {'size': 12}
    data.plot(kind='bar', color='g')
    plt.title('2019票房前20天数', font)
    plt.ylabel('票房', font)
    plt.savefig("img/2019票房前20天数.png")
    plt.show()


def drawBoxInfo(data):
    '''
    绘制2019年票房走势
    :param data:
    :return: None
    '''

    plt.rcParams['font.sans-serif'] = ['SimHei']
    # pandas要求注册mat时使用，消除警告
    rmc(explicit=True)
    fig = plt.figure()
    font = {'size': 12}
    ax = fig.add_subplot(111)
    ax.set_title('2019年票房走势', font)
    ax.set_xlabel('日期', font)
    ax.set_ylabel('票房', font)
    # 设置X轴坐标间距
    # ax.set_xticks(range(0, len(data), 20))
    # ax.set_xticklabels(data.index.strftime('%m-%d')[::20])
    # 设置X轴坐标间距
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%m/%d'))
    ax.xaxis.set_major_locator(mticker.MultipleLocator(14))
    # 根据轴的时间时间属性来设置坐标
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%m/%d'))
    # ax.set_xticks(pd.date_range('2019-01-01', '2019-05-07', freq='15d'))
    ax.plot(data.index, data['totalbox'], color='g')
    ax.annotate('春节',
                xy=('2019-02-05',
                    data.loc['2019-02-05',
                             'totalbox']),
                xytext=('2019-02-15',
                        data.loc['2019-02-05',
                                 'totalbox']),
                xycoords='data',
                fontsize=12,
                arrowprops=dict(arrowstyle='->',
                                connectionstyle="arc3,rad=.2"))
    ax.annotate('情人节',
                xy=('2019-02-14',
                    data.loc['2019-02-14',
                             'totalbox']),
                xytext=('2019-02-24',
                        data.loc['2019-02-14',
                                 'totalbox']),
                xycoords='data',
                fontsize=12,
                arrowprops=dict(arrowstyle='->',
                                connectionstyle="arc3,rad=.2"))
    ax.annotate('复仇者联盟上映',
                xy=('2019-04-23',
                    data.loc['2019-04-24',
                             'totalbox']),
                xytext=('2019-04-01',
                        data.loc['2019-02-14',
                                 'totalbox']),
                xycoords='data',
                fontsize=12,
                arrowprops=dict(arrowstyle='->',
                                connectionstyle="arc3,rad=.2"))
    plt.savefig("img/2019年票房走势.png", dip=500)
    plt.show()


def readData():
    conn = create_engine(
        'mysql+mysqlconnector://root:1231@localhost:3306/self_ind?charset=utf8&auth_plugin=mysql_native_password')
    data_total = pd.read_sql_query(
        'select maoyanViewInfo,onlineViewInfo,viewInfo,totalbox,queryDate from day_total_box',
        con=conn,
        index_col='queryDate')
    # 由于前期在SQL中存储时，没有转化为数字格式，在这里需要转换下
    data_total['onlineViewInfo'] = data_total['onlineViewInfo'].astype(
        np.float)
    sql = "select movieName,sumBoxInfo from daybox "
    data = pd.read_sql_query(sql, con=conn)
    return data_total, data


def run():
    data_total, data = readData()
    drawBoxInfo(data_total)
    drawTop20Day(data_total['totalbox'].sort_values(ascending=False)[0:21])
    # # 这个函数不能放在最后
    drawBuyInfo(data_total)
    drawViewInfo(data_total)
    drawWordCloud(data)
    print("draw end")
