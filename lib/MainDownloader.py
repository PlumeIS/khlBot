import os
import time
import requests
import threading
import tqdm

MB = 1024 * 1024                                            # 定义MB大小

basicHeaders = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44"
}

class RateBar:
    def __init__(self, initValue, msg, unit):
        self.value = initValue
        self.msg = msg
        self.unit = unit
        self.updateStamp = time.time()

    def update(self, increment):
        self.value += increment
        updateTime = time.time()-self.updateStamp
        speed = increment/updateTime
        print(f"\r{self.msg} {self.value}{self.unit} 速度:{speed}{self.unit}/s", end="")





def getFileSize(url):                                       # 获得文件总大小
    response = requests.head(url,
                             headers=basicHeaders,
                             allow_redirects=True)          # 获得返回头
    fileSize = response.headers.get("Content-Length")       # 获得头文件内的 内容长度
    if not fileSize:                                        # 判断是否有返回 内容长度
        return None
    else:
        return int(fileSize)                                # 返回整型数 内容长度


def splitFile(fileSize, splitSize):                         # 分块文件
    splits = []
    for headPos in range(-1, fileSize, splitSize):          # 循环 内容长度 阶梯为 splitSize
        tailPos = headPos + splitSize                       # 获得 下一个开始点
        splits.append((headPos+1, min(tailPos, fileSize)))  # 判断下一个开始点是否大于文件总长度 并 将分块添加到列表
    return splits                                           # 返回 列表[元组(头文件点,尾文件点)]


def ordinaryDownload(url, fileName):                        # 当无法多线程下载时 普通下载
    downloadSize = 0
    downloadStartTime = time.time()
    size = getFileSize(url)
    if size:
        bar = tqdm.tqdm(total=size, desc=f"文件下载 {fileName}")
    else:
        bar = RateBar(0, f"文件下载 {fileName} 已下载", "MB")
    responseData = requests.get(url,
                                headers=basicHeaders,
                                allow_redirects=True)       # 获得返回内容
    with open(fileName, "wb") as downloadFile:              # 打开文件
        for chunk in responseData.iter_content(512):        # 分块写入
            if chunk:                                       # 判断是否有数据
                downloadFile.write(chunk)                   # 以二进制写入数据
                downloadSize += 512
                print(f"\r已下载大小 {round(downloadSize/MB,2)}MB", end="")
    uesTime = round((time.time() - downloadStartTime), 2)
    print(f"\n下载完成 耗时{uesTime}s 速度{round(downloadSize/1024/1024/uesTime, 2)}MB/s")


def download(url, fileName):                                # 主下载函数
    fileSize = getFileSize(url)                             # 获得文件大小
    if fileSize is None:                                    # 判断是否返回文件长度
        print("文件无法获得总长度!开始普通下载")
        ordinaryDownload(url, fileName)                     # 普通下载文件
        return None

    if fileSize < 64*MB:                                    # 小于64MB的文件 16MB为一块
        fileSplit = splitFile(fileSize, 16*MB)
    elif fileSize < 128*MB:                                 # 小于128MB的文件 32MB为一块
        fileSplit = splitFile(fileSize, 32*MB)
    else:                                                   # 其余的64MB 为一块
        fileSplit = splitFile(fileSize, 64*MB)

    print(f'开始下载 总大小 {round(fileSize/MB, 2)}MB 文件分块数:{len(fileSplit)}')
    downloader = requests.session()                         # 下载流
    try:
        os.mkdir("TempDownload")                            # 创建临时文件夹
    except FileExistsError:
        pass
    bar = tqdm.tqdm(total=fileSize, desc=f"文件下载 {fileName}")

    def partDownload(Url, filePath, startPos, endPos, Downloader):
        headers = basicHeaders.copy()                       # 复制基础头文件
        headers["Range"] = f"bytes={startPos}-{endPos}"     # 更改下载区域
        data = Downloader.get(Url,
                              headers=headers,
                              stream=True,
                              allow_redirects=True)         # 下载分块文件
        with open(filePath, "wb") as downloadFile:          # 写入临时分块文件
            for chunk in data.iter_content(512):            # 分块写
                if chunk:
                    downloadFile.write(chunk)
                    bar.update(512)
    downloadStartTime = time.time()                         # 计时
    taskList = []
    for downloadId in range(len(fileSplit)):                # 启动分块下载
        time.sleep(0.1)
        path = "TempDownload/"+fileName.split("/")[-1]+"_Temp_"+str(downloadId)
        downloadTask = threading.Thread(target=partDownload, args=(url,
                                                                   path,
                                                                   fileSplit[downloadId][0],
                                                                   fileSplit[downloadId][1],
                                                                   downloader))
        downloadTask.start()
        taskList.append(downloadTask)                       # 将线程地址存储
    for task in taskList:
        task.join()                                         # 线程阻塞 等待下载完成
    uesTime = round((time.time()-downloadStartTime-(len(fileSplit)*0.1)), 2)
    bar.close()                                             # 计时结束
    print(f"下载完成 耗时{uesTime} 速度{round(fileSize/1024/1024/uesTime,2)}M/s 正在整合文件")
    with open(fileName, "wb") as File:                      # 整合文件
        for taskId in range(len(fileSplit)):
            path = "TempDownload/" + fileName.split("/")[-1] + "_Temp_" + str(taskId)
            with open(path, "rb") as TempFile:
                File.write(TempFile.read())
            os.remove(path)
    print(f"整合完成")


