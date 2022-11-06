import os
import re
import shutil
import sys
import zipfile
import requests
from bs4 import BeautifulSoup
from lib.MainDownloader import download


def updateMSEdgeDriver():
    downloadPage = requests.get("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/").text
    DPSoup = BeautifulSoup(downloadPage, "html.parser")
    downloadItems = DPSoup.find_all(class_="bare driver-downloads")
    for i in downloadItems:
        downloadLink = re.findall('<a aria-label="x64 .*? channel, version .*?" href="(.*?/edgedriver_win64.zip)">x64</a>', str(i))
        if downloadLink:
            downloadLink = downloadLink[0]
            break
    else:
        raise Exception("无法找到下载链接,请手动更新https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
    fileName = os.path.basename(downloadLink)
    download(downloadLink, "./lib/"+fileName)
    DFZip = zipfile.ZipFile("./lib/"+fileName)
    DFZip.extractall("./lib/")
    DFZip.close()

    os.remove("./lib/"+fileName)
    shutil.rmtree("./lib/Driver_Notes")
    shutil.rmtree("TempDownload")


def updateChromeDriver():
    chromeVersionRaw = os.popen("google-chrome -version")
    chromeVersion = chromeVersionRaw.read().split(" ")[2]
    path = "./lib/"+os.path.basename("https://registry.npmmirror.com/-/binary/chromedriver/{chromeVersion}/chromedriver_{sys.platform}.zip")
    try:
        download(f"https://registry.npmmirror.com/-/binary/chromedriver/{chromeVersion}/chromedriver_{sys.platform}.zip", path)
    except Exception as err:
        print(err, "无法更新chromedriver,请手动下载到(lib):https://registry.npmmirror.com/binary.html?path=chromedriver/")
    chromeDriverZip = zipfile.ZipFile(path)
    chromeDriverZip.extractall("./lib/")
    chromeDriverZip.close()

    os.remove(path)
    shutil.rmtree("TempDownload")
