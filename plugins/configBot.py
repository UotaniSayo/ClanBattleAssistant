#config.py
#通过指令对bot进行配置
#目前指令：


from __future__ import unicode_literals
from nonebot import on_command, CommandSession
from nonebot.permission import GROUP_ADMIN, GROUP
from botCfgDat import NekoBot
import re

#bot实例dict，存储所有bot class，希望是个全局变量
allBotInstance = {}

#指令：设置公会群
#新建bot class并加入实例list，该指令无参数
@on_command('setGroup', aliases=['公会群', '工会群'], permission=GROUP_ADMIN, only_to_me=True)
async def askBoss(session: CommandSession):
	#获取群号
	groupNo = session.ctx['group_id']
	groupNo = str(groupNo)
	#新建bot实例
	newBot = NekoBot()
	newBot.groupNo = groupNo
	allBotInstance[groupNo] = newBot
	
	succeed = '已添加群'+groupNo
	await session.send('succeed')

	
