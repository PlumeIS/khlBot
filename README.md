# 基于selenium的开黑啦机器人(今KOOK)  
**其最大特点是不需要开黑啦官方的机器人内测权限**  
  
## 注意：实验性仓库，请勿投入于生产环境使用！  
  
### 依赖库的安装  
    pip install selenium
    pip install requests
    pip install tqdm
    pip install shutil
    pip install zipfile
  
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
    
    mf = MessageFetcher(bot, 50)
    ms = MessageSender(bot)
    chat = mf.fetch()
    if chat:
        print(chat)
    ms.sendMessage("Hello World!")
  
来接收以及发送消息  
  
