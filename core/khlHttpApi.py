import json
import base64
from flask import Flask, request, jsonify
from tools.AutoLogin import AutoLogin
from khlBotCoreEdge import Bot
from message.MessageSender import MessageSender
from message.MessageFetcher import MessageFetcher

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

accountConfig = AutoLogin()
if not accountConfig:
    phone = input("账号:")
    password = input("密码:")
else:
    phone = accountConfig["account"]
    password = accountConfig["password"]

bot = Bot(phone, password)
bot.botLogin()

messageSender = None
messageFetcher = None


@app.route("/getServerName", methods=["GET"])
def getServer():
    return jsonify({"code": 0, "msg": "success", "data": bot.getServers()})


@app.route("/getChannelName", methods=["GET"])
def getChannel():
    if bot.isSelectServer:
        return jsonify({"code": 0, "msg": "success", "data": bot.getServers()})
    else:
        return jsonify({"code": 1, "msg": "Not Select Server!"})


@app.route("/selectServer", methods=["POST"])
def selectServer():
    if request.form.get("name") in bot.getServers():
        bot.selectServer(request.form.get("name"))
        return jsonify({"code": 0, "msg": "success"})
    else:
        return jsonify({"code": 1, "msg": "Not Server!"})


@app.route("/selectChannel", methods=["POST"])
def selectChannel():
    global messageSender
    global messageFetcher
    if bot.isSelectServer and request.form.get("name") in bot.getChannels():
        bot.selectChannel(request.form.get("name"))
        messageSender = MessageSender(bot)
        messageFetcher = MessageFetcher(bot)
        return jsonify({"code": 0, "msg": "success"})
    else:
        return jsonify({"code": 0, "msg": "Not Select Server or Not Channel Name!"})


@app.route("/fetchMessage", methods=["GET", "POST"])
def fetchMessage():
    global messageFetcher
    if bot.isSelectServer and bot.isSelectChannel:
        return jsonify({"code": 0, "msg": "success", "data": messageFetcher.fetch()})
    else:
        return jsonify({"code": 1, "msg": "Not Select Server or Channel!"})


@app.route("/sendMessage", methods=["POST"])
def sendMessage():
    global messageSender
    if bot.isSelectServer and bot.isSelectChannel:
        messageSender.sendMessage(request.form.get("text"))
        return jsonify({"code": 0, "msg": "success"})
    else:
        return jsonify({"code": 1, "msg": "Not Select Server or Channel!"})


@app.route("/sendImage", methods=["POST"])
def sendImage():
    global messageSender
    if bot.isSelectServer and bot.isSelectChannel:
        imgType = request.form.get("type")
        imgdata = request.form.get("data")
        if imgType == "base64":
            with open("./temp.png", "wb") as img:
                img.write(base64.b64decode(imgdata.encode("utf-8")))
            messageSender.sendImage(path="./temp.png")
        elif imgType == "path":
            messageSender.sendImage(path=imgdata)
        elif imgType == "url":
            messageSender.sendImage(url=imgdata)
        else:
            return jsonify({"code": 1, "msg": "Only support type: base64, path, url"})
        return jsonify({"code": 0, "msg": "success"})
    else:
        return jsonify({"code": 1, "msg": "Not Select Server or Channel!"})


if __name__ == '__main__':
    with open("../config/khlHttpApi.json", "r") as configFile:
        config = json.loads(configFile.read())

    app.run(port=config["port"],
            host=config["host"])
