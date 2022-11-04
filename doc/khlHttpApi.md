# API文档

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
  
    /getServerName
  
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
  
### 捕获消息 /fetchMessage  
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
  
### [API更新日志](https://github.com/PlumeIS/khlBot/blob/main/doc/ApiUpdateLog.md)
