from core.khlBotCoreEdge import Bot
from selenium.webdriver.common.keys import Keys


class MessageSender:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.Elements = {
            "sendMessageAreaElement": '//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div[4]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/p'
        }

    def sendMessage(self, message):
        inputArea = self.bot.getDriver().find_element("xpath", self.Elements["sendMessageAreaElement"])
        inputArea.send_keys(message)
        inputArea.send_keys(Keys.ENTER)
        self.bot.logger("INFO", f'Send a message to {self.bot.server}:{self.bot.channel} "{message}"')

