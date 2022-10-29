# 基于selenium的开黑啦机器人(今KOOK)  
**其最大特点是不需要开黑啦官方的机器人内测权限**  
  
## 注意：实验性仓库，请勿投入于生产环境使用！ 
  
### TODO  
+ 将会更新http api 交互以减少机器人重启时间 **已完成**

## 使用API与机器人交互  
  
安装依赖库后,启动:  
  
    start.bat  
  
### [API文档](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md)  
  
---  
  
  
### 依赖库的安装  
必要依赖库:  
  
    pip install selenium
    pip install flask
  
以自动更新driver的方式启动机器人时(Bot(isUpdateDriver=True),仅Edge)，需要追加以下依赖库:  
  
    pip install requests
    pip install zipfile
    pip install shutil
    pip install tqdm
  
### 机器人的登录 
    from core.khlBotCoreEdge import Bot
    
    if __name__ == '__main__':
    bot = Bot("账号", "密码")
    bot.botLogin()
    bot.selectServer('服务器名')
    bot.selectChannel("频道名")
  
#### 服务器以及频道名称的获取 
    print(bot.getServers())
    print(bot.getChannels())  
将会返回包含字符串的列表  
  
### 关于消息的处理  
可以通过  
  
    from message.MessageSender import MessageSender
    from message.MessageFetcher import MessageFetcher
    
    if __name__ == '__main__':
    bot = ......
    
    mf = MessageFetcher(bot)
    ms = MessageSender(bot)
    chat = mf.fetch()
    if chat:
        print(chat)
    ms.sendMessage("Hello World!")
  
来接收以及发送消息  
  
