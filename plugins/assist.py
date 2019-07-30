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
#可选参数：boss的阶段数和编号
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
	bossInfo = open('./plugins/bossInfo.csv', 'r')
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
		session.pause('')
		#continue
		
	session.state[session.current_key] = stripped_arg
	
#指令：请求色图，该指令无参数
@on_command('eroPic', aliases=['色图', '涩图'], permission=GROUP | PRIVATE_FRIEND, only_to_me=True)
async def eroPic(session: CommandSession):
	pic = getEroPic()
	#经URL发送图片
	#coolQ air版本不支持发图片
	await session.send(f'[CQ:image, file={pic}]')
    
#指令：boss作业，查询或者分享作业
#参数：boss信息 作业内容（可选）
#管理员参数：查看当前所有作业，清空作业，删除特定作业
#指令形式：@bot 作业 参数一 参数二
#参数解释
#参数一：boss名字
#	参数二：上传作业内容，空则为查询作业
#参数一：all|全部|所有 （管理员参数）
#	参数二：无，查询当前所有作业
#参数一：del|删除|清除 （管理员参数）
#	参数二：要删除的作业索引，空则为清空所有作业
@on_command('reference', aliases=['作业'], permission=GROUP | PRIVATE_FRIEND, only_to_me=True, shell_like=True)
async def reference(session: CommandSession):
	#检查参数数量
	cmdArgs = session.args['argv']
	
	#没有参数，则退出指令
	if len(cmdArgs) == 0:
		await session.send('boss信息有误，请重新输入')
		return
	
	#有两个参数，先检查第一个参数是否为管理员参数
	#如果是，则执行管理员指令
	#管理员指令有独立出口(return)
	#查看当前所有作业
	if cmdArgs[0] in ['all','全部','所有']:
		if not session.ctx['sender']['role'] in ['owner','admin']:
			await session.send('只有管理员才能查看所有作业哦')
			return
		allRef = []
		refInfo = open('./plugins/bossReference.csv', 'r')
		reader = csv.reader(refInfo)
		for row in reader:
			allRef.append(row)
		#检查是否有作业
		if len(allRef) == 1:
			await session.send('目前还没有任何作业哦')
			return
			
		#删除首行，排序
		del(allRef[0])
		allRef = sorted(allRef)
		
		#按index拆分作业
		reply = '所有作业：'
		for r in range(1,4):
			for n in range(1,6):
				thisIndex = str(5*(r-1)+n)
				thisRefList = [refList for refList in allRef if refList[0]==thisIndex]
				reply = reply + '\n' + str(r) + '阶段' + str(n) + '号作业：'
				if len(thisRefList) == 0:
					reply = reply + '\n这个boss还没有作业哦'
					continue
				for i in thisRefList:
					thisRef = re.sub('\'','',i[2])
					reply = reply + '\n' + i[1] + ':' + thisRef
		await session.send(reply)
		return
		
		
	#如果不是，则为查询或分享作业
	#如果因为输入空格而存在更多的参数，将后面参数合并
	
	#获取boss名字
	bossName = cmdArgs[0]
	share = False
	
	if len(cmdArgs) >= 2:
		reference = str(cmdArgs[1:len(cmdArgs)])
		reference = re.sub('\[|\]', '', reference)
		reference = re.sub(', *', ' ', reference)
		share = True
		
	#将汉字替换为数字
	bossName = re.sub('一', '1', bossName)
	bossName = re.sub('二', '2', bossName)
	bossName = re.sub('三', '3', bossName)
	bossName = re.sub('四', '4', bossName)
	bossName = re.sub('五', '5', bossName)
	bossLocStr = re.findall('[0-9]', bossName)
	
	#boss名字第一次检查，确认有两个数字
	if len(bossLocStr) != 2:
		await session.send('boss信息有误，请重新输入')
		return
	bossLoc = [int(bossLocStr[0]), int(bossLocStr[1])]
	bossIndex = 5*(bossLoc[0]-1)+bossLoc[1]
	
	#boss名字第二次检查，确认阶段数和编号未超出范围
	if bossLoc[0]>3 or bossLoc[0]<1 or bossLoc[1]>5 or bossLoc[1]<1:
		await session.send('boss信息有误，请重新输入')
		return
	
	#如果是查询作业，则打开文件读取
	#可能有多个作业，因此做成list
	#csv每行内容顺序：boss索引，作业编号（行数），作业内容
	ref = []
	if not share:
		refInfo = open('./plugins/bossReference.csv', 'r')
		reader = csv.reader(refInfo)
		for row in reader:
			#避免空白行报错，使用try来读内容
			try:
				if row[0] == str(bossIndex):
					ref.append(row[1]+':'+row[2])
			except:
				continue
				
		#检查是否有作业
		if len(ref) == 0:
			await session.send('这个boss还没有作业哦')
			return
			
		#合并作业
		reply = bossLocStr[0]+'阶段'+bossLocStr[1]+'号作业：'
		for i in ref:
			i = re.sub('\'','',i)
			reply = reply + '\n' + i
		
	#如果是分享作业，则打开文件写入
	if share:
		uploadUser = session.ctx['sender']['card']
		
		#获取当前文件内容行数
		#需要先以read模式打开
		refInfo = open('./plugins/bossReference.csv', 'r')
		lineCnt = sum(1 for line in refInfo)
		refInfo.close()
		
		#重新打开
		refInfo = open('./plugins/bossReference.csv', 'a')
		thisRef = '\n'+str(bossIndex)+','+str(lineCnt)+','+reference+' by '+uploadUser
		refInfo.write(thisRef)
		reply = bossLocStr[0]+'阶段'+bossLocStr[1]+'号作业：'+str(lineCnt)+'添加完成'
		
	try:
		refInfo.close()
	except:
		pass
		
	#根据信息生成回复内容
	await session.send(reply)
	
