from enum import Enum
import csv
import datetime
from getweather import getWeather

# 主功能模块在最底下

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
    LineGraph = 1
    Cmp3DGraph = 2
    CmpBarGraph = 3
    CondBarGraphM = 4
    CondBarGraphY = 5
    CondPieGraphM = 6
    CondPieGraphY = 7

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
    with open('weather.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["日期", "最高气温", "最低气温", "天气", "风向"])
        writer.writerows([list(day_weather_dict.values()) 
                          for month_weather in weathers for day_weather_dict in month_weather])
        
def mainFunc(city: Where, feature: GraphType = GraphType.Null, 
             year: str = '2023', month: str = '1'):
    yearAnalysis = True

    # 主功能模块函数预处理: 参数检测
    if feature == GraphType.Null:
        raise ValueError('the arg \'feature\' must be specified')   # 抛出异常（异常会在ui模块中被捕获）
    
    if feature == GraphType.LineGraph or feature == GraphType.CondBarGraphM or feature == GraphType.CondPieGraphM:
        yearAnalysis = False
    
    # 检测时间月份是否合法
    y, m, d = str(datetime.date.today()).split('-')
    if int(year) > int(y) or (int(year) == int(y) and int(month) >= int(m)):
        raise ValueError('invalid date')
    
    # 抓取url，写入csv
    weathers = []
    if yearAnalysis:
        # 对整年分析
        for m in range(1, 13):
            url = generateUrl(city, year, str(m))
            weather = getWeather(url)
            weathers.append(weather)
    else:
        # 对某月分析
        url = generateUrl(city, year, month)
        weather = getWeather(url)
        weathers.append(weather)
    writeCsv(weathers)
    print(weathers)

    # 

if __name__ == '__main__':
    # 单模块测试
    # print(generateUrl(Where.Beijing, '2023', '4'))
    mainFunc(Where.Beijing, GraphType.CondBarGraphY, '2023')