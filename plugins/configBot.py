#config.py
#通过指令对bot进行配置
#目前指令：
#设置公会群


from __future__ import unicode_literals
import nonebot
from nonebot import on_command, CommandSession
from nonebot.permission import GROUP_ADMIN, GROUP
from plugins.botCfgDat import MadaBot
import re

#bot实例dict，存储所有bot class，希望是个全局变量
allBotInstance = {}

#指令：注册公会群
#为发消息的群新建bot实例并加入实例list，该指令无参数
@on_command('addGroup', aliases=['注册', '登录', '登陆'], permission=GROUP_ADMIN, only_to_me=True)
async def addGroup(session: CommandSession):
	#获取群号
	groupNo = session.ctx['group_id']
	groupNo = str(groupNo)
	if groupNo in allBotInstance.keys():
		await session.send('该群已经注册，不要重复操作哦')
		return
	#新建bot实例
	newBot = MadaBot()
	newBot.groupNo = groupNo
	allBotInstance[groupNo] = newBot
	
	succeed = '已添加群'+groupNo
	await session.send(succeed)
	
#指令：注销公会群
#将发消息的群从实例list中移除，该指令无参数
@on_command('removeGroup', aliases=['注销', '退出'], permission=GROUP_ADMIN, only_to_me=True)
async def removeGroup(session: CommandSession):
	#获取群号
	groupNo = session.ctx['group_id']
	groupNo = str(groupNo)
	#删除实例
	try:
		del allBotInstance[groupNo]
	except:
		pass
	succeed = '已移除群'+groupNo
	await session.send(succeed)

#指令：设置bot实例
#设置实例的以下参数：
#允许普通成员将自己添加进列表
#公会成员群昵称标签
#允许报刀不提供伤害
@on_command('options', aliases=['设置', '配置'], permission=GROUP_ADMIN, only_to_me=True)	
async def options(session: CommandSession):
	#获取群号
	groupNo = session.ctx['group_id']
	groupNo = str(groupNo)
	if not(groupNo in allBotInstance.keys()):
		await session.send('该群尚未注册，请先注册哦')
		return
	#to do
	#这部分尽量在全部实例参数确定下来之后再进行

#指令：自动更新公会成员
#需要设置群昵称标签，该指令无参数
@on_command('updateClanMbr', aliases=['更新成员', '更新团员'], permission=GROUP_ADMIN, only_to_me=True)
async def updateClanMbr(session: CommandSession):
	#获取群号
	groupNo = session.ctx['group_id']
	groupNo = str(groupNo)
	if not(groupNo in allBotInstance.keys()):
		await session.send('该群尚未注册，请先注册哦')
		return
	
	thisBot = allBotInstance[groupNo]
	
	botApi = nonebot.get_bot()
	thisBot.clanMbr = []
	mbrList = []
	try:
        #获取群成员列表，格式为list[dict]
		mbrList = await botApi.get_group_member_list(group_id=int(groupNo))
	except:
		await session.send('出错啦，再试一下咯')
		return
	
	for user in mbrList:
		if re.search(thisBot.mbrTag, user['card']):
			thisBot.clanMbr.append(str(user['user_id']))
			
	if len(thisBot.clanMbr) > 30:
		thisBot.clanMbr = []
		await session.send('失败：成员超过30个，请检查标签')
		return
	
	result = '更新完成，目前有{0}成员。'.format(len(thisBot.clanMbr))
	await session.send(result)
