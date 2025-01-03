import json
import re
import logging
import requests
from PIL import Image, ImageDraw, ImageColor
import areaImage
import webcolors

with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
logging.info("mapGen.py 画像生成のための設定を読み込みました。")


beforeMapNmame = ""
positionList = []


def mapping(image: Image, hall: str, day: int, circlePlace, priority):
    global beforeMapNmame, positionList

    logging.info(f"{circlePlace}のマップの位置データを取得します")
    url = settings["url"]["webMapData"]["domainOrigin"] + \
        settings["url"]["webMapData"]["mapData"] + hall
    cookie = settings["url"]["cookie"]
    colorName = settings["priorityColor"]["priority" + str(priority)]
    logging.info(f"{hall}のマップの位置データを取得します")

    if hall != beforeMapNmame:
        beforeMapNmame = hall
        positionList = getMapDataFromWeb(hall, url, cookie)
    else:
        pass

    space_dict = preprocess_data(positionList)

    basePlace = circlePlace[:3]
    try:
        count = space_dict[basePlace]
    except KeyError:
        return image
    print(positionList[count])
    circlePlaceData = positionList[count]

    positionDataList = areaImage.openGridFile(hall, day)
    position = positionDataList[circlePlaceData["locate"]
                                [0]][circlePlaceData["locate"][1]]

    baseCorrection = (settings["map"]["cellSize"]-1)/2

    x = position[0]+1
    y = position[1]+1
    if "←" in circlePlaceData["dirbase"]:
        x -= int((int(settings["map"]["cellSize"])-1)/2)

    x += baseCorrection
    y += baseCorrection
    x_end = x
    y_end = y

    print("base", x, y, x_end, y_end)

    palce = circlePlace[3:]
    print(palce)
    x_start_correction, y_start_correction, x_end_correction, y_end_correction = abPosition(
        circlePlaceData["dirbase"][0], palce)

    x += x_start_correction
    y += y_start_correction
    x_end += x_end_correction
    y_end += y_end_correction
    y_save = y

    print(x, y, x_end, y_end)
    # 画像のピクセルデータにアクセスするためのオブジェクトを取得
    pixels = image.load()

    # 範囲内の白いピクセルを置換
    for x in range(int(x), int(x_end)):
        y = (y_save)
        for y in range(int(y), int(y_end)):
            if all(240 <= pixels[x, y][i] <= 255 for i in range(3)):  # 白いピクセルを特定
                pixels[x, y] = ImageColor.getrgb(colorName)  # 指定の色に置換
    return image


def preprocess_data(data):
    space_dict = {}
    for i, element in enumerate(data):
        space = element.get("space")
        space_dict[space] = i
    return space_dict


def getMapDataFromWeb(hall, url, cookie):
    response = requests.get(url, cookies=cookie, allow_redirects=False)
    if response.status_code == 302:
        logging.error(
            f"ステータスコード{response.status_code} 権限エラーです。\n cookieを更新してください")
    logging.info(
        f"ステータスコード{response.status_code} {hall}のデータを取得しました。")
    hallMapJson = response.json()
    return hallMapJson["mapcsv"]


def abPosition(base, place):
    x_start_correction = 0
    y_start_correction = 0
    x_end_correction = 0
    y_end_correction = 0
    base_correction = (settings["map"]["cellSize"]-1)/2
    if place == "ab":
        x_start_correction = -base_correction
        y_start_correction = -base_correction
        x_end_correction = base_correction
        y_end_correction = base_correction
    elif place == "a":
        if base == "左":
            x_start_correction = -base_correction
            y_start_correction = -base_correction
            x_end_correction = 0
            y_end_correction = base_correction
        elif base == "右":
            x_start_correction = 0
            y_start_correction = -base_correction
            x_end_correction = base_correction
            y_end_correction = base_correction
        elif base == "上":
            x_start_correction = -base_correction
            y_start_correction = -base_correction
            x_end_correction = base_correction
            y_end_correction = 0
        elif base == "下":
            x_start_correction = -base_correction
            y_start_correction = 0
            x_end_correction = base_correction
            y_end_correction = base_correction
    elif place == "b":
        if base == "左":
            x_start_correction = 0
            y_start_correction = -base_correction
            x_end_correction = base_correction
            y_end_correction = base_correction
        elif base == "右":
            x_start_correction = -base_correction
            y_start_correction = -base_correction
            x_end_correction = 0
            y_end_correction = base_correction
        elif base == "上":
            x_start_correction = -base_correction
            y_start_correction = 0
            x_end_correction = base_correction
            y_end_correction = base_correction
        elif base == "下":
            x_start_correction = -base_correction
            y_start_correction = -base_correction
            x_end_correction = base_correction
            y_end_correction = 0
    return x_start_correction, y_start_correction, x_end_correction, y_end_correction


# image = Image.open("mapimage/out/e7-day1.png")

# # # image = mapping(image, "w12", 1, "の42a", 5)
# image = mapping(image, "e7", 1, "n07b", 5)
# image = mapping(image, "e7", 1, "n07a", 4)

# image.save("result.png")
