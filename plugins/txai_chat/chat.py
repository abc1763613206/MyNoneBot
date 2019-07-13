# 参照 https://ai.qq.com/doc/sdk.shtml
from .apiutil import *
#import apiutil

app_id = session.bot.config.TX_CHAT_APPID
app_key = session.bot.config.TX_CHAT_APPKEY


async def call_txchat_api(session: CommandSession, text: str) -> Optional[str]:
    # 调用腾讯AI SDK 获取回复

    if not text:
        return None

    ai_obj = AiPlat(app_id, app_key)
    rsp = ai_obj.getNlpTextChat(text,context_id(session.ctx, use_hash=True))
    if rsp['ret'] == 0:
        return json.dumps(rsp, encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4)
    else:
        print (json.dumps(rsp, encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4))
        return None