from mapping import mapping
import json
import re


def mapGen(excelFileName, circleJson, dayOption, outFileName):

    counter = 0
    day1 = []
    day2 = []
    day1Counter = 0
    day2Counter = 0

    for circleID in circleJson:
        # サークル情報の取得
        circleInfo = circleJson[circleID]
        day = circleInfo["day"]
        if day == "1":
            day1.append(circleID)
        elif day == "2":
            day2.append(circleID)
    print("day1=", len(day1), "day2=", len(day2))
    print("load complete circleInfomation")

    for i, circleID in enumerate(circleJson):

        # サークル情報の取得
        circleInfo = circleJson[circleID]

        # サークル名前
        circlePlace = circleInfo["place"]
        match = re.match(r"([^\d]*\d+)(\w+)", circlePlace)
        if match:
            base, suffixes = match.groups()
            circlePlaces = ["_" + base + suffix for suffix in suffixes]
        else:
            circlePlaces = ["_" + circlePlace]  # 注意　リスト型

        day = circleInfo["day"]
        try:
            priority = circleInfo["priority"]
            # オプションによって生成回数の変更(最後)
            if dayOption == 1:
                if day == "1":
                    for circlePlace in circlePlaces:
                        if counter != 0:
                            excelFileName = outFileName
                        else:
                            counter += 1
                        mapping(excelFileName, circlePlace,
                                priority, outFileName)
                        print(len(day1)/day1Counter * 100, "%完了")
                        day1Counter += 1
            elif dayOption == 2:
                if day == "2":
                    for circlePlace in circlePlaces:
                        if counter != 0:
                            excelFileName = outFileName
                        else:
                            counter += 1
                        mapping(excelFileName, circlePlace,
                                priority, outFileName)
                        print(len(day2)/day2Counter * 100, "%完了")
                        day2Counter += 1
            elif dayOption == 3:
                outFileName = "day1_" + outFileName
                if day == "1":
                    for circlePlace in circlePlaces:
                        if counter != 0:
                            excelFileName = outFileName
                        else:
                            counter += 1
                        mapping(excelFileName, circlePlace,
                                priority, outFileName)
                        print(len(day1)/day1Counter * 100, "%完了")
                        day1Counter += 1
                if day == "2":
                    outFileName = "day1_" + outFileName
                    for circlePlace in circlePlaces:
                        if counter != 0:
                            excelFileName = outFileName
                        else:
                            counter += 1
                        mapping(excelFileName, circlePlace,
                                priority, outFileName)
                        print(len(day2)/day2Counter * 100, "%完了")
                        day2Counter += 1
        except:
            pass


def genCircleInfoList(circleInfos, priorityInfos):
    infoList = {}
    for circleInfo in circleInfos:
        if circleInfos[circleInfo]["deleted"] == False:
            for priority in priorityInfos:
                try:
                    if circleInfos[circleInfo]["id"] == priority["circleId"]:
                        circleInfos[circleInfo]["priority"] = priority["priority"]
                        infoList.update(circleInfos)
                except:
                    pass

    return infoList


# サークル情報の読み込み
with open("list.json", 'r', encoding="utf-8") as json_file:
    circleInfoJson = json.load(json_file)

with open("priority.json", 'r', encoding="utf-8") as json_file:
    priorityInfoJson = json.load(json_file)

with open("aaa.json", 'r', encoding="utf-8") as json_file:
    aaa = json.load(json_file)
Info = genCircleInfoList(circleInfoJson, priorityInfoJson)
mapGen("c103.xlsm", aaa, 1, "out.xlsx")

# サークル情報のjsonファイルの形式
# "circleId1": {
#         "name": "xxxx",
#         "day": 1,
#         "place": "a01ab",
#         "rank": 5,
#         "wing": "east"
#     }
