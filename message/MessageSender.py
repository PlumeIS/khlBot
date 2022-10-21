import time

import os
import win32clipboard
from PIL import Image
from io import BytesIO
from lib.MainDownloader import ordinaryDownload, getFileName
from core.khlBotCoreEdge import Bot
from selenium.webdriver.common.keys import Keys


class MessageSender:
    def __init__(self, bot: Bot):
        self.bot = bot

    def sendMessage(self, message):
        for i in message.split("\n"):
            inputArea = self.bot.getDriver().find_element("class name", "slate-editor.theme-scroll-bar").find_element(
                "tag name", "p")
            inputArea.send_keys(i)
            inputArea.send_keys(Keys.ENTER)
        self.bot.logger("INFO", f'Send a message to {self.bot.server}:{self.bot.channel} "{message}"')

    def sendImage(self, path=None, url=None):
        if url:
            filename = getFileName(url)
            if filename:
                ordinaryDownload(url, f"./{filename}")
                path = f"./{filename}"
            else:
                ordinaryDownload(url, f"./temp.png")
                path = f"./temp.png"
            self.copyImageToClipboard(path)
            inputArea = self.bot.getDriver().find_element("class name", "slate-editor.theme-scroll-bar").find_element(
                "tag name", "p")
            inputArea.send_keys(Keys.CONTROL, "v")
            self.bot.getDriver().find_element("class name", "chuanyu-button.size-md.type-appprimary").click()
            self.bot.logger("INFO", f'Send a message to {self.bot.server}:{self.bot.channel} "{path}"')
            os.remove(path)
        elif path:
            self.copyImageToClipboard(path)
            inputArea = self.bot.getDriver().find_element("class name", "slate-editor.theme-scroll-bar").find_element(
                "tag name", "p")
            inputArea.send_keys(Keys.CONTROL, "v")
            self.bot.getDriver().find_element("class name", "chuanyu-button.size-md.type-appprimary").click()
            self.bot.logger("INFO", f'Send a message to {self.bot.server}:{self.bot.channel} "{path}"')

    @staticmethod
    def copyImageToClipboard(path):
        image = Image.open(path)
        output = BytesIO()
        image.save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()


