# API文档
## API目录
+ ### [服务器以及频道](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%BB%A5%E5%8F%8A%E9%A2%91%E9%81%93)
  + [获得服务器名列表](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E8%8E%B7%E5%BE%97%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%90%8D%E5%88%97%E8%A1%A8-getservername)
  + [获得频道名列表](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E8%8E%B7%E5%BE%97%E9%A2%91%E9%81%93%E5%90%8D%E5%88%97%E8%A1%A8-getchannelname)
  + [进入服务器](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E8%BF%9B%E5%85%A5%E6%9C%8D%E5%8A%A1%E5%99%A8-selectserver)
  + [进入频道](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E8%BF%9B%E5%85%A5%E9%A2%91%E9%81%93-selectchannel)
+ ### [机器人相关](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%9B%B8%E5%85%B3)
  + [获得机器人名称](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E8%8E%B7%E5%BE%97%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%90%8D%E7%A7%B0-getbotname)
+ ### [服务器成员](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%88%90%E5%91%98)
  + [获得服务器全部成员昵称](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E8%8E%B7%E5%BE%97%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%85%A8%E9%83%A8%E6%88%90%E5%91%98%E6%98%B5%E7%A7%B0-getallmemberinfo)
  + [获得成员资料](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E8%8E%B7%E5%BE%97%E6%88%90%E5%91%98%E4%BF%A1%E6%81%AF-getmemberinfo)
  + [获得全部成员资料](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E8%8E%B7%E5%BE%97%E5%85%A8%E9%83%A8%E6%88%90%E5%91%98%E4%BF%A1%E6%81%AF-getallmemberinfo)
