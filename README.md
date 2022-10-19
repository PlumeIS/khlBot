# 基于selenium的开黑啦机器人(今KOOK)  
**其最大特点是不需要开黑啦官方的机器人内测权限**  
  
## 注意：实验性仓库，请勿投入于生产环境使用！  
  
### 依赖库的安装  
    pip install selenium
    pip install requests
    pip install tqdm
    pip install shutil
    pip install zipfile
    pip install bs4
  
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
    from message.GetChatList import ChatList
    
    if __name__ == '__main__':
    bot = ......
    
    cl = ChatList(bot, 50)
    ms = MessageSender(bot)
    chat = cl.getChatList(1)
    if chat:
        print(chat)
    ms.sendMessage("Hello World!")
  
来接收以及发送消息  
  
**注意!!!:请勿在循环获取消息中使用同一机器人调用sendMessage，会引发消息列表从后往前抛出并报错，这是个未修复的BUG（给我整不会了），暂时可以使用两个机器人来代替**  


