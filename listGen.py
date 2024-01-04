import json
import requests
import time

# 設定ファイルの読み込み
with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
print("settings for listing is loaded")

cookie = {"ARRAffinity": "7d577d29f8e00b2374ddb413016b2f6617c84445e3b963399a9d336135481e13",
          "ARRAffinitySameSite": "7d577d29f8e00b2374ddb413016b2f6617c84445e3b963399a9d336135481e13"
          }


# def webCircleInfo(circleWithPriorityInfoJson, itemInfoJson, itemIDperCircleList, day):
def webCircleInfo(day):

    domainOrigin = settings["url"]["webMapInfo"]["domainOrigin"]
    mapInfo = settings["url"]["webMapInfo"]["mapInfo"]

    for block in settings["block"]:
        hall = settings["block"][block]
        url = f"{domainOrigin}{mapInfo}?day=Day{day}&hall={hall}"
        response = requests.get(url, cookies=cookie)
        if response.status_code == 302:
            print("cookieを更新してください")
            break
        print(response.text)

    # for i, circleID in enumerate(circleWithPriorityInfoJson):
    #     if circleWithPriorityInfoJson[circleID]["day"] == str(day):

    #         pass


webCircleInfo(1)
