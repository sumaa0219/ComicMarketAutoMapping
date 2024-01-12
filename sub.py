import json
import mapGen
import listGen
import requests
import imgGen
import os
from plyer import notification
import os
from platform import system

# 設定ファイルの読み込み
with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)

cookie = settings["url"]["webMapInfo"]["cookie"]

pf = system()
# os.remove("generate.log")
# サークル情報の読み込み
# with open("list.json", 'r', encoding="utf-8") as json_file:
#     circleInfoJson = json.load(json_file)
circleInfoJson = requests.get(
    "https://com-fork-c103.vercel.app/api/db/circle", allow_redirects=False).json()
print("サークル情報の読み込みが完了しました。")

# 購入物情報の読み込み
# with open("item.json", 'r', encoding="utf-8") as json_file:
#     itemInfoJson = json.load(json_file)
itemInfoJson = requests.get(
    "https://com-fork-c103.vercel.app/api/db/item", allow_redirects=False).json()
print("購入物情報の読み込みが完了しました。")

# ユーザーの読み込み
# with open("user.json", 'r', encoding="utf-8") as json_file:
#     userInfoJson = json.load(json_file)
userInfoJson = requests.get(
    "https://com-fork-c103.vercel.app/api/db/user", allow_redirects=False).json()
print("ユーザー情報の読み込みが完了しました。")

Info, itemIDperCircle = mapGen.genCircleInfoList(circleInfoJson, itemInfoJson)
# mapGen.mapGen("c103.xlsm", Info, 1, "out2.xlsx")
# print(Info)
listGen.circleInfoImageGen(
    Info, itemInfoJson, itemIDperCircle, 1, userInfoJson)
print("サークル情報の画像生成が完了しました。")
pathlist = listGen.buylistImageGen(Info, 1, "w12")


if pf == "Darwin":
    os.system("osascript -e 'display notification \"完了しました。\"'")
elif pf == "Windows":
    notification.notify(
        title="報告",
        message="完了しました。",
        app_name="プログラム監視"
    )
