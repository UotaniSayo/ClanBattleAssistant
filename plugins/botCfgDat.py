#botCfgDat
#存储bot的配置信息


from __future__ import unicode_literals
import pickle
class NekoBot:
    #公会群号
    groupNo = '0'
    #公会成员列表
    clanMbr = []
    #允许普通成员将自己添加进列表
    allowMbrSelfAdd = False
    #公会成员群昵称标签
    mbrTag = '【Mbr】'
    #测试模式
    debugMode = True
    
    def saveCfg(self):
        cfgFile = open('./plugins/nekobot.cfg', 'wb')
        pickle.dump(self, cfgFile)
        cfgFile.close()
        
    def loadCfg():
        try:
            cfgFile = open('./plugins/nekobot.cfg', 'wb')
            newBot = pickle.load(cfgFile)
            cfgFile.close()
            return newBot
        except:
            return False
#临时
