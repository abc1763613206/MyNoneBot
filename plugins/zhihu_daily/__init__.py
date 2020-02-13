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

__plugin_name__ = '知乎日报'
__plugin_usage__ = r"""
获取今天的知乎日报

用法：知乎日报
"""
DAILY_LATEST_API_URL = 'https://news-at.zhihu.com/api/4/news/latest'
DAILY_STORY_URL_FORMAT = 'https://daily.zhihu.com/story/{}'

@cached(ttl=5 * 60) # 5 min
async def get_zhihu_daily() -> str:
    ret = "API 请求失败，若持续出现该问题，请联系机器人作者！"
    resp = requests.get(DAILY_LATEST_API_URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    })
    if not resp.status_code == 200:
        ret = "[{}]抱歉，Server 端到 API 的请求出错！\n错误详情：\n{}".format(str(resp.status_code),str(resp.text))
        return ret
    payload = json.loads(resp.text)
    if not isinstance(payload, dict) or \
            len(payload['stories']) == 0:
        return ret
    
    try:
        stories = payload['stories']
        ret = "知乎日报 {}：\n\n".format(str(payload['date']))
        for story in stories:
          ret +="{}\n{}\n{}\n\n".format(str(story['title']).replace('\\',''),str(story['hint']).replace('\\',''),str(story['']).replace('\\','url'))
        return ret
    except (TypeError, KeyError, IndexError):
        print(traceback.format_exc())
        return ret



@on_command('zhihu_daily', aliases=('知乎日报'), only_to_me=False)
async def zhihu_daily(session: CommandSession):
    ret = await get_zhihu_daily()
    session.finish(ret)



