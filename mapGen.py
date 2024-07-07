import json
import re
import logging
import requests
from mapping import mapping
from PIL import Image, ImageDraw
import os

# ログの設定
logging.basicConfig(filename='generate.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)


def mapGen(hall, circleJson, dayOption, outFileName):

    day1 = []
    day2 = []
    day1Counter = 0
    day2Counter = 0

    imagePath = os.path.join(
        settings["map"]["baseMapAssetsDir"], "out", f"{hall}-day{day}.png")
    image = Image.open(imagePath)

    for circleID in circleJson:
        # サークル情報の取得
        circleInfo = circleJson[circleID]
        day = circleInfo["day"]
        if day == "1":
            day1.append(circleID)
        elif day == "2":
            day2.append(circleID)
    logging.info(f"1日目={len(day1)}サークル 2日目={len(day2)} サークル")
    logging.info("登録サークルの情報を取得を完了しました。")

    logging.info(f"{dayOption}日目のマッピングを開始します。")
    for i, circleID in enumerate(circleJson):

        # サークル情報の取得
        circleInfo = circleJson[circleID]

        # サークル名前
        circlePlace = circleInfo["place"]
        match = re.match(r"([^\d]*\d+)(\w+)", circlePlace)
        if match:
            base, suffixes = match.groups()
            circlePlaces = [base + suffix for suffix in suffixes]
        else:
            circlePlaces = [circlePlace]  # 注意　リスト型

        day = circleInfo["day"]
        priority = circleInfo["priority"]
        print(circlePlaces)
        # オプションによって生成回数の変更(最後)
        if dayOption == 1:
            if day == "1":
                for circlePlace in circlePlaces:
                    image = mapping(image, hall, circlePlace,
                                    priority)
                    logging.debug(f"サークルマッピング:{circlePlace} {priority}")
                    # print(f"{len(day1)/day1Counter * 100}%完了")
                    day1Counter += 1
        elif dayOption == 2:
            if day == "2":
                for circlePlace in circlePlaces:
                    image = mapping(image, hall, circlePlace,
                                    priority)
                    logging.debug(f"サークルマッピング:{circlePlace} {priority}")
                    # logging.info(f"{len(day2)/day2Counter * 100}%完了")
                    day2Counter += 1
        else:
            logging.error("dayOptionの値が不正です。再度実行してください。")
            break

    # # 保存
    image.save(outFileName)
    logging.info(f"マップデータ<{ outFileName}>の作成及び保存を完了しました。")


def genCircleInfoList(circleInfos, itemInfos):
    infoList = {}
    itemIDperCircle = {}

    logging.info("購入物とサークルの関係を調べます。")
    for circleInfo in circleInfos:
        if circleInfos[circleInfo]["deleted"] == False:
            itemcircleList = {}
            i = 0
            for item in itemInfos:
                if circleInfos[circleInfo]["id"] == itemInfos[item]["circleId"]:
                    itemcircleList.update({str(i): itemInfos[item]["id"]})
                    i += 1
            itemIDperCircle.update({circleInfo: itemcircleList})
        elif circleInfos[circleInfo]["deleted"] == True:
            logging.warning(f"サークル{circleInfos[circleInfo]['name']}は削除されています。")
    logging.info("すべての購入物とサークルの関係を取得しました。")
    # print(itemIDperCircle)  # サークルごとのアイテムIDのリスト 必要なら出す

    logging.info("すべてのサークル情報に購入物における最高優先度の情報を追加します。")
    for circleInfo in circleInfos:
        if circleInfos[circleInfo]["deleted"] == False:
            info = circleInfos[circleInfo]
            priority = 0
            if circleInfo in itemIDperCircle:  # この行を追加
                for itemIdNum in itemIDperCircle[circleInfo]:  # この行を修正
                    itemID = itemIDperCircle[circleInfo][itemIdNum]  # この行を修正
                    for users in itemInfos[itemID]["users"]:
                        if priority < users["priority"]:
                            priority = users["priority"]
            if priority != 0:
                info["priority"] = priority
                infoList.update({circleInfo: info})
            elif priority == 0:
                logging.warning(
                    f"サークル{circleInfos[circleInfo]['name']}の購入物の優先度は0に設定されています。")
    logging.info("すべてのサークル情報に優先度の情報を追加しました。")

    return infoList, itemIDperCircle

# サークル情報のjsonファイルの形式
# "demo.json"を参照
