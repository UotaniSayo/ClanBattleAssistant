#assist.py
#辅助指令，与公会战报刀查刀功能不直接相关
#目前指令：
#查询boss信息
#发色图（未测试）


from __future__ import unicode_literals
from nonebot import on_command, CommandSession
from nonebot.permission import GROUP, PRIVATE_FRIEND
import re
import csv

from plugins.getEroPic import getEroPic

#指令：查询boss信息，返回boss的双防
@on_command('askBoss', aliases=['查boss', '查Boss', '查BOSS'], permission=GROUP | PRIVATE_FRIEND, only_to_me=True)
async def askBoss(session: CommandSession):
	#获取boss名字，如果没有则为 None
	bossName = session.state['bossName'] if 'bossName' in session.state else None
	#没有输入boss名字时，提示输入
	if not bossName:
		bossName = session.get('bossName', prompt='输入想要查询的boss的阶段数和编号')
	#将汉字替换为数字
	bossName = re.sub('一', '1', bossName)
	bossName = re.sub('二', '2', bossName)
	bossName = re.sub('三', '3', bossName)
	bossName = re.sub('四', '4', bossName)
	bossName = re.sub('五', '5', bossName)
	bossLocStr = re.findall('[0-9]', bossName)
	
	#boss名字第一次检查，确认有两个数字
	if len(bossLocStr) != 2:
		await session.send('guna!')
		return
	bossLoc = [int(bossLocStr[0]), int(bossLocStr[1])]
	bossIndex = 5*(bossLoc[0]-1)+bossLoc[1]
	
	#boss名字第二次检查，确认阶段数和编号未超出范围
	if bossLoc[0]>3 or bossLoc[0]<1 or bossLoc[1]>5 or bossLoc[1]<1:
		await session.send('guna!')
		return
	
	#读取boss信息
	bossInfo = open('./plugins/boss.csv', 'r')
	reader = csv.reader(bossInfo)
	for i, rows in enumerate(reader):
		if i == bossIndex:
			row = rows
	
	#根据信息生成回复内容
	bossAns = bossLocStr[0]+'阶段'+bossLocStr[1]+'号：'+'物理防御'+row[2]+'，魔法防御'+row[3]
	bossInfo.close()
	await session.send(bossAns)
	
#指令解析：查询boss信息
@askBoss.args_parser
async def _(session:CommandSession):
	stripped_arg = session.current_arg_text.strip()
	if session.is_first_run:
		if stripped_arg:
			session.state['bossName'] = stripped_arg
		return
		
	if not stripped_arg:
		session.pause('输入想要查询的boss，阶段数和编号用半角数字')
		
	session.state[session.current_key] = stripped_arg
	
#指令：请求色图，该指令无参数
@on_command('eroPic', aliases=['色图', '涩图'], permission=GROUP | PRIVATE_FRIEND, only_to_me=True)
async def eroPic(session: CommandSession):
	pic = getEroPic()
	#经URL发送图片
	#coolQ air版本不支持发图片
	await session.send(f'[CQ:image, file={pic}]')
    
