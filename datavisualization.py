from enum import Enum
from PyQt6.QtWidgets import QWidget
import csv
from getweather import getWeather
from ui import ChartDisplay
import pandas as pd
import numpy as np
import pyecharts.options as opts
import pyecharts.charts as pc

# 全局变量
months = ['一月', '二月', '三月', '四月', '五月', '六月', 
          '七月', '八月', '九月', '十月', '十一月', '十二月']

class Where(Enum):
    # 存储城市字符串所用枚举，方便UI模块传参
    Nanjing = 0
    Beijing = 1
    Shanghai = 2
    Guangzhou = 3
    Wuhan = 4
    Lichuan = 5

class GraphType(Enum):
    # 存储功能所用枚举，方便UI模块传参
    Null = 0
    RangeBarChart = 1
    RangePieChart = 2
    LineChart = 3
    WordCloud = 4
    Cmp3DChart = 5
    Heatmap = 6
    CmpBarChart = 7

# 主功能模块在最底下
def getCityName(city: Where):
    match city:
        case Where.Nanjing:
            return 'nanjing'
        case Where.Beijing:
            return 'beijing'
        case Where.Shanghai:
            return 'shanghai'
        case Where.Guangzhou:
            return 'guangzhou'
        case Where.Wuhan:
            return 'wuhan'
        case Where.Lichuan:
            return 'lichuan'

def generateUrl(city: Where, year: str, month: str) -> str:
    weatherTime = year + ('0' + month if int(month) < 10 else month)
    cityName = getCityName(city)
    url = f'https://lishi.tianqi.com/{cityName}/{weatherTime}.html'
    return url

def writeCsv(weathers: list) -> None:
    with open('weather.csv', 'w', newline='', encoding='gbk') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["日期", "最高气温", "最低气温", "天气", "风向"])
        writer.writerows([list(day_weather_dict.values()) 
                          for month_weather in weathers for day_weather_dict in month_weather])
        
def mainFunc(city: Where, feature: GraphType = GraphType.Null, 
             year: str = '2023', parent: QWidget = None):
    # 引用全局变量
    global months

    # 主功能模块函数预处理: 参数检测
    if feature == GraphType.Null:
        raise ValueError('the arg \'feature\' must be specified')   # 抛出异常（异常会在ui模块中被捕获）
    if parent == None:
        # 需要传入qwidget才能显示
        raise ConnectionError('no parent QWidget is loaded, display function error')    
    
    # 抓取url，写入csv
    weathers = []
    for m in range(1, 13):
        url = generateUrl(city, year, str(m))
        weather = getWeather(url)
        weathers.append(weather)
    writeCsv(weathers)
    print(weathers)

    # 主要功能
    data = pd.read_csv('weather.csv', encoding='gbk')

    match feature:
        case GraphType.RangeBarChart:
            # 遍历weathers
            stat = [0 for i in range(12)]   # 列表存储每月满足温度范围在18-26的天数
            for index, row in data.iterrows():
                date, h_temp, l_temp = row['日期'], int(row['最高气温']), int(row['最低气温'])
                y, m, d = [int(i) for i in date.split('-')]
                if 18 <= h_temp <= 26 and 18 <= l_temp <= 26:
                    stat[m - 1] += 1
            chart = pc.Bar()
            chart.add_xaxis(months)
            chart.add_yaxis('天数(单位:天)', stat)
            chart.set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{c}'))
        
        case GraphType.RangePieChart:
            # 遍历weathers
            stat = [0 for i in range(12)]   # 列表存储每月最高温超过30度或者最低温低于5度的天数
            for index, row in data.iterrows():
                date, h_temp, l_temp = row['日期'], int(row['最高气温']), int(row['最低气温'])
                y, m, d = [int(i) for i in date.split('-')]
                if h_temp >= 30 or l_temp <= 5:
                    stat[m - 1] += 1
            # 生成图表
            chart = pc.Pie()
            chart.add('', [list(z) for z in zip(months, stat)])
            chart.set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{c}'))
        
        case GraphType.LineChart:
            # 遍历weathers
            stat = [0 for i in range(12)]   # 列表存储每月日温差大于10的天数
            for index, row in data.iterrows():
                date, h_temp, l_temp = row['日期'], int(row['最高气温']), int(row['最低气温'])
                y, m, d = [int(i) for i in date.split('-')]
                if h_temp - l_temp > 10:
                    stat[m - 1] += 1
            max_v = max(stat)
            max_m = stat.index(max_v) + 1
            h_temp_list, l_temp_list = [], []   # 列表存储当月最高温度
            day_count = 0
            # 遍历weathers
            for index, row in data.iterrows():
                date, h_temp, l_temp = row['日期'], int(row['最高气温']), int(row['最低气温'])
                y, m, d = [int(i) for i in date.split('-')]
                if m == max_m:
                    day_count += 1
                    h_temp_list.append(h_temp)
                    l_temp_list.append(l_temp)
            # 生成图表
            chart = pc.Line()
            chart.add_xaxis([i for i in range(1, day_count + 1)])
            chart.add_yaxis(y_axis=h_temp_list, series_name='最高温', 
                            symbol='circle', is_symbol_show=True, symbol_size=8)
            chart.add_yaxis(y_axis=l_temp_list, series_name='最低温', 
                            symbol='pin', is_symbol_show=True, symbol_size=8)

    
    # 渲染图表
    chart.render()
    display = ChartDisplay(parent)
    display.setHtml('render.html')
    display.show()

if __name__ == '__main__':
    # 单模块测试
    mainFunc(Where.Beijing, GraphType.RangeBarChart, '2023')