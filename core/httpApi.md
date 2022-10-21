# API文档

## 配置文件  
[khlHttpApi.json](https://github.com/PlumeIS/khlBot/blob/main/config/khlHttpApi.json)  
  
    {
        "host": "localhost", #地址
        "port": 5000  #端口
    }  
  
## 调用  
  
### /getServerName  
方法 GET  
  
输入:  
  
    无  
  
输出:  
  
    {
      "code": 0,
      "msg": "success",
      "data": [...]
    }  
  
| 变量 | 类型 |
| ---- | ---- |
| code | int |
| msg | str |
| data | list[str] |
  
