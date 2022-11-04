import re
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


class Bot:
    def __init__(self, phoneNumber: str, password: str, isUpdateDriver=False):
        self.channel = None
        self.server = None
        self.startTime = datetime.datetime.now()
        self.PhoneNumber = phoneNumber
        self.password = password
        self.isLogging = True
        self.isUpdate = isUpdateDriver

        options = Options()
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1
        })
        options.headless = False
        options.add_argument('log-level=3')
        service = Service(executable_path="./lib/msedgedriver.exe")
        try:
            self.botDriver = webdriver.Edge(options=options, service=service)
        except SessionNotCreatedException:
            if self.isUpdate:
                self.logger("ERROR", "Driver已过期,正在更新")
                from tools.DriverUpdater import updateMSEdgeDriver
                updateMSEdgeDriver()
                self.logger("INFO", "更新完成!")
            self.botDriver = webdriver.Edge(options=options, service=service)
        except WebDriverException:
            if self.isUpdate:
                self.logger("ERROR", "Driver不存在,正在下载")
                from tools.DriverUpdater import updateMSEdgeDriver
                updateMSEdgeDriver()
                self.logger("INFO", "下载完成!")
            self.botDriver = webdriver.Edge(options=options, service=service)

        self.Elements = {
            "SwitchToPhoneNumberAndPasswordElement": '//*[@id="root"]/div/div[4]/div[2]/div[1]/div[2]',
            "PhoneNumberInputElement": '//*[@id="root"]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div/input',
            "PasswordInputElement": '//*[@id="root"]/div/div[4]/div[2]/div[2]/div[2]/input',
            "LoginButtonElement": '//*[@id="root"]/div/div[4]/div[2]/div[3]/button',
            "TempWindowClose": '/html/body/div[3]/div/div/div[3]/button/span',
            "HomeTempWindowClose": '//*[@id="confirmBtn"]',
            "HomeEnterLogin": '//*[@id="btn-quick-start"]',
            "QuitChannelButton": '//*[@id="root"]/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/svg/g/g/g/path',
            "ChannelCheck": '//*[@id="root"]/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[1]/span[1]/span'
        }

        self.isGetServers = False
        self.isGetChannels = False
        self.isSelectServer = False
        self.isSelectChannel = False

    def getXpathElement(self, element: str):
        return self.botDriver.find_element("xpath", self.Elements[element])

    def botLogin(self):
        self.logger("INFO", "Start login")
        self.botDriver.get("https://www.kaiheila.cn/app/login")
        time.sleep(0.5)
        # self.getXpathElement("TempWindowClose").click()
        self.getXpathElement("SwitchToPhoneNumberAndPasswordElement").click()
        self.getXpathElement("PhoneNumberInputElement").send_keys(self.PhoneNumber)
        self.getXpathElement("PasswordInputElement").send_keys(self.password)
        self.getXpathElement("LoginButtonElement").click()
        time.sleep(1)
        try:
            self.getXpathElement("LoginButtonElement")
        except NoSuchElementException:
            while True:
                if self.botDriver.find_elements("class name", "icon-clip.image-button"):
                    time.sleep(0.5)
                    break
            self.logger("INFO", "Login successful")
        else:
            self.logger("ERROR", "Wrong password!")
            raise ValueError("Wrong password!")

    def __botLoginByCookies(self, cookies):
        self.logger("INFO", f"Start login by cookies:{cookies}")
        self.botDriver.get("https://www.kaiheila.cn/app/discover")
        for cookie in cookies:
            cookie["domain"] = "www.kaiheila.cn"
            self.logger("DEBUG", f"add cookie{cookie}")
            self.botDriver.add_cookie(cookie)
        self.botDriver.get("https://www.kaiheila.cn/app/discover")
        time.sleep(0.5)

    def __getCookies(self):
        server = self.server
        channel = self.channel
        self.botDriver.get("https://www.kaiheila.cn/app/discover")
        time.sleep(2)
        cookies = self.botDriver.get_cookies()
        if server is not None:
            self.selectServer(server)
        if channel is not None:
            self.selectChannel(channel)
        return cookies

    def getServers(self):
        self.logger("INFO", "Start get servers")
        self.serverElementList = self.botDriver.find_elements("class name", 'icon-button ')
        self.serverNameList = []
        self.serverNameToElementDirt = {}
        for server in self.serverElementList:
            serverName = re.findall('<div class="guild-name">(.*?)</div>', str(server.get_attribute("data-tip")))
            if not serverName:
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

    def getBotName(self):
        if self.isSelectServer:
            return self.botDriver.find_element("class name", "user-name-text").text
        else:
            return None

    def selectChannel(self, ChannelName: str):
        self.getChannels()
        self.channelNameToElementDirt[ChannelName].click()
        self.channelNameToElementDirt[ChannelName].click()
        try:
            self.getXpathElement("QuitChannelButton")
        except NoSuchElementException:
            pass
        else:
            while True:
                try:
                    self.getXpathElement("ChannelCheck")
                except NoSuchElementException:
                    continue
                else:
                    break
        finally:
            self.isSelectChannel = True
            self.channel = ChannelName
            self.logger("INFO", f"Select ChannelName to {ChannelName}")

    def quitChannel(self):
        self.getXpathElement("QuitChannelButton").click()

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

    def quit(self):
        self.botDriver.quit()
