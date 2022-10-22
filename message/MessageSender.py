import os
import time
import win32clipboard
from PIL import Image
from io import BytesIO
from core.khlBotCoreEdge import Bot
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from lib.MainDownloader import ordinaryDownload, getFileName


class MessageSender:
    def __init__(self, bot: Bot):
        self.bot = bot

    def sendAt(self, username):
        try:
            inputArea = self.bot.getDriver().find_element("class name", "slate-editor.theme-scroll-bar").find_element(
                "tag name", "p")
        except NoSuchElementException:
            raise ValueError("Can't find message input element!")
        inputArea.send_keys("@")
        time.sleep(0.1)
        inputArea.send_keys(username)
        inputArea.send_keys(Keys.ENTER)
        inputArea.send_keys(Keys.ENTER)

    def sendMessage(self, message):
        try:
            inputArea = self.bot.getDriver().find_element("class name", "slate-editor.theme-scroll-bar").find_element(
                "tag name", "p")
        except NoSuchElementException:
            raise ValueError("Can't find message input element!")
        self.copyToClipboard(message)
        inputArea.send_keys(Keys.CONTROL, "v")
        inputArea.send_keys(Keys.ENTER)
        self.clearClipboard()
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
            try:
                inputArea = self.bot.getDriver().find_element("class name", "slate-editor.theme-scroll-bar").find_element(
                    "tag name", "p")
            except NoSuchElementException:
                raise ValueError("Can't find message input element!")
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
    def copyToClipboard(text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
        win32clipboard.CloseClipboard()

    @staticmethod
    def clearClipboard():
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()

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
