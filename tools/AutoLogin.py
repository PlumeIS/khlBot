import os
import json


def AutoLogin():
    if os.path.isfile("./config/account/autoLogin.json"):
        with open("./config/account/autoLogin.json", 'r') as configFile:
            config = json.loads(configFile.read())
            if config["account"] == "":
                return None
            return config
    else:
        with open("./config/account/autoLogin.json", 'w') as configFile:
            configFile.write("""
{
  "account": "",
  "password": ""
}""")
            return None
