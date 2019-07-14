from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

import requests
import json

@nonebot.scheduler.scheduled_job('cron', hour='6-23')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        retry_count = 5
        msg = f'Hi, 现在{now.hour}点整啦！'
        while retry_count > 0:
            try:
                webresult = requests.get('https://api.ihcr.top/hitokoto/', timeout=3)
                data = json.loads(webresult.text)
                retry_count = 0
            except Exception:
                retry_count -= 1
        msg = msg + '\n--------------\n本小时的一言(Hitokoto):\n'+data['content']+'\n'+data['translation']+'\n—— '+data['origin']['singer']+' 《'+data['origin']['title']+'》\n'
        for gid in bot.config.MANGROUP:
            await bot.send_group_msg(group_id=gid,
                                 message=msg)
    except CQHttpError:
        pass