# 当前阶段只能发欢迎词，惭愧
from nonebot import on_notice, NoticeSession


# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    if session.ctx['group_id'] in session.bot.config.MANGROUP:
        await session.send('欢迎新朋友～ 进群请先阅读群规哦~')