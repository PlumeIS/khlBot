import re
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class Bot:
    def __init__(self, phoneNumber: str, password: str):
        self.startTime = datetime.datetime.now()
        self.PhoneNumber = phoneNumber
        self.password = password
        options = Options()
        options.headless = False
        service = Service(executable_path="../lib/chromedriver.exe")
        self.botDriver = webdriver.Chrome(options=options, service=service)

        self.Elements = {
            "SwitchToPhoneNumberAndPasswordElement": '//*[@id="root"]/div/div[2]/div[1]/div[2]/div[1]/div[1]',
            "PhoneNumberInputElement": '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[3]/div/input',
            "PasswordInputElement": '//*[@id="root"]/div/div[2]/div[2]/div[2]/input',
            "LoginButtonElement": '//*[@id="root"]/div/div[2]/div[3]/button',
        }

        self.isGetServers = False
        self.isGetChannels = False
        self.isSelectServer = False
        self.isSelectChannel = False

        self.isLogging = True

    def getXpathElement(self, element: str):
        return self.botDriver.find_element("xpath", self.Elements[element])

    def botLogin(self):
        self.logger("INFO", "Start login")
        self.botDriver.get("https://www.kaiheila.cn/app/login")
        self.getXpathElement("SwitchToPhoneNumberAndPasswordElement").click()
        self.getXpathElement("PhoneNumberInputElement").send_keys(self.PhoneNumber)
        self.getXpathElement("PasswordInputElement").send_keys(self.password)
        self.getXpathElement("LoginButtonElement").click()
        time.sleep(1)
        try:
            self.getXpathElement("LoginButtonElement")
        except NoSuchElementException:
            time.sleep(3)
            self.logger("INFO", "Login successful")
        else:
            self.logger("ERROR", "Wrong password!")
            raise ValueError("Wrong password!")

    def getServers(self):
        self.logger("INFO", "Start get servers")
        self.serverElementList = self.botDriver.find_elements("class name", 'icon-button ')
        self.serverNameList = []
        self.serverNameToElementDirt = {}
        for server in self.serverElementList:
            serverName = re.findall('<div class="guild-name">(.*?)</div>', server.get_attribute("data-tip"))
            if serverName == []:
                serverName = [server.get_attribute("data-tip")]
            self.serverNameToElementDirt[serverName[0]] = server
            self.serverNameList.append(serverName[0])
        self.isGetServers = True
        return self.serverNameList

    def getChannels(self):
        self.logger("INFO", "Start get channels")
        if self.isSelectServer:
            self.channelElementList = self.botDriver.find_elements("class name", 'channel-info')
            self.channelNameList = []
            self.channelNameToElementDirt = {}
            for channel in self.channelElementList:
                channelHtmlText = re.findall('title="(.*?)"', channel.get_attribute("innerHTML"))[0]
                self.channelNameToElementDirt[channelHtmlText] = channel
                self.channelNameList.append(channelHtmlText)
        else:
            return
        self.isGetChannels = True
        return self.channelNameList

    def selectServer(self, serverName: str):
        self.getServers()
        self.serverNameToElementDirt[serverName].click()
        self.isSelectServer = True
        self.server = serverName
        time.sleep(1)
        self.logger("INFO", f"Select server to {serverName}")

    def selectChannel(self, ChannelName: str):
        self.getChannels()
        self.channelNameToElementDirt[ChannelName].click()
        self.channelNameToElementDirt[ChannelName].click()
        self.isSelectChannel = True
        self.channel = ChannelName
        self.logger("INFO", f"Select ChannelName to {ChannelName}")

    def setLogger(self, switch: bool):
        if switch:
            self.logger("INFO", "Logger on")
        else:
            self.logger("INFO", "Logger off")
        self.isLogging = switch

    def logger(self, level, message):
        if self.isLogging:
            print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}][{level}] {message}')

    def getDriver(self):
        return self.botDriver
