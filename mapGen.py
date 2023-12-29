import mapping
import json
import re

# mapping.mapping("sample.xlsx", "circlePlace", 1, "out.xlsx")


def mapGen(excelFileName, circleJsonFileName, dayOption, outFileName):

    # サークル情報の読み込み
    with open(circleJsonFileName, 'r', encoding="utf-8") as json_file:
        circleInfoJson = json.load(json_file)

    for circleID in circleInfoJson:
        # サークル情報の取得
        circleInfo = circleInfoJson[circleID]

        # サークル名前
        circlePlace = circleInfo["place"]
        match = re.match(r"([^\d]*\d+)(\w+)", circlePlace)
        if match:
            base, suffixes = match.groups()
            circlePlaces = [base + suffix for suffix in suffixes]
        else:
            circlePlaces = [circlePlace]  # 注意　リスト型

        # オプションによって生成回数の変更(最後)
        if dayOption == 1:
            circlePlaces = [circlePlaces[0]]

        # circleRank = circleInfo["rank"]
        # if dayOption == 1:
        #     circleRank = circleInfo["rank1"]
        # elif dayOption == 2:
        #     circleRank = circleInfo["rank2"]
        # mapping.mapping(excelFileName, circlePlace, circleRank, outFileName)
        print(circlePlaces)


mapGen("103.xlsm", "list.json", 1, "out.xlsx")
