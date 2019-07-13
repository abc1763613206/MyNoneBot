import string
import time
from urllib.parse import urlencode
import hashlib
from random import randint
import json
import aiohttp
from aiocqhttp.message import escape

# https://github.com/amongtheflowers/gadgetBot/blob/master/gadget/untils/chat_txai.py
# 
# 


def get_nonce_str():
    nonce_str_example = 'fa577ce340859f9fe'
    nonce_str = ''
    len_str = string.digits + string.ascii_letters
    for i in range(len(self.nonce_str_example)):
        nonce_str += len_str[randint(0, len(len_str) - 1)]
    return nonce_str


def sign(req_data):
    new_list = sorted(req_data.items())
    encode_list = urlencode(new_list)
    req_data = encode_list + "&" + "app_key" + "=" + self.app_key
    md5 = hashlib.md5()
    md5.update(req_data.encode('utf-8'))
    data = md5.hexdigest()
    return data.upper()

async def call_txchat_api(session: CommandSession, text: str) -> Optional[str]:
    # 调用腾讯AI SDK 获取回复
    app_id = session.bot.config.TX_CHAT_APPID
    app_key = session.bot.config.TX_CHAT_APPKEY
    api_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    ct = lambda: time.time()
    
    req_data = {
            'app_id': app_id,
            'time_stamp': int(self.ct()),
            'nonce_str': get_nonce_str(),
            'session': urlencode(context_id(session.ctx, use_hash=True)),
            'question': text,
    }
    
    req_data['sign'] = sign(req_data)
    req_data = sorted(req_data.items())
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(api_url, params=req_data) as response:
                try:
                    data =  json.loads(await response.text())
                    if data['ret'] == 0:
                        return data['data']['answer']
                    else:
                        return None
                except:
                    print(await response.text())
                    return None
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return None
