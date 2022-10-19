import time
from bs4 import BeautifulSoup
from lib import ConversionDate
from core.khlBotCoreEdge import Bot


class ChatList:
    def __init__(self, bot: Bot, refreshTick, filters=None):
        self.fetchLength = -1
        if not filters:
            self.filters = []
        else:
            self.filters = filters
        self.refreshTick = refreshTick
        self.bot = bot
        self.createDate = bot.startTime
        self.endID = self.initID()
        self.FetchCounter = 0

    def initID(self):
        if self.bot.isSelectServer and self.bot.isSelectChannel:
            soup = BeautifulSoup(self.bot.getDriver().page_source, "html.parser")
            return soup.find_all(class_="text-message-item")[-1]["id"]

    def safeRefresh(self):
        if self.FetchCounter > self.refreshTick:
            self.bot.getDriver().refresh()
            self.bot.botDriver.switch_to.alert.accept()
            while True:
                if self.bot.getDriver().find_elements("class name", "icon-clip.image-button"):
                    time.sleep(0.5)
                    break
            self.FetchCounter = 0

    def refresh(self):
        self.bot.getDriver().refresh()
        while True:
            if self.bot.getDriver().find_elements("class name", "icon-clip.image-button"):
                time.sleep(0.5)
                break
        self.FetchCounter = 0

    def getChatList(self, count):
        self.safeRefresh()
        soup = BeautifulSoup(self.bot.getDriver().page_source, "html.parser")
        for s in soup('style'):
            s.extract()
        for s in soup('script'):
            s.extract()
        allChatList = soup.find_all(class_="text-message-item")
        canFetchIDList = []
        infos = {}

        for ele in allChatList[::-1]:
            if "is-group" not in ele["class"]:
                infos[ele["data-gather-id"]] = (ele.find_next(class_="username").text, ele.find_next(class_="msg-time").text)
        allList = []
        # for ele in allChatList[::-1]:
        #     allList.append(ele["id"])
        # print(allList)
        # print(allList[0] == self.endID)

        for ele in allChatList[::-1]:
            # print(ele["id"], self.endID)
            if ele["id"] == self.endID:
                break
            else:
                canFetchIDList.append(ele["id"])

        canFetchIDList = list(reversed(canFetchIDList))
        self.fetchLength = len(canFetchIDList)
        messages = []
        try:
            for messageItemID in canFetchIDList[:count]:
                self.endID = messageItemID
                ele = soup.find(id=messageItemID)

                sender, date = infos[ele["data-gather-id"]]

                if sender in self.filters:
                    self.FetchCounter += 1
                    continue

                smallTime = ele.find(class_="message-small-time")
                if smallTime:
                    date = " ".join(date.split(" ")[:2]) + f" {smallTime.text}"
                    sendTime = ConversionDate.ConversionDate(date)
                else:
                    try:
                        sendTime = ConversionDate.ConversionDate(date)
                    except ValueError:
                        self.refresh()
                        self.initID()
                        return []

                chatData = ele.find_next(class_="content")
                data = {"text": [], "emoji": [], "image": []}
                for i in chatData("span"):
                    try:
                        i["class"]
                    except KeyError:
                        if i.img:
                            data["emoji"].append({"views": i.img["alt"], "url": i.img["src"]})
                data["text"] = chatData.text

                # for i in chatData("div"):
                #     if "sizeable-image-wrapper" in i["class"]:
                #         data["image"].append(i.img["src"])

                messages.append({"sender": sender, "time": sendTime, "data": data, "id": messageItemID})
                # print(messageItemID)
                self.FetchCounter += 1
            return messages
        except IndexError:
            return messages
