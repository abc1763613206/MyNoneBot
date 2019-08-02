import asyncio
import json
import nonebot
from quart import request
from nonebot import MessageSegment
from nonebot import on_command, CommandSession
from aiocqhttp.exceptions import Error as CQHttpError

def make_response(ok, result):
    from json import JSONEncoder
    return JSONEncoder().encode({"ok": ok, "result": result})

bot = nonebot.get_bot()


@bot.server_app.route("/paintboard/send_code", methods=["POST"])
async def paintboard_send_code():
    form = await request.form
    token = form.get("token")
    target = form.get("target")
    content = form.get("content")
    if (token == None) or (target == None) or (content == None):
        return make_response(False, {"message": "参数不完整"})
    if token != bot.config.TOKEN:
        return make_response(False, {"message": "Token错误"})
    try:
        await bot.send_private_msg(user_id=target, message=content)
    except CQHttpError:
        return make_response(False, {"message": "无法与CQ交互，发送失败"})
    return make_response(True,{"message": "发送成功"})
