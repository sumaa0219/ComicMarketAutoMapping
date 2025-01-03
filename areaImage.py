import json
import requests
import os
import re
import logging
from PIL import Image, ImageDraw

# ログの設定
logging.basicConfig(filename='generate.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
logging.info("画像生成のための設定を読み込みました。")


def genAllAreaMapImage():
    baseMapAssetsDir = settings["map"]["baseMapAssetsDir"]
    if not os.path.exists(baseMapAssetsDir):
        logging.error(
            f"ディレクトリ{baseMapAssetsDir}が存在しません。設定を変更するか、マップ画像を配置してください。")
        return

    baseMapAssetsDirList = os.listdir(baseMapAssetsDir)

    if len(baseMapAssetsDirList) == 0:
        logging.error(
            f"ディレクトリ{baseMapAssetsDir}にエリアのディレクトリが存在しません。設定を変更するか、エリアのディレクトリを配置してください。")
        return

    for areaDir in baseMapAssetsDirList:
        if areaDir != "out":

            logging.info(f"{areaDir}の画像を生成します")
            mergeImagesWithTransparency(baseMapAssetsDir, areaDir)
            genMapGridData(areaDir)  # 実際にはファイル名として利用


def genAreaMapImage(baseMapAssetsDir, areaDir, layer):
    areaMapAssetsDir = os.path.join(baseMapAssetsDir, areaDir, layer)
    areaMapAssetsDirList = os.listdir(areaMapAssetsDir)
    if len(areaMapAssetsDirList) == 0:
        logging.error(
            f"ディレクトリ{areaMapAssetsDir}にエリアの画像が存在しません。設定を変更するか、エリアの画像を配置してください。")
        return

    maxMapWidthPerImage = settings["map"]["maxMapWidthPerImage"]
    instrationMapImageList = []
    for x in range(int(maxMapWidthPerImage)):
        imagePerSeparatedAreaList = []
        for y in range(int(maxMapWidthPerImage)):
            imagePath = os.path.join(
                areaMapAssetsDir, f"{x}-{y}.png")
            if os.path.exists(imagePath):
                imagePerSeparatedAreaList.append(imagePath)
            else:
                pass
        instrationMapImageList.append(imagePerSeparatedAreaList)

    width, height = getFullImageWidthHigh(instrationMapImageList)
    print(width, height)
    new_image = Image.new('RGBA', (width, height))
    positionX = 0
    # 画像を貼り付け
    for x in instrationMapImageList:
        positionY = 0
        for y in x:
            image = Image.open(y)
            new_image.paste(image, (positionX, positionY))
            positionY += image.height-1
        positionX += image.width-1

    # トリミングされた画像を保存
    return new_image


def mergeImagesWithTransparency(baseMapAssetsDir, areaDir):
    # try:
    image1 = genAreaMapImage(
        baseMapAssetsDir, areaDir, "main").convert("RGBA")
    # image2 = genAreaMapImage(
    #     baseMapAssetsDir, areaDir, "sub").convert("RGBA")

    # 画像を統合　image2は透過画像として扱いmardegeする
    merged_image = Image.new(
        "RGBA", image1.size, (255, 255, 255, 0))
    merged_image.paste(image1, (0, 0))
    # merged_image.paste(image2, (0, 0), image2)

    # 画像を保存
    outDir = os.path.join(baseMapAssetsDir, "out")
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    outputPath = os.path.join(outDir, f"{areaDir}.png")

    # アルファチャンネルを取得
    alpha = merged_image.split()[-1]
    # アルファチャンネルの境界を取得
    bbox = alpha.getbbox()
    # 画像をトリミング
    if bbox:
        print(bbox)
        adjusted_bbox = (bbox[0], bbox[1], bbox[2]+1, bbox[3])
        print(adjusted_bbox)
        merged_image = merged_image.crop(adjusted_bbox)

    # Save the merged image
    merged_image.save(outputPath)
    logging.info(f"画像を統合して保存しました: {outputPath}")
    # except Exception as e:
    #     logging.error(f"画像の統合中にエラーが発生しました: {e}")


def getFullImageWidthHigh(instrationMapImageList):
    # 画像の幅と高さを取得
    width = 0
    height = 0
    try:
        for x in range(len(instrationMapImageList)):
            image = Image.open(instrationMapImageList[x][0])
            print("0")
            width += image.width
            if x == 0:
                for y in range(len(instrationMapImageList[x])):
                    print("1")
                    image = Image.open(instrationMapImageList[x][y])
                    height += image.height
    except IndexError:
        pass
    return width, height


def genMapGridData(areaName):
    AreaName = areaName[:-5]
    print(AreaName)
    startPosition = settings["map"]["startPosition"][AreaName]
    cellSize = settings["map"]["cellSize"]
    imageFilePath = os.path.join(
        settings["map"]["baseMapAssetsDir"], "out", f"{areaName}.png")
    image = Image.open(imageFilePath)
    baseX = startPosition["x"]
    gridList = []
    print(image.width, image.height, int(image.width /
          (cellSize-1)), int(image.height/(cellSize-1)))
    for x in range(int(image.width/(cellSize-1))):
        gridgridList = []
        baseY = startPosition["y"]
        for y in range(int(image.height/(cellSize-1))):
            gridgridList.append([baseX, baseY])
            baseY += cellSize-1
        baseX += cellSize-1
        gridList.append(gridgridList)
    # print(gridList)
    with open(os.path.join(settings["map"]["baseMapAssetsDir"], "out", f"{areaName}.txt"), 'w') as f:
        for row in gridList:
            f.write(' '.join(map(str, row)) + '\n')


def openGridFile(areaName, day):
    filePath = os.path.join(
        settings["map"]["baseMapAssetsDir"], "out", f"{areaName}-day{day}.txt")
    with open(filePath, 'r') as f:
        rowData = f.readlines()

    data = []
    for line in rowData:
        row = []
        pairs = line.strip().split()
        for num in range(0, len(pairs), 2):
            row.append([int(pairs[num].replace("[", "").replace("]", "").replace(
                ",", "")), int(pairs[num+1].replace("[", "").replace("]", "").replace(",", ""))])
        data.append(row)
    return data


def tryGrid(areaName, day):  # 使わない（デバック用）
    gridData = openGridFile(areaName, day)
    # 画像を読み込む
    image = Image.open(os.path.join(
        settings["map"]["baseMapAssetsDir"], "out", f"{areaName}-day{day}.png"))
    draw = ImageDraw.Draw(image)
    cellSize = settings["map"]["cellSize"]

    # Draw squares
    for row in gridData:
        for point in row:
            left_up_point = (point[0], point[1])
            right_down_point = (point[0] + cellSize-1, point[1] + cellSize-1)
            draw.rectangle([left_up_point, right_down_point],
                           outline='red', fill=None)

    # Save the image
    image.save(f'{areaName}_grid.png')


# genAllAreaMapImage()  # 基本これだけ実行でOK
# genMapGridData("e123-day1")
# tryGrid("e123", "1")