def downloadWithoutTemp(url, fileName):
    fileSize = getFileSize(url)                             # 获得文件大小

    if fileSize is None:                                    # 判断是否返回文件长度
        print("文件无法获得总长度!开始普通下载")
        ordinaryDownload(url, fileName)                     # 普通下载文件
        return None

    if fileSize < 64*MB:                                    # 小于64MB的文件 16MB为一块
        fileSplit = splitFile(fileSize, 16*MB)
    elif fileSize < 128*MB:                                 # 小于128MB的文件 32MB为一块
        fileSplit = splitFile(fileSize, 32*MB)
    else:                                                   # 其余的64MB 为一块
        fileSplit = splitFile(fileSize, 64*MB)

    print(f'开始下载 总大小 {round(fileSize/MB, 2)}MB 文件分块数:{len(fileSplit)}')
    bar = tqdm.tqdm(total=fileSize, desc=f"文件下载 {fileName}")
    downloader = requests.session()                         # 下载流

    def partDownload(Url, FileName, startPos, endPos, Downloader):
        chunks = []
        headers = basicHeaders.copy()                       # 复制基础头文件
        headers["Range"] = f"bytes={startPos}-{endPos}"     # 更改下载区域
        data = Downloader.get(Url,
                              headers=headers,
                              stream=True,
                              allow_redirects=True)         # 下载分块文件
        for chunk in data.iter_content(512):                # 分块处理
            if chunk:                                       # 判断是否有数据
                chunks.append(chunk)                        # 将数据暂存
                bar.update(512)                             # 更新进度条
        with open(FileName, "wb") as File:                  # 写入数据
            File.seek(startPos)                             # 移动指针到头位置
            for chunk in chunks:
                File.write(chunk)                           # 将暂存的数据写到文件里

    downloadStartTime = time.time()                         # 计时
    taskList = []
    for downloadId in range(len(fileSplit)):                # 启动分块下载
        time.sleep(0.1)
        downloadTask = threading.Thread(target=partDownload, args=(url,
                                                                   fileName,
                                                                   fileSplit[downloadId][0],
                                                                   fileSplit[downloadId][1],
                                                                   downloader))
        downloadTask.start()
        taskList.append(downloadTask)                       # 将线程地址存储
    for task in taskList:
        task.join()                                         # 线程阻塞 等待下载完成
    uesTime = round((time.time() - downloadStartTime - (len(fileSplit) * 0.1)), 2)
    bar.close()                                             # 计时结束
    print(f"下载完成 耗时{int(uesTime/60)}min{uesTime%60} 速度{round(fileSize / 1024 / 1024 / uesTime, 2)}M/s")
