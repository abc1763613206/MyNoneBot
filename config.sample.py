from nonebot.default_config import *

HOST = '0.0.0.0'
PORT = 8023

# 超级用户，只有超级用户邀请入群才会同意
SUPERUSERS = {10086}
# 管理的群组，在其中的群组有新成员加入时会发欢迎词
MANGROUP = {10086}

# 命令前缀与机器人昵称 参考官方NoneBot设置
COMMAND_START = {'','~', '/', '!', '／', '！'}

NICKNAME = {'Bot','机器人','小i'}

# 腾讯AI聊天API，请去 ai.qq.com 申请，并激活智能闲聊功能
TX_CHAT_APPID = ''
TX_CHAT_APPKEY = ''

# 默认设置为带有如下字段就通过
APPROVE_MSG = 'bot'

