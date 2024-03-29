from lib import ConversionDate
from core.khlBotCoreEdge import Bot
from selenium.common.exceptions import *


class MessageFetcher:
    def __init__(self, bot: Bot, filters=None):
        if not filters:
            filters = []
        self.bot = bot
        self.filters = filters
        self.messageCount = len(self.bot.getDriver().find_elements("class name", "text-message-item"))
        self.errorCounter = 0
        self.maxErrorCount = 20

    def getAllNewCount(self, messageElements):
        lastCount = self.messageCount
        self.messageCount = len(messageElements)

        if self.messageCount >= lastCount:
            return self.messageCount - lastCount
        else:
            return (self.messageCount - 100) + (200 - lastCount)

    def getHeadInfos(self, readCount):
        errorCounter = 0
        while errorCounter < self.maxErrorCount * 2:
            allMessages = self.bot.getDriver().find_elements("class name", "text-message-item")
            headInfos = {}
            try:
                for index, message in enumerate(allMessages[::-1]):
                    if "is-group" not in message.get_attribute("class"):
                        headInfos[message.get_attribute("data-gather-id")] = (
                            message.find_element("class name", "username").text,
                            message.find_element("class name", "msg-time").text
                        )
                        if index >= readCount:
                            break
            except StaleElementReferenceException:
                errorCounter += 1
                pass
            else:
                return headInfos
        else:
            raise StaleElementReferenceException

    @staticmethod
    def getChatData(message):
        data = {"text": [], "emoji": [], "image": []}
        textRetry = True
        while textRetry:
            try:
                textRetry = False
                chatData = message.find_element("class name", "markdown-preview")
            except NoSuchElementException:
                try:
                    img = message.find_element("class name", "image-type-content")
                    image = img.find_element("tag name", "img")
                    data["image"].append({image.get_attribute("src")})
                except NoSuchElementException:
                    textRetry = True
            else:

                for i in chatData.find_elements("tag name", "span"):
                    className = i.get_attribute("class")
                    if className == "emoji-wrapper":
                        emoji = i.find_element("tag name", "img")
                        data["emoji"].append({"alt": emoji.get_attribute("alt"), "url": emoji.get_attribute("src")})
                    elif className == "image-type-content":
                        image = i.find_element("tag name", "img")
                        data["image"].append(image.get_attribute("src"))
                    else:
                        if i.find_elements("tag name", "img"):
                            emoji = i.find_element("tag name", "img")
                            data["emoji"].append(
                                {"alt": emoji.get_attribute("alt"), "url": emoji.get_attribute("src")})
                data["text"] = chatData.text
        return data

    def fetch(self):
        allMessages = self.bot.getDriver().find_elements("class name", "text-message-item")
        readCount = self.getAllNewCount(allMessages)
        headInfos = self.getHeadInfos(readCount)

        messageData = []

        if readCount == 0:
            return []

        retry = True
        stopFlag = False
        while retry:
            for message in allMessages[-readCount:]:
                if stopFlag:
                    break
                while self.errorCounter < self.maxErrorCount:
                    try:
                        sender, date = headInfos[message.get_attribute("data-gather-id")]
                        retry = False
                        break
                    except KeyError:
                        self.errorCounter += 1
                        headInfos = self.getHeadInfos(readCount)
                    except StaleElementReferenceException:
                        allMessages = self.bot.getDriver().find_elements("class name", "text-message-item")
                        stopFlag = True
                        continue
                else:
                    sender, date = ("Unknown", "今天 上午 8:00")
                self.errorCounter += 0

                if sender in self.filters:
                    continue

                smallTime = message.find_elements("class name", "message-small-time")
                if smallTime:
                    date = " ".join(date.split(" ")[:2]) + f' {smallTime[0].get_attribute("innerHTML")}'
                    sendTime = ConversionDate.ConversionDate(date)
                else:
                    sendTime = ConversionDate.ConversionDate(date)

                data = self.getChatData(message)
                messageData.append(
                    {"sender": sender, "server": self.bot.server, "channel": self.bot.channel, "time": sendTime.strftime("%y-%m-%d %H:%M"), "data": data})
        return messageData
