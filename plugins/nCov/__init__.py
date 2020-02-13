import asyncio
import re
import time
from typing import Optional, List, Dict, Any

from aiocache import cached
from nonebot import MessageSegment
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.command.argfilter import extractors, validators

import json
import requests
import traceback

from jieba import posseg

__plugin_name__ = '新型冠状病毒（SARS-CoV-2）数据'
__plugin_usage__ = r"""
新型冠状病毒（SARS-CoV-2）数据(丁香园)

用法：疫情 ([地市名])
"""


@cached(ttl=5 * 60) # 5 min
async def get_nCov_data(keyword: str) -> str:
    keyword = keyword.strip()
    ret = "API 请求失败，请检查您的输入是否规范，或是联系机器人作者！"
    print('Searching  ' + keyword)
    # 源站居然经常报502，再多层检测
    api_overall = "https://lab.isaaclin.cn/nCoV/api/overall"
    resp = requests.get(api_overall)
    if not resp.status_code == 200:
        ret = "[{}]抱歉，Server 端到 API 的请求出错！\n错误详情：\n{}".format(str(resp.status_code),str(resp.text))
        return ret
    if not keyword or keyword == '全部':
        payload = json.loads(resp.text)
        try:
            nowt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(payload['results'][0]['updateTime'])/1000))
            res = payload['results'][0]
            ret = "新型冠状病毒（SARS-CoV-2）数据汇总(丁香园)：\n截至 {} \n累计确诊：{}（较昨日+{}）\n疑似：{}（较昨日+{}）\n重症：{}（较昨日+{}）\n死亡：{}（较昨日+{}）\n治愈：{}（较昨日+{}）".format(str(nowt),res['confirmedCount'],res['confirmedIncr'],res['suspectedCount'],res['suspectedIncr'],res['seriousCount'],res['seriousIncr'],res['deadCount'],res['deadIncr'],res['curedCount'],res['curedIncr'])
            print('get')
            return ret
        except (TypeError, KeyError, IndexError):
            print(traceback.format_exc())
            return ret
        
    api_area = "https://lab.isaaclin.cn/nCoV/api/area?latest=1"
    resp = requests.get(api_area)
    payload = json.loads(resp.text)
    if not isinstance(payload, dict) or \
            len(payload['results']) == 0:
        return ret
    resu = payload['results']
    try:
        for prov in resu:
          nowt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(prov['updateTime'])/1000))
          if keyword in prov['provinceName']: # 省
              res = prov 
              if prov['provinceName'] == prov['country']:
                  countryName = prov['provinceName']
              else:
                  countryName = prov['country'] + prov['provinceName']
              ret = "新型冠状病毒（SARS-CoV-2）数据汇总(丁香园)：\n{} 截至 {} \n累计确诊：{}\n疑似：{}\n死亡：{}\n治愈：{}".format(countryName,str(nowt),res['confirmedCount'],res['suspectedCount'],res['deadCount'],res['curedCount'])
              print('get')
              return ret 
          #print(prov['cities'])
          if prov['cities']:
            for city in prov['cities']:
              if keyword in city['cityName']:
                  res = city
                  countryName = prov['country'] + prov['provinceName'] + res['cityName']
                  ret = "新型冠状病毒（SARS-CoV-2）数据汇总(丁香园)：\n{} 截至 {} \n累计确诊：{}\n疑似：{}\n死亡：{}\n治愈：{}".format(countryName,str(nowt),res['confirmedCount'],res['suspectedCount'],res['deadCount'],res['curedCount'])
                  print('get')
                  return ret


          
    except (TypeError, KeyError, IndexError):
        print(traceback.format_exc())
        return ret


# on_command 装饰器将函数声明为一个命令处理器
@on_command('nCov', aliases=('疫情', '疫情查询', 'nCov'), only_to_me=False)
async def nCov(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪里的疫情呢？（查看汇总请回复 全部）')
    # 获取城市的天气预报
    report = await get_nCov_data(city)
    # 向用户发送天气预报
    await session.send(report)



# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@nCov.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        #session.pause('要查询的名称不能为空呢，请重新输入（想要查询汇总信息请发送“疫情 全部”）')
        session.state['city'] = '全部'
        return

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    #session.state[session.current_key] = stripped_arg

# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords={'疫情'})
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg)

    city = None
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'ns':
            # ns 词性表示地名
            city = word.word

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'nCov', current_arg=city or '')
