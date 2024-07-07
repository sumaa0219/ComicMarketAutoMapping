import json
import requests
import os
import re
import logging
import imgGen

# ログの設定
logging.basicConfig(filename='generate.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')


# 設定ファイルの読み込み
with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
logging.info("リスト作成のための設定を読み込みました。")

# ユーザーの読み込み  消して！！！！
# with open("user.json", 'r', encoding="utf-8") as json_file:
#     userInfoJson = json.load(json_file)

cookie = settings["url"]["cookie"]


def circleInfoImageGen(circleWithPriorityInfoJson, itemInfoJson, itemIDperCircleList, day, userInfoJson):

    mapDomainOrigin = settings["url"]["webMapInfo"]["domainOrigin"]
    mapInfo = settings["url"]["webMapInfo"]["mapInfo"]
    mapJson = {}

    for block in settings["block"]:
        hall = settings["block"][block]
        url = f"{mapDomainOrigin}{mapInfo}?day=Day{day}&hall={hall}"
        response = requests.get(url, cookies=cookie, allow_redirects=False)
        if response.status_code == 302:
            logging.error(
                f"ステータスコード{response.status_code} 権限エラーです。\n cookieを更新してください")
            break

        logging.info(
            f"ステータスコード{response.status_code} {day}日目 {hall}のデータを取得しました。")
        mapJson.update(response.json())
        # 以下のようなデータが取得される
        # あ01a: {
        #     wid: 19016572,
        #     id: 10435692
        #     }

    logging.info("マップデータの取得が完了しました。")
    # with open('mapData.json', 'w', encoding="utf-8") as f:
    #     json.dump(mapJson, f, indent=2, ensure_ascii=False)  # 動作が不安定になるようなら

    selectDayCircleJson = {}
    for i, circleID in enumerate(circleWithPriorityInfoJson):
        if circleWithPriorityInfoJson[circleID]["day"] == str(day):
            selectDayCircleJson.update(
                {circleID: circleWithPriorityInfoJson[circleID]})
    logging.info(f"{len(selectDayCircleJson)}個のサークルがリストに追加されます")

    outputFileNameList = []
    for i, circleID in enumerate(selectDayCircleJson):
        try:

            place = selectDayCircleJson[circleID]["place"]
            match = re.match(r"([^\d]*\d+)(\w+)", place)
            if match:
                base, suffixes = match.groups()
                circlePlaces = [base + suffix for suffix in suffixes]
                logging.debug(f"サークルの場所{place}は{circlePlaces}に変換されました")
            else:
                circlePlaces = [place]  # 注意　リスト型

            wid = mapJson[circlePlaces[0]]["wid"]
            reqURL = f"{mapDomainOrigin}/Circle/{wid}/DetailJson"
            circleInfo = requests.get(
                reqURL, cookies=cookie, allow_redirects=False).json()
            circleImageURL = circleInfo["CircleCutUrls"][0]
            imageURL = mapDomainOrigin + circleImageURL
            # print(selectDayCircleJson[circleID])
            image = imgGen.genCircleImage(circleInfo, selectDayCircleJson[circleID],
                                          itemIDperCircleList[circleID], itemInfoJson, imageURL, userInfoJson)

            if image != "Noimage":
                path = os.path.join("out", circleID)
                image.save(f"{path}.png")
                outputFileNameList.append(f"{path}.png")
        except Exception as e:
            # logging.error(f"{e}")
            pass
    return outputFileNameList


def buylistImageGen(circleInfo, day, hall):
    mapDomainOrigin = settings["url"]["webMapInfo"]["domainOrigin"]
    mapInfo = settings["url"]["webMapInfo"]["mapInfo"]

    url = f"{mapDomainOrigin}{mapInfo}?day=Day{day}&hall={hall}"
    response = requests.get(url, cookies=cookie, allow_redirects=False)
    if response.status_code == 302:
        logging.error(
            f"ステータスコード{response.status_code} 権限エラーです。\n cookieを更新してください")

    logging.info(
        f"ステータスコード{response.status_code} {day}日目 {hall}のデータを取得しました。")

    hallMapJson = response.json()

    circleImageList = []
    for hallMapPlace in hallMapJson:
        for circleID in circleInfo:
            place = circleInfo[circleID]["place"]
            match = re.match(r"([^\d]*\d+)(\w+)", place)
            if match:
                base, suffixes = match.groups()
                circlePlaces = [base + suffix for suffix in suffixes]
                logging.debug(f"サークルの場所{place}は{circlePlaces}に変換されました")
            else:
                circlePlaces = [place]  # 注意　リスト型

            if circlePlaces[0] == hallMapPlace and circleInfo[circleID]["day"] == str(day):
                circleImageList.append(circleID)

    imgGen.genDayBuylistImagePerHall(circleImageList, day, hall)