+ ### [消息相关](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E6%B6%88%E6%81%AF%E7%9B%B8%E5%85%B3)
  + [捕获消息](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E6%8D%95%E8%8E%B7%E6%B6%88%E6%81%AF-fetchmessage)
  + [发送文本消息](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E5%8F%91%E9%80%81%E6%96%87%E6%9C%AC%E6%B6%88%E6%81%AF-sendmessage)
  + [发送图片](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E5%8F%91%E9%80%81%E5%9B%BE%E7%89%87-sendimage)
  + [发送At消息](https://github.com/PlumeIS/khlBot/blob/main/doc/khlHttpApi.md#%E5%8F%91%E9%80%81at%E6%B6%88%E6%81%AF-sendat)
### [API更新日志](https://github.com/PlumeIS/khlBot/blob/main/doc/ApiUpdateLog.md)

## 配置文件  
[khlHttpApi.json](https://github.com/PlumeIS/khlBot/blob/main/config/khlHttpApi.json)  
  
    {
        "host": "localhost", #地址
        "port": 5000  #端口
    }  
  
## 调用  

---

## 服务器以及频道

### 获得服务器名列表 /getServerName  
条件:

    无

方法:  

    GET  

输入:  

    无  

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
      "data": [...]
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |
| data | list[str] | 包含服务器名称的列表 |
  
---  
  
### 获得频道名列表 /getChannelName  
条件:  

    /selectServer

方法:  

    GET  

输入:  

    无  

输出 JSON:   

    {
      "code": 0,
      "msg": "success",
      "data": [...]
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |
| data | list[str] | 包含频道名称的列表 |
  
---  
  
### 进入服务器 /selectServer  
条件:  

    无

方法:  

    POST  
  
输入 表单数据:  

    {
     "name": ""
    }

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| name | str | 服务器名称 |

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |

---  

### 进入频道 /selectChannel  
条件:  

    /selectServer

方法:  

    POST  

输入 表单数据:  

    {
     "name": ""
    }

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| name | str | 频道名称 |

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |

---  

## 机器人相关

### 获得机器人名称 /getBotName  
条件:

    /selectServer

方法:  

    GET  

输入:  

    无  

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
      "data": ""
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |
| data | str | 机器人名称 |
  
--- 

## 服务器成员

### 获得服务器全部成员昵称 /getMemberList
条件:

    /selectServer

方法:  

    GET  

输入:  

    无  

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
      "data": []
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |
| data | list[str] | 包含成员昵称的列表 |
  
--- 

### 获得成员资料 /getMemberInfo  
条件:

    /selectServer

方法:  

    GET  

输入:  

    name="name"&profile=false

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| name | str | 成员昵称 |
| profile | bool | 是否获取简介(建议为False,否则增加查询耗时) |
  
输出 JSON:  

    {
      "code": 0,
      "msg": "success",
      "data": {
        "online": True,
        "server": "",
        "nameId": "",
        "name": "",
        "id": "",
        "nick": "",
        "avatar": "",
        "banner": "",
        "profile": "",
        "roles":[],
        "game": {
          "type": "",
          "name"|"game":,
          "time"|"siger"
        }
      }
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |
| data | dict | 信息 |
| online | bool | 是否上线 |
| server | str | 所属服务器 |
| nameId | str | 包含ID的名称(绿毛#0001) |
| name | str | 名称 |
| id | str | ID(不带#号) |
| nick | str | 昵称(在服务器中的名称) |
| avatar | str | 头像(url) |
| banner | str/None | 背景(url或None) |
| profile | str/None | 个人简介(输入profile=false时为None) |
| roles | list[str] | 包含角色名称的列表 |
| game | dict | 正在玩的游戏或听的音乐 |
| type | str | 类型("正在玩游戏"或"正在听音乐") |
| name/game | str | 音乐或游戏名称 |
| time/siger | str | 游戏时长或歌手 |

--- 

### 获得全部成员资料 /getAllMemberInfo  
#### 注意:极其耗时,不建议使用,30人的服务器需要等待10秒左右
条件:

    /selectServer

方法:  

    GET  

输入:  

    profile=false

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| profile | bool | 是否获取简介(建议为False,否则增加查询耗时) |
  
输出 JSON:  

    {
      "code": 0,
      "msg": "success",
      "data": [],
    }

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |
| data | list | 单条内容为/getMemberInfo的data |

--- 

## 消息相关

### 捕获消息 /fetchMessage  
条件:  

    /selectServer
    /selectChannel

方法:  

    GET, POST  

输入:  

    无

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
      "data": [
        {'data':
          {
            'emoji': [
              {
                "view": "",
                "url": ""
              }
            ],
            'image': [
              {
                "url": ""
              }
            ],
            'text': ''
           },
           'sender': '',
           "server": '',
           "channel": '',
           'time': ''
         },
         ...
      ]
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |
| data | dict | 数据 |
| data[data] | dict | 聊天数据 |
| emoji | list | 表情 |
| emoji[view] | str | 表情预览 |
| emoji[url] | str | 表情链接 |
| image | list | 图片 |
| image[url] | str | 图片链接 |
| text | str | 消息文本 |
| sender | str | 发送者 |
| server | str | 服务器 |
| channel | str | 频道 |
| time | str | 时间(%y-%m-%d %H:%M) |
  
---  
  
### 发送文本消息 /sendMessage  
条件:  

    /selectServer
    /selectChannel

方法:  

    POST  

输入 表单数据:  

    {
     "text": ""
    }

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| text | str | 发送文本 |

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |

### 发送图片 /sendImage  
条件:  

    /selectServer
    /selectChannel

方法:  

    POST  

输入 表单数据:  

    {
     "type": "",
     "data": ""
    }

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| type | str | 图片类型,支持:本地路径(path),url(path),base64(base64) |
| data | str | 本地路径,url,base64[str] |

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 |

### 发送At消息 /sendAt  
条件:  

    /selectServer
    /selectChannel

方法:  

    POST  

输入 表单数据:  

    {
     "username": ""
    }

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| username | str | 用户名 |

输出 JSON:  

    {
      "code": 0,
      "msg": "success",
    }  

| 变量 | 类型 | 描述 |
| ---- | ---- | ---- |
| code | int | 状态码 |
| msg | str | 状态 | 
