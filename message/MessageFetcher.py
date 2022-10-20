from lib import ConversionDate
from core.khlBotCoreEdge import Bot
from selenium.common.exceptions import *


class MessageFetcher:
    def __init__(self, bot: Bot, filters=None):
        self.bot = bot
        self.filters = filters
        self.messageCount = len(self.bot.getDriver().find_elements("class name", "text-message-item"))

    def getAllNewCount(self, messageElements):
        lastCount = self.messageCount
        self.messageCount = len(messageElements)

        if self.messageCount >= lastCount:
            return self.messageCount - lastCount
        else:
            return (self.messageCount - 100) + (200 - lastCount)

    def fetch(self):
        allMessages = self.bot.getDriver().find_elements("class name", "text-message-item")
        readCount = self.getAllNewCount(allMessages)
        headInfos = {}

        while True:
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
                allMessages = self.bot.getDriver().find_elements("class name", "text-message-item")
            else:
                break

        messageData = []

        if readCount == 0:
            return []
        for message in allMessages[-readCount:]:
            sender, date = headInfos[message.get_attribute("data-gather-id")]

            if sender in self.filters:
                continue

            smallTime = message.find_elements("class name", "message-small-time")
            if smallTime:
                date = " ".join(date.split(" ")[:2]) + f' {smallTime[0].get_attribute("innerHTML")}'
                sendTime = ConversionDate.ConversionDate(date)
            else:
                sendTime = ConversionDate.ConversionDate(date)

            data = {"text": [], "emoji": [], "image": []}
            try:
                chatData = message.find_element("class name", "markdown-preview")
            except NoSuchElementException:
                img = message.find_element("class name", "image-type-content")
                image = img.find_element("tag name", "img")
                data["image"].append({image.get_attribute("src")})
            else:
                for i in chatData.find_elements("tag name", "span"):
                    className = i.get_attribute("class")
                    if className == "emoji-wrapper":
                        emoji = i.find_element("tag name", "img")
                        data["emoji"].append({"id": emoji.get_attribute("alt"), "url": emoji.get_attribute("src")})
                    elif className == "image-type-content":
                        image = i.find_element("tag name", "img")
                        data["image"].append({image.get_attribute("src")})
                    else:
                        if i.find_elements("tag name", "img"):
                            emoji = i.find_element("tag name", "img")
                            data["emoji"].append(
                                {"view": emoji.get_attribute("alt"), "url": emoji.get_attribute("src")})
                data["text"] = chatData.text
            messageData.append({"sender": sender, "time": sendTime, "data": data})
        return messageData
