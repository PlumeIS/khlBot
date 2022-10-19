import os
import re
import shutil
import zipfile
import requests
from bs4 import BeautifulSoup
from .MainDownloader import download


def updateMSEdgeDriver(path):
    downloadPage = requests.get("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/").text
    DPSoup = BeautifulSoup(downloadPage, "html.parser")
    downloadItems = DPSoup.find_all(class_="bare driver-downloads")
    downloadLink = re.findall('<a aria-label="x64 stable channel, version .*?" href="(.*?/edgedriver_win64.zip)">x64</a>', str(downloadItems[0]))[0]
    filePath = os.path.basename(downloadLink)
    download(downloadLink, filePath)
    DFZip = zipfile.ZipFile(filePath)
    DFZip.extractall(path)
    DFZip.close()

    os.remove(f"edgedriver_win64.zip")
    shutil.rmtree(f"{path}Driver_Notes")
    shutil.rmtree(f"TempDownload")
