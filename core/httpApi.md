# API文档

## 配置文件  
[khlHttpApi.json](https://github.com/PlumeIS/khlBot/blob/main/config/khlHttpApi.json)  
  
    {
        "host": "localhost", #地址
        "port": 5000  #端口
    }  
  
## 调用  
  
### /getServerName  
方法:  
  
    GET  
  
输入:  
  
    无  
  
输出:  
  
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
  
### /getChannelName  
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
  
### /selectServer  
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
  
### /selectChannel  
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
  
### /fetchMessage  
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
| time | str | 时间 |
  
### /sendMessage  
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
  
