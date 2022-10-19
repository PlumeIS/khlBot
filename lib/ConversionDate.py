import datetime


def halfToFullDate(isNoon: str, time: str):
    if isNoon == "上午" or isNoon == "凌晨" or isNoon == "中午":
        return time
    elif isNoon == "下午":
        hourAndMinute = time.split(":")
        hour = int(hourAndMinute[0])
        minute = hourAndMinute[1]
        return f"{str(hour + 12).zfill(2)}:{minute}"


def ConversionDate(relativeTime: str, nowTime=None):
    if nowTime is None:
        nowTime = datetime.datetime.now()

    nowWeek = nowTime.weekday()

    timeArgsList = relativeTime.split(" ")
    fullTime = halfToFullDate(timeArgsList[1], timeArgsList[2])

    if timeArgsList[0] == "今天":
        return datetime.datetime.strptime(f'{nowTime.strftime("%Y-%m-%d")} {fullTime}', "%Y-%m-%d %H:%M")
    elif timeArgsList[0] == "昨天":
        return datetime.datetime.strptime(f'{(nowTime - datetime.timedelta(days=1)).strftime("%Y-%m-%d")} {fullTime}',
                                          "%Y-%m-%d %H:%M")

    elif timeArgsList[0] == "星期一":
        if nowWeek < 2:
            nowWeek += 7
        return datetime.datetime.strptime(
            f'{(nowTime - datetime.timedelta(days=nowWeek)).strftime("%Y-%m-%d")} {fullTime}', "%Y-%m-%d %H:%M")

    elif timeArgsList[0] == "星期二":
        if nowWeek + 1 < 3:
            nowWeek += 7
        return datetime.datetime.strptime(
            f'{(nowTime - datetime.timedelta(days=nowWeek + 1)).strftime("%Y-%m-%d")} {fullTime}', "%Y-%m-%d %H:%M")

    elif timeArgsList[0] == "星期三":
        if nowWeek + 2 < 4:
            nowWeek += 7
        return datetime.datetime.strptime(
            f'{(nowTime - datetime.timedelta(days=nowWeek + 2)).strftime("%Y-%m-%d")} {fullTime}', "%Y-%m-%d %H:%M")

    elif timeArgsList[0] == "星期四":
        if nowWeek + 3 < 5:
            nowWeek += 7
        return datetime.datetime.strptime(
            f'{(nowTime - datetime.timedelta(days=nowWeek + 3)).strftime("%Y-%m-%d")} {fullTime}', "%Y-%m-%d %H:%M")

    elif timeArgsList[0] == "星期五":
        if nowWeek + 4 < 6:
            nowWeek += 7
        return datetime.datetime.strptime(
            f'{(nowTime - datetime.timedelta(days=nowWeek + 4)).strftime("%Y-%m-%d")} {fullTime}', "%Y-%m-%d %H:%M")

    elif timeArgsList[0] == "星期六":
        if nowWeek + 5 < 7:
            nowWeek += 7
        return datetime.datetime.strptime(
            f'{(nowTime - datetime.timedelta(days=nowWeek + 5)).strftime("%Y-%m-%d")} {fullTime}', "%Y-%m-%d %H:%M")

    elif timeArgsList[0] == "星期日":
        if nowWeek + 6 < 8:
            nowWeek += 7
        return datetime.datetime.strptime(
            f'{(nowTime - datetime.timedelta(days=nowWeek + 6)).strftime("%Y-%m-%d")} {fullTime}', "%Y-%m-%d %H:%M")

    else:
        return datetime.datetime.strptime(f'{timeArgsList[0]} {fullTime}', "%Y年%m月%d日 %H:%M")
