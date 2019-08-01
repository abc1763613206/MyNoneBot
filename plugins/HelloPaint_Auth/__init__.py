import asyncio
import json
import nonebot
from quart import request
from nonebot import MessageSegment
from nonebot import on_command, CommandSession

def make_response(ok, result):
    from json import JSONEncoder
    return JSONEncoder().encode({"ok": ok, "result": result})

bot = nonebot.get_bot()


@bot.server_app.route("/paintboard/send_code", methods=["POST","GET"])
async def paintboard_send_code():
	form = await request.form
    token = form["token"]
    target = form["target"]
    content = form["content"]
    if token != bot.config.TOKEN:
        return make_response(False, {"message": "token错误"})
    try:
        await bot.send_private_msg(user_id=target, message=content)
    except CQHttpError:
        pass
    return make_response(True)