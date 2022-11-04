import re
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
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

    def waitElement(self, method, value, timeout, interval):
        t = time.time()
        while True:
            try:
                self.botDriver.find_element(method, value)
            except NoSuchElementException:
                pass
            else:
                return self.botDriver.find_element(method, value)
            if time.time() - t > timeout:
                raise TimeoutException(f"Can't not wait element {value} by {method}")
            time.sleep(interval)

    def waitElementByElement(self, element, method, value, timeout, interval):
        t = time.time()
        while True:
            try:
                element.find_element(method, value)
            except NoSuchElementException:
                pass
            else:
                return self.botDriver.find_element(method, value)
            if time.time() - t > timeout:
                raise TimeoutException(f"Can't not wait element {value} by {method}")
            time.sleep(interval)

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
            self.waitElement("class name", "icon-clip.image-button", 1000, 0.5)
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

    def getUsers(self):
        if self.isSelectServer:
            userNames = []
            users = self.botDriver.find_elements("class name", "user-item")
            for i in users:
                try:
                    userNames.append(i.find_element("class name", "user-name-text").text)
                except NoSuchElementException:
                    continue
            return userNames
        else:
            return []

    def getAllUserInfo(self, isReadProfile):
        if self.isSelectServer:
            users = self.botDriver.find_elements("class name", "user-item")
            userInfos = []
            for i in users:
                try:
                    self.botDriver.execute_script("arguments[0].scrollIntoView(false);", i)
                    self.botDriver.execute_script("arguments[0].scrollIntoView();", i)
                    i.find_element("class name", "user-name-text")
                    online = False if "offline" in i.get_attribute("class") else True
                    i.click()
                    try:
                        self.waitElement("class name", "user-info-card-content", 5, 0)
                    except TimeoutException:
                        return None
                    nameCard = self.botDriver.find_element("class name", "user-basic-content")
                    try:
                        userNameIdText = nameCard.find_element("class name", "user-name")
                    except NoSuchElementException:
                        userName = nameCard.find_element("class name", "name").text
                        userId = nameCard.find_element("class name", "user-id").text.replace("#", "")
                        userNameId = userName + "#" + userId
                        userNick = userName
                    else:
                        userName = userNameIdText.find_element("class name", "name").text
                        userId = userNameIdText.find_element("class name", "user-id").text.replace("#", "")
                        userNameId = userName + "#" + userId
                        userNick = nameCard.find_element("class name", "name").text

                    roles = []
                    roleBox = self.botDriver.find_elements("class name", "role-name")
                    for j in roleBox:
                        roles.append(j.text)

                    userGaming = {}
                    try:
                        gamingBox = self.botDriver.find_element("class name", "user-game-panel")
                    except NoSuchElementException:
                        pass
                    else:
                        userGamingType = gamingBox.find_element("class name", "title").text
                        userGaming["type"] = userGamingType
                        if userGamingType == "正在玩游戏":
                            userGaming["game"] = gamingBox.find_element("class name", "game-name").text
                            userGaming["time"] = gamingBox.find_element("class name", "game-time").text
                        else:
                            userGaming["name"] = gamingBox.find_element("class name", "music-name").text
                            userGaming["siger"] = gamingBox.find_element("class name", "music-siger").text
                            userGamingIcon = gamingBox.find_element("class name", "game-icon").get_attribute("style")
                            if userGamingIcon:
                                userGaming["icon"] = re.findall('url[(]"(.*?)"[)]', userGamingIcon)[0]
                            else:
                                userGaming["icon"] = None

                    try:
                        userBannerImg = self.botDriver.find_element("class name", "user-banner.has-banner")
                        userAvatarStyle = userBannerImg.get_attribute("style")
                        userBanner = re.findall('url[(]"(.*?)"[)]', userAvatarStyle)[0]
                    except NoSuchElementException:
                        userBanner = None

                    userAvatarBox = self.botDriver.find_element("class name", "user-avatar-img")
                    userAvatarImg = userAvatarBox.find_element("class name", "kook-avatar-picture-static")
                    userAvatarStyle = userAvatarImg.get_attribute("style")
                    userAvatar = re.findall('url[(]"(.*?)/icon"[)]', userAvatarStyle)[0]
                    if isReadProfile:
                        userAvatarBox.click()
                        profile = self.waitElement("class name", "textarea-box", 1, 0).text
                        self.botDriver.find_element("tag name", "body").send_keys(Keys.ESCAPE)
                    else:
                        profile = None
                    userInfos.append({"online": online, "nameId": userNameId, "name": userName, "id": userId, "nick": userNick, "avatar": userAvatar,
                                      "banner": userBanner, "profile": profile, "game": userGaming})
                except NoSuchElementException:
                    continue
            self.botDriver.find_element("tag name", "body").send_keys(Keys.ESCAPE)
            return userInfos
        return None

    def getUserInfo(self, nickName, isReadProfile):
        if self.isSelectServer:
            users = self.botDriver.find_elements("class name", "user-item")
            for i in users:
                try:
                    self.botDriver.execute_script("arguments[0].scrollIntoView(false);", i)
                    self.botDriver.execute_script("arguments[0].scrollIntoView();", i)
                    if i.find_element("class name", "user-name-text").text == nickName:
                        online = False if "offline" in i.get_attribute("class") else True
                        i.click()
                        try:
                            self.waitElement("class name", "user-info-card-content", 5, 0)
                        except TimeoutException:
                            return None
                        nameCard = self.botDriver.find_element("class name", "user-basic-content")
                        try:
                            userNameIdText = nameCard.find_element("class name", "user-name")
                        except NoSuchElementException:
                            userName = nameCard.find_element("class name", "name").text
                            userId = nameCard.find_element("class name", "user-id").text.replace("#", "")
                            userNameId = userName + "#" + userId
                            userNick = userName
                        else:
                            userName = userNameIdText.find_element("class name", "name").text
                            userId = userNameIdText.find_element("class name", "user-id").text.replace("#", "")
                            userNameId = userName + "#" + userId
                            userNick = nameCard.find_element("class name", "name").text

                        roles = []
                        roleBox = self.botDriver.find_elements("class name", "role-name")
                        for j in roleBox:
                            roles.append(j.text)

                        userGaming = {}
                        try:
                            gamingBox = self.botDriver.find_element("class name", "user-game-panel")
                        except NoSuchElementException:
                            pass
                        else:
                            userGamingType = gamingBox.find_element("class name", "title").text
                            userGaming["type"] = userGamingType
                            if userGamingType == "正在玩游戏":
                                userGaming["game"] = gamingBox.find_element("class name", "game-name").text
                                userGaming["time"] = gamingBox.find_element("class name", "game-time").text
                            else:
                                userGaming["name"] = gamingBox.find_element("class name", "music-name").text
                                userGaming["siger"] = gamingBox.find_element("class name", "music-siger").text
                                userGamingIcon = gamingBox.find_element("class name", "game-icon").get_attribute("style")
                                if userGamingIcon:
                                    userGaming["icon"] = re.findall('url[(]"(.*?)"[)]', userGamingIcon)[0]
                                else:
                                    userGaming["icon"] = None

                        try:
                            userBannerImg = self.botDriver.find_element("class name", "user-banner.has-banner")
                            userAvatarStyle = userBannerImg.get_attribute("style")
                            userBanner = re.findall('url[(]"(.*?)"[)]', userAvatarStyle)[0]
                        except NoSuchElementException:
                            userBanner = None

                        userAvatarBox = self.botDriver.find_element("class name", "user-avatar-img")
                        userAvatarImg = userAvatarBox.find_element("class name", "kook-avatar-picture-static")
                        userAvatarStyle = userAvatarImg.get_attribute("style")
                        userAvatar = re.findall('url[(]"(.*?)/icon"[)]', userAvatarStyle)[0]
                        if isReadProfile:
                            userAvatarBox.click()
                            profile = self.waitElement("class name", "textarea-box", 1, 0).text
                            self.botDriver.find_element("tag name", "body").send_keys(Keys.ESCAPE)
                        else:
                            profile = None
                            self.botDriver.find_element("tag name", "body").send_keys(Keys.ESCAPE)
                        return {"online": online, "nameId": userNameId, "name": userName, "id": userId, "nick": userNick, "avatar": userAvatar,
                                "banner": userBanner, "profile": profile, "game": userGaming}
                except NoSuchElementException:
                    continue
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
