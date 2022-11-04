# API文档

### [API更新日志](https://github.com/PlumeIS/khlBot/blob/main/doc/ApiUpdateLog.md)

## 配置文件  
[khlHttpApi.json](https://github.com/PlumeIS/khlBot/blob/main/config/khlHttpApi.json)  
  
    {
        "host": "localhost", #地址
        "port": 5000  #端口
    }  
  
## 调用  

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

### 获得服务器全部成员昵称 /getAllMemberInfo  
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

### 获得成员信息 /getMemberInfo  
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

### 获得全部成员信息 /getAllMemberInfo  
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
