import json
import base64
import atexit
from flask import Flask, request, jsonify
from tools.AutoLogin import AutoLogin
from core.khlBotCoreEdge import Bot
from message.MessageSender import MessageSender
from message.MessageFetcher import MessageFetcher

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

messageSender: MessageSender
messageFetcher: MessageFetcher

codes = {
    0: "Successful!",
    1: "Missing parameter!",
    2: "Wrong value!",
    3: "Flow operation of missing process!",
    4: "Internal error!",
    5: "Io error!"
}

version = "1.3.9"


class Respond(dict):
    def __init__(self, code=None, msg=None, data=None):
        super().__init__()
        self["code"] = 0
        self["msg"] = "Successful!"
        self["data"] = None
        if code:
            self["code"] = code
        if msg:
            self["msg"] = msg
        if data:
            self["data"] = data

    def setCode(self, code):
        self["code"] = code
        return self

    def setMsg(self, msg):
        self["msg"] = msg
        return self

    def setData(self, data):
        self["data"] = data
        return self


@app.route("/about", methods=["GET", "POST"])
def about():
    return jsonify(Respond(data={"version": version}))


@app.route("/getServerName", methods=["GET"])
def getServer():
    respond = Respond()
    try:
        data = bot.getServers()
    except Exception as err:
        respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
        return jsonify(respond)
    else:
        return jsonify(respond.setData(data))


@app.route("/getChannelName", methods=["GET"])
def getChannel():
    respond = Respond()
    if bot.isSelectServer:
        try:
            data = bot.getChannels()
        except Exception as err:
            respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
            return jsonify(respond)
        else:
            return jsonify(respond.setData(data))
    else:
        return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))


@app.route("/selectServer", methods=["POST"])
def selectServer():
    global messageSender
    respond = Respond()
    name = request.form.get("name")
    if name:
        if name in bot.getServers():
            try:
                bot.selectServer(name)
                messageSender = MessageSender(bot)
            except Exception as err:
                respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
                return jsonify(respond)
            else:
                return jsonify(respond)
        else:
            jsonify(respond.setCode(2).setMsg(codes[2] + f'No Server! "{name}"'))
    else:
        return jsonify(respond.setCode(1).setCode(codes[2] + '"name"'))


@app.route("/selectChannel", methods=["POST"])
def selectChannel():
    global messageFetcher
    respond = Respond()
    name = request.form.get("name")
    if name:
        if bot.isSelectServer:
            if name in bot.getChannels():
                try:
                    bot.selectChannel(name)
                    messageFetcher = MessageSender(bot)
                except Exception as err:
                    respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
                    return jsonify(respond)
                else:
                    return jsonify(respond)
            else:
                jsonify(respond.setCode(2).setMsg(codes[2] + f'No Channel! "{name}"'))
        else:
            return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))
    else:
        return jsonify(respond.setCode(1).setCode(codes[2] + '"name"'))


@app.route("/getBotName", methods=["GET"])
def getBotName():
    respond = Respond()
    if bot.isSelectServer:
        try:
            data = bot.getBotName()
        except Exception as err:
            respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
            return jsonify(respond)
        else:
            return jsonify(respond.setData(data))
    else:
        return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))


@app.route("/getMemberList", methods=["GET"])
def getMemberList():
    respond = Respond()
    if bot.isSelectServer:
        try:
            data = bot.getUsers()
        except Exception as err:
            respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
            return jsonify(respond)
        else:
            return jsonify(respond.setData(data))
    else:
        return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))


@app.route("/getAllMemberInfo", methods=["GET"])
def getAllMemberInfo():
    respond = Respond()
    isProfile = request.form.get("profile", "None")
    if not isProfile == "None":
        if bot.isSelectServer:
            try:
                data = bot.getAllUserInfo(isProfile)
            except Exception as err:
                respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
                return jsonify(respond)
            else:
                return jsonify(respond.setData(data))
        else:
            return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))
    else:
        return jsonify(respond.setCode(1).setCode(codes[2] + '"profile"'))


@app.route("/getMemberInfo", methods=["GET"])
def getMemberInfo():
    respond = Respond()
    name = request.form.get("name")
    isProfile = request.form.get("profile", "None")
    if name:
        if not isProfile == "None":
            if bot.isSelectServer:
                try:
                    data = bot.getUserInfo(name, isProfile)
                except Exception as err:
                    respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
                    return jsonify(respond)
                else:
                    return jsonify(respond.setData(data))
            else:
                return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))
        else:
            return jsonify(respond.setCode(1).setCode(codes[2] + '"profile"'))
    else:
        return jsonify(respond.setCode(1).setCode(codes[2] + '"name"'))


@app.route("/fetchMessage", methods=["GET", "POST"])
def fetchMessage():
    global messageFetcher
    respond = Respond()
    if bot.isSelectServer:
        if bot.isSelectChannel:
            try:
                data = messageFetcher.fetch()
            except Exception as err:
                respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
                return jsonify(respond)
            else:
                return jsonify(respond.setData(data))
        else:
            return jsonify(respond.setCode(3).setMsg(codes[3] + " Not channel selected!"))
    else:
        return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))


@app.route("/sendMessage", methods=["POST"])
def sendMessage():
    global messageSender
    respond = Respond()
    if bot.isSelectServer:
        if bot.isSelectChannel:
            try:
                messageSender.sendMessage(request.form.get("text"))
            except Exception as err:
                respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
                return jsonify(respond)
            return jsonify(respond)
        else:
            return jsonify(respond.setCode(3).setMsg(codes[3] + " Not channel selected!"))
    else:
        return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))


@app.route("/sendImage", methods=["POST"])
def sendImage():
    global messageSender
    respond = Respond()
    if bot.isSelectServer:
        if bot.isSelectChannel:
            try:
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
                    return respond.setCode(1).setMsg(codes[1] + "Only support type: base64, path, url")
            except Exception as err:
                respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
                return jsonify(respond)
            else:
                return jsonify(respond)
        else:
            return jsonify(respond.setCode(3).setMsg(codes[3] + " Not channel selected!"))
    else:
        return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))


@app.route("/sendAt", methods=["POST"])
def sendAt():
    global messageSender
    respond = Respond()
    if bot.isSelectServer:
        if bot.isSelectChannel:
            try:
                messageSender.sendAt(request.form.get("username"))
            except Exception as err:
                respond.setCode(4).setMsg(codes[4] + f'({err})[{err.__traceback__.tb_frame.f_globals["__file__"]}:{err.__traceback__.tb_lineno}]')
                return jsonify(respond)
            else:
                return jsonify(respond)
        else:
            return jsonify(respond.setCode(3).setMsg(codes[3] + " Not channel selected!"))
    else:
        return jsonify(respond.setCode(3).setMsg(codes[3] + " Not server selected!"))


if __name__ == '__main__':
    accountConfig = AutoLogin()
    if not accountConfig:
        phone = input("账号:")
        password = input("密码:")
    else:
        phone = accountConfig["account"]
        password = accountConfig["password"]

    bot = Bot(phone, password, True)
    bot.botLogin()
    atexit.register(bot.quit)

    with open("./config/khlHttpApi.json", "r") as configFile:
        config = json.loads(configFile.read())

    app.run(port=config["port"],
            host=config["host"])
