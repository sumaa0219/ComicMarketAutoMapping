import json
import mapGen
import listGen
import requests
import imgGen
import os

# 設定ファイルの読み込み
with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)

cookie = settings["url"]["webMapInfo"]["cookie"]

os.remove("generate.log")
# サークル情報の読み込み
# with open("list.json", 'r', encoding="utf-8") as json_file:
#     circleInfoJson = json.load(json_file)
circleInfoJson = requests.get(
    "https://com-fork-c103.vercel.app/api/db/circle", allow_redirects=False).json()


# 購入物情報の読み込み
# with open("item.json", 'r', encoding="utf-8") as json_file:
#     itemInfoJson = json.load(json_file)
itemInfoJson = requests.get(
    "https://com-fork-c103.vercel.app/api/db/item", allow_redirects=False).json()


# ユーザーの読み込み
# with open("user.json", 'r', encoding="utf-8") as json_file:
#     userInfoJson = json.load(json_file)
userInfoJson = requests.get(
    "https://com-fork-c103.vercel.app/api/db/user", allow_redirects=False).json()


Info, itemIDperCircle = mapGen.genCircleInfoList(circleInfoJson, itemInfoJson)
# mapGen.mapGen("c103.xlsm", Info, 1, "out2.xlsx")
# print(Info)
listGen.webCircleInfo(Info, itemInfoJson, itemIDperCircle, 1)

# circleInfo = requests.get(
#     "https://webcatalog-free.circle.ms/Circle/18000267/DetailJson", cookies=cookie, allow_redirects=False).json()
# url = "https://webcatalog-free.circle.ms/Spa/CachedImage/18000266/1/5e5500aa-74de-44b0-b490-08db97daf671/3903477550986"
# imgGen.genCircleImage(circleInfo, itemInfoJson,
#                       itemIDperCircle[10], url, userInfoJson)
