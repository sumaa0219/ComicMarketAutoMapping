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

cookie = settings["url"]["cookie"]


pf = system()
# os.remove("generate.log")
# サークル情報の読み込み
# with open("list.json", 'r', encoding="utf-8") as json_file:
#     circleInfoJson = json.load(json_file)
circleInfoJson = requests.get(
    "https://com-fork-c104.vercel.app/api/db/circle", allow_redirects=False).json()
print("サークル情報の読み込みが完了しました。")

# 購入物情報の読み込み
# with open("item.json", 'r', encoding="utf-8") as json_file:
#     itemInfoJson = json.load(json_file)
itemInfoJson = requests.get(
    "https://com-fork-c104.vercel.app/api/db/item", allow_redirects=False).json()
print("購入物情報の読み込みが完了しました。")

# ユーザーの読み込み
# with open("user.json", 'r', encoding="utf-8") as json_file:
#     userInfoJson = json.load(json_file)
userInfoJson = requests.get(
    "https://com-fork-c104.vercel.app/api/db/user", allow_redirects=False).json()
print("ユーザー情報の読み込みが完了しました。")

Info, itemIDperCircle = mapGen.genCircleInfoList(circleInfoJson, itemInfoJson)
# mapGen.mapGen("e123", Info, 1, "1日目東123ホール.png")
# mapGen.mapGen("e456", Info, 2, "2日目東456ホール.png")
# mapGen.mapGen("e7", Info, 1, "1日目東7ホール.png")
# mapGen.mapGen("w12", Info, 1, "1日目西ホール.png")

# for day in [1, 2]:
#     listGen.circleInfoImageGen(
#         Info, itemInfoJson, itemIDperCircle, day, userInfoJson)
#     print("サークル情報の画像生成が完了しました。")
#     for hallOption in settings["block"]:
#         hall = settings["block"][hallOption]
#         mapGen.mapGen(hall, Info, day, f"out/map_day{day}_{hall}.png")

#         # print(Info, itemIDperCircle)

#         pathlist = listGen.buylistImageGen(Info, day, hall)

print(settings["block"].keys())


if pf == "Darwin":
    os.system("osascript -e 'display notification \"完了しました。\"'")
elif pf == "Windows":
    notification.notify(
        title="報告",
        message="完了しました。",
        app_name="プログラム監視"
    )
