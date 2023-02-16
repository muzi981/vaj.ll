from datetime import date, datetime, timedelta
import math
from turtle import color
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
from zhdate import ZhDate as lunar_date
from datetime import date, datetime, timedelta
from borax.calendars.lunardate import LunarDate
import requests
import os
import random

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


today = datetime.now() + timedelta(hours=8)

#-----------------------------生日模块----------------------------
#切片获取年月日
n = int(birthday[0:4:1])
y = int(birthday[5:7])
r = int(birthday[8:])
# 农历转阳历
date1 = lunar_date(n, y, r)
#农历日期转换称公历日期.将公里日期输出为字符串
dt_str = date1.to_datetime().strftime('%Y-%m-%d')# 2020-08-25 00:00:00，农历转换成阳历日期  datetime 类型

#生日-----------支持农历生日倒计时
#1、倒计时函数实现方式一：
def get_birthday_l():
  next = date1.to_datetime()
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#2、倒计时函数实现方式二：
def get_birthday_m():
  next = datetime.strptime(dt_str, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#3、倒计时函数实现方式三：
year = LunarDate.today().year  #LunarDate.today().year  获取当前年份
birthday1 = LunarDate(year, y, r)#构建农历日期
birthday2 = birthday1.to_solar_date()#转化成公历日期，输出为字符串
def get_birthday_s():
  next = datetime.strptime(birthday2.strftime("%Y-%m-%d"), "%Y-%m-%d")#先转换成datetime.date类型,再转换成datetime.datetime
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days
#生日倒计时函数源码
# def get_birthday():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days


#------------------------天气api获取模块----------------------------
#墨迹天气api
# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][0]
#   return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])

#天行数据api  https://api.tianapi.com/tianqi/index?key=19131d4a18378e7b5ff4c44a608b03d3&city=
def get_weather1():
  url = "https://api.tianapi.com/tianqi/index?key=19131d4a18378e7b5ff4c44a608b03d3&city=" + city
  res1 = requests.get(url).json()
  muzi = res1['newslist'][0]
  #area 城市  weather = 今天天气  real = 当前温度  lowest = 最低气温  highest= 最高气温  wind = 风项  windsc = 风力
  return muzi['area'], muzi['weather'], muzi['real'], muzi['lowest'], muzi['highest'], muzi['wind'], muzi['windsc'], muzi['tips'], muzi['week'], muzi['sunrise'], muzi['sunset'], muzi['humidity'], muzi['aqi']

#墨迹天气pm25
def get_weather3():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + '合肥'
  res1 = requests.get(url).json()
  # weather = res['data']['list'][0]
  muzi1 = res1['data']['list'][0]
  return math.floor(muzi1['pm25'])   #tips, area, weather, real, temperature, highest, lowest = get_weather1()

#兼容pm2。5数据接口
# def get_weather2():
#   # if city is None:
#   #   print('请设置城市')
#   #   return None
#   url = "https://v0.yiketianqi.com/api?unescape=1&version=v61&appid=78158848&appsecret=650ylFRx&city=" + city
#   res = requests.get(url).json()
#   return res['week'],res['wea'], res['alarm'],res['aqi'], res['win'],res['win_speed'],res['tem'], res['tem2'], res['tem1'],res['air_tips'], res['pm25']


#--------------------------农历日期api获取模块---------------------------
#农历接口
def get_lunar_calendar():
  date = today.strftime("%Y-%m-%d")
  url = "http://api.tianapi.com/lunar/index?key=d5edced4967c76fd11899dbe1b753d91&date=" + date
  lunar_calendar = requests.get(url,verify=False).json()
  res3 = lunar_calendar['newslist'][0]
  return res3['lubarmonth'],res3['lunarday'],res3['jieqi'],res3['lunar_festival'],res3['festival']




def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days


#彩虹屁接口
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

#朋友圈文案api接口
def get_words1():
  words1 = requests.get("https://api.shadiao.pro/pyq")
  if words1.status_code != 200:
    return get_words1()
  return words1.json()['data']['text']

#随机颜色1
# def get_random_color():
#   return "#%06x" % random.randint(0, 0xFFFFFF)

#随机颜色2
def get_random_color():
  colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
  color = ""
  for i in range(6):
      color += colorArr[random.randint(0,14)]
  return "#"+color

def get_1():
  ews = get_weather1()
  win = ews[1]
  yu = ''
  if win == '雷阵雨转中雨':
      return '⛈'

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
# wea, temperature, highest, lowest = get_weather()
area, weather, real, lowest, highest, wind, windsc, tips, week, sunrise, sunset, humidity, aqi = get_weather1()
# pm25 = get_weather3()
lubarmonth, lunarday, jieqi, lunar_festival, festival = get_lunar_calendar()
url = "https://www.baidu.com/"
data = {
    # "url": "https://www.baidu.com",
    "date1": {
        'value':'📅'
    },
    "city1": {
        'value':'🏙'
    },
    "tq": {
        "value":'☀'
    },
    "wind_windsc": {
        "value":'🌀'
    },
    "temperature1": {
        'value':'🌡'
    },
    "lowest1": {
        'value':'🌑'
    },
    "highest1": {
        'value':'🌈'
    },
    #pm25
    "pm25_1":{
        "value":'😷'
    },
    "sunrise1":{
        "value":'🌅日出：'
    },
    "sunset1":{
        "value":'🌇日落：'
    },
    "humidity1":{
        "value":'📉湿度：'
    },
    "tips1": {
        "value":'👗'
    },
    "love_days1": {
        'value':'🥰我们已经相爱：'
    },
    "birthday_left1": {
      "value":'🎂你的生日还有：'
    },
    # "birthday_left": {
    #     "value":get_birthday(),
    #     "color":get_random_color()
    # },

    #日期：今天日期
    "date": {
        'value':today.strftime('%Y年%m月%d日'+lubarmonth+lunarday+week),
        'color':get_random_color()
    },
    #所在城市
    "area":{
        "value":area,
        "color":get_random_color()
    },
    # "city": {
    #     "value":city,
    #     "color":get_random_color()
    # },

    #天气
    "weather":{
        "value":weather,
        "color":get_random_color()
    },
    #风向
    "wind": {
        "value":wind,
        "color":get_random_color()
    },
    #风速
    "windsc": {
        "value":windsc,
        "color":get_random_color()
    },
    #当前温度
    "real":{
        "value":real,
        "color":get_random_color()
    },
    #低温
    "lowest":{
        "value":lowest,
        "color":get_random_color()
    },
    #高温
    "highest":{
        "value":highest,
        "color":get_random_color()
    },
    #pm25
    "pm25": {
        "value":aqi,
        "color":get_random_color()
    },
    "sunrise":{
        "value":sunrise,
        "color":get_random_color()
    },
    "sunset":{
        "value":sunset,
        "color":get_random_color()
    },
    "humidity":{
        "value":humidity,
        "color":get_random_color()
    },
    #穿衣建议：
    "tips":{
        "value":tips,
        "color":get_random_color()
    },
    #相爱时间
    "love_days": {
        "value":get_count(),
        "color":get_random_color()
    },
    #生日倒计时
    "birthday_left": {
        "value":get_birthday_l(),
        "color":get_random_color()
    },
    #随机情话
    "words": {
        "value":get_words(),
        "color":get_random_color()
    },
    #今天天气
    # "weather": {
    #     "value":'🌤今天天气：'+wea,
    #     "color":get_random_color()
    # },

    # "temperature": {
    #     "value":temperature,
    #     "color":get_random_color()
    # },

    # "highest": {
    #     "value":highest,
    #     "color":get_random_color()
    # },
    # "lowest": {
    #     "value":lowest,
    #     "color":get_random_color()
    # },

    #日期
    # "date":{
    #     "value":date,
    #     "color":get_random_color()
    # },
}
# data = {"date1":{'value':'📅今天是：'},"city1":{'value':'🏙城市：'},"tq":{"value":'🌤今天天气：'},"temperature1":{'value':'🌡当前温度：'},"lowest1":{'value':'🌑今日最低温：'},"highest1":{'value':'🌈今日最高温：'},"love_days1":{'value':'🥰我们已经相爱：'},"date":{'value':today.strftime('%Y年%m月%d日'),'color':'#2fe30d'},"weather":{"value":'🌤今天天气：'+wea,"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"love_days":{"value":get_count(),"color":get_random_color()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(),"color":get_random_color()},"highest": {"value":highest,"color":get_random_color()},"lowest":{"value":lowest, "color":get_random_color()}"tips":{}}
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data, url)
  count+=1
print("发送了" + str(count) + "条消息")
