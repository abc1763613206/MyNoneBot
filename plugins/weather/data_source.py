# https://api.isoyu.com/#/?id=_5-%e5%a4%a9%e6%b0%94%e9%a2%84%e6%8a%a5
import requests
import json

async def get_weather_of_city(city: str) -> str:
    webresult = requests.get('https://api.isoyu.com/api/Weather/get_weather', params={
        'city': city
    }, timeout=1)
    data = json.loads(webresult.text)
    #print(type(data))
    #rint(data['msg'])
    Date = data['data']['date']
    City = data['data']['results'][0]['currentCity']
    pm25 = data['data']['results'][0]['pm25']
    WIndex = data['data']['results'][0]['index'] #list
    WData = data['data']['results'][0]['weather_data'] #list
    NowData = WData[0]
    output = str('Hi, 来自'+City+'的朋友:\n现在是: '+NowData['date']+'('+Date+') \n当前天气: '+NowData['weather']+' '+NowData['wind']+'   温度 '+NowData['temperature'] + '\nPM2.5 指数: '+pm25+'\n') #main
    output = str(output+'\n-------------\n今天的天气指数:\n\n')
    for ind in WIndex:
        output = str(output+ind['tipt']+': '+ind['zs']+'\n'+ind['des']+'\n\n')
    output = str(output+'\n-------------\n今天及未来几天的天气预报:\n\n')
    for ind in WData:
        output = str(output+ind['date']+': \n'+ind['weather']+' '+ind['wind']+' 气温'+ind['temperature']+'\n\n')
    output = str(output+'\n-------------\nSource: 百度天气(姬长信API)\n')

    return output
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    # return f'{city}的天气是……'