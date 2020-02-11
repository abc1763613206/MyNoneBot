# 当前阶段只能发欢迎词，惭愧
from nonebot import on_notice, NoticeSession


# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    if session.ctx['group_id'] in session.bot.config.MANGROUP:
        await session.send('欢迎新朋友～ 进群请先阅读群规哦~')

bot = nonebot.get_bot()
# 群成员入群/邀请登录号入群
@on_request('group')
async def _(session: RequestSession):
    if session.ctx['sub_type'] == 'add': # 加群请求
        # 判断验证信息是否符合要求
        if session.bot.config.APPROVE_MSG in session.ctx['comment']:
            # 验证信息正确，同意入群
            await session.approve()
            return
        # 验证信息错误，拒绝入群
        await session.reject('请说出暗号！')
    elif session.ctx['sub_type'] == 'invite': # 邀请入群
        if session.ctx['user_id'] in session.bot.config.SUPERUSERS:
            # 验证信息正确，同意入群
            await session.approve()
            return
        # 验证信息错误，拒绝入群
        # await session.reject('非超级用户，不能进行邀请操作')
            await bot.send_private_msg(user_id=session.ctx['user_id'], message='抱歉，您不是超级用户，不能进行邀请操作！')

    else:
    	return