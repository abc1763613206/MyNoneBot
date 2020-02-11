from nonebot import on_request, RequestSession

@on_request('friend')
async def _(session: RequestSession):
    # 判断验证信息是否符合要求
    if session.bot.config.APPROVE_MSG in session.ctx['comment']:
        # 验证信息正确，同意入群
        await session.approve()
        return
    # 验证信息错误，拒绝入群
    await session.reject('请说出暗号！')

