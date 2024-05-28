import requests
from lxml import etree
import csv

def getWeather(url):
    weather_info = []
    headers = { }       #加浏览器请求头
    resp = requests.get(url,headers=headers)
    resp_html = etree.HTLM(resp.text)
    resp_list = resp_html.xpath("//ul[@class='thrui']/li")
    for li in resp_list:
        day_weather_info = {}
        day_weather_info['date_time'] = li.xpath("./div[1]/test()")[0].split('')[0]
        high = li.xpath("./div[2]/test()")[0]
        day_weather_info['high'] = high[:high.find('℃')]
        low = li.xpath("./div[3]/test()")[0]
        day_weather_info['low'] = low[:low.find('℃')]
        day_weather_info['weather'] = li.xpath("./div[4]/test()")[0]
        day_weather_info['wind'] = li.xpath("./div[5]/test()")[0]
        weather_info.append(day_weather_info)
    return weather_info


weathers = []


for month in range(1,13):
    weather_time = '2023' + ('0' + str(month) if month < 10 else str(month))
    print(weather_time)
    url = f'https://lishi.tianqi.com/nanjing/{weather_time}.html'
    weather = getWeather(url)
    weathers.append(weather)
print(weathers)


with open("weather.csv","w",newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["日期","最高气温","最低气温","天气","风向"])
    writer.writerows([list(day_weather_dict.values()) for month_weather in weathers for day_weather_dict in month_weather])