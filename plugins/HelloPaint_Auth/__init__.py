import asyncio
import json
import nonebot
from nonebot import MessageSegment
from nonebot import on_command, CommandSession

def make_response(ok, result):
    from json import JSONEncoder
    return JSONEncoder().encode({"ok": ok, "result": result})

bot = nonebot.get_bot()


@bot.server_app.route("/paintboard/send_code", methods=["POST"])
def paintboard_send_code():
    token, target, content = request.form["token"], request.form["target"], request.form["content"]
    if token != bot.config.TOKEN:
        return make_response(False, {"message": "token错误"})

    bot.send_private_msg(user_id=target, message=content)
    return make_response(True)