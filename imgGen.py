from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import json
import logging
import webcolors
import math
import os
import img2pdf

# ログの設定
logging.basicConfig(filename='generate.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
logging.info("画像生成のための設定を読み込みました。")

if os.path.exists("out") == False:
    os.mkdir("out")
if os.path.exists("out/buyListImage") == False:
    os.mkdir("out/buyListImage")
if os.path.exists("out/toBuyList") == False:
    os.mkdir("out/toBuyList")

cookie = settings["url"]["cookie"]


def genCircleImage(circleInfofromWeb, circleInfo, BuyItemList, itemList, imageURL, userInfo):
    # print(circleInfofromWeb, itemInfo, BuyItemList, imageURL)
    # 新しい画像のサイズを指定
    image_width = mm_to_pixels(52)
    image_height = mm_to_pixels(23)

    padding = mm_to_pixels(1)

    # 新しい画像を作成
    new_image = Image.new("RGB", (image_width, image_height), (255, 255, 255))

    # 描画オブジェクトを作成
    draw = ImageDraw.Draw(new_image)

    # 曜日、ホール、場所の表示
    font = ImageFont.truetype("GenEiNuGothic-EB.ttf", 130)
    place = circleInfofromWeb['HaichiStr']
    place = place.replace("曜日", "")
    text_position = (mm_to_pixels(16), mm_to_pixels(1))
    text_color = (0, 0, 0)  # 黒色
    draw.text(text_position, place, font=font, fill=text_color)

    # サークル名の表示
    circleName = circleInfofromWeb['Name']
    name_font_size = 120
    font = ImageFont.truetype("GenEiNuGothic-EB.ttf", name_font_size)
    position_width = mm_to_pixels(16)
    position_height = mm_to_pixels(7)
    # テキストの幅が画像の幅を超えているか確認
    while round(draw.textlength(circleName, font=font)) > image_width-position_width-padding:
        # テキストの幅が画像の幅を超えている場合、フォントサイズを小さくする
        name_font_size -= 1
        font = ImageFont.truetype("GenEiNuGothic-EB.ttf", name_font_size)
    text_color = (0, 0, 0)  # 黒色
    draw.text((position_width, position_height),
              circleName, font=font, fill=text_color)

    # 枠線の色を指定
    border_color = (0, 0, 0)  # 黒色
    border_width = mm_to_pixels(0.5)
    # 枠線を描画
    draw.rectangle([(0, 0), (image_width, image_height)],
                   outline=border_color, width=border_width)
    # サークル主の表示
    author = circleInfofromWeb['Author']
    font = ImageFont.truetype("GenEiNuGothic-EB.ttf", 40)
    text_position = (mm_to_pixels(16), mm_to_pixels(13))
    text_color = (0, 0, 0)  # 黒色
    draw.text(text_position, author, font=font, fill=text_color)

    # 画像をURLから取得して重ねる
    response = requests.get(imageURL, cookies=cookie, allow_redirects=False)
    overlay_image = Image.open(BytesIO(response.content))
    # 画像のリサイズ
    overlay_image = overlay_image.resize((mm_to_pixels(15), mm_to_pixels(23)))
    # 画像を貼り付ける位置を指定
    overlay_position = (0, 0)
    new_image.paste(overlay_image, overlay_position)

    # 優先度を色で表示
    priority = circleInfo["priority"]
    colorName = settings["priorityColor"]["priority" + str(priority)]
    colorHex = webcolors.name_to_hex(colorName)

    # 四角形の左上と右下の座標を指定
    rectangle_position = [(mm_to_pixels(0.5), mm_to_pixels(
        0.5)), (mm_to_pixels(4), mm_to_pixels(4.3))]
    # 四角形を描画
    draw.rectangle(rectangle_position, fill=colorHex)

    resultCounter = 0
    # 購入物の表示
    for itemIdNUm in BuyItemList:
        itemID = BuyItemList[itemIdNUm]
        item = itemList[itemID]
        itemName = item["name"]
        price = item["price"]
        count = 0
        userIDList = []
        userNameList = []
        for userList in item["users"]:
            count += userList["count"]
            userIDList.append(userList["uid"])

        for nameID in userIDList:
            userNameList.append(userInfo[nameID]["name"])

        if int(priority) != 0 and count != 0 and len(userNameList) != 0:
            text = f"単価{price}円 {itemName} {count}つ "
            for name in userNameList:
                text += f"{name} "
            # print(text)
            if text != "":
                item_font_size = 45
                font = ImageFont.truetype(
                    "GenEiNuGothic-EB.ttf", item_font_size)
                position_width = mm_to_pixels(16)
                position_height = mm_to_pixels(16+2*int(resultCounter))
                # テキストの幅が画像の幅を超えているか確認
                while round(draw.textlength(text, font=font)) > image_width-position_width-padding:
                    # テキストの幅が画像の幅を超えている場合、フォントサイズを小さくする
                    item_font_size -= 1
                    font = ImageFont.truetype(
                        "GenEiNuGothic-EB.ttf", item_font_size)
                text_color = (0, 0, 0)  # 黒色
                draw.text((position_width, position_height),
                          text, font=font, fill=text_color)
            resultCounter += 1
        else:
            pass
        if int(resultCounter) > 3:
            logging.warning(
                f"サークル{circleInfofromWeb['Name']}の購入物が3つ以上あります。すべて表示されていません。確認してください。")
    if resultCounter > 0:
        return new_image
    else:
        return "Noimage"

    # # 新しい画像を保存
    # new_image.save("generated_image_with_url.jpg")


def genDayBuylistImagePerHall(circleIDList, day, hall):
    # circleIDListの長さを30で割り、切り上げてpaperNumを計算
    paperNum = math.ceil(len(circleIDList) / 35)
    originHall = hall
    fileList = []
    for i in range(paperNum):

        # 新しい画像のサイズを指定
        image_width = mm_to_pixels(297)
        image_height = mm_to_pixels(210)

        # 新しい画像を作成
        new_image = Image.new(
            "RGB", (image_width, image_height), (255, 255, 255))

        # 描画オブジェクトを作成
        draw = ImageDraw.Draw(new_image)
        for x in range(35):
            try:
                path = os.path.join(
                    "out", "toBuyList", circleIDList[x+(i*35)] + ".png")
                circleImage = Image.open(path)
                position = settings["buyListPosition"][str(int(x)+1)]
                new_image.paste(circleImage, (mm_to_pixels(
                    position["x"]), mm_to_pixels(position["y"])))
            except IndexError:
                pass
            else:
                logging.error(f"サークル{circleIDList[x+(i*35)]}の画像がありません。")
        date = settings["date"][str(day)]
        hall = hall.replace("e", "東")
        hall = hall.replace("w", "西")
        font = ImageFont.truetype("GenEiNuGothic-EB.ttf", 220)
        text_position = (mm_to_pixels(5), mm_to_pixels(5))
        text_color = (0, 0, 0)  # 黒色
        draw.text(
            text_position, f"コミックマーケット  {day}日目({date})  {hall}", font=font, fill=text_color)

        baseSizemm = 4
        basePositionX = 170
        basePositionY = 10
        for y, priorityRank in enumerate(settings["priorityColor"]):
            priorityRank_jp = priorityRank.replace("priority", "優先度")
            if priorityRank != "priority0":
                colorName = settings["priorityColor"][priorityRank]
                colorHex = webcolors.name_to_hex(colorName)
                positionX = mm_to_pixels(
                    basePositionX) + ((y+1) * mm_to_pixels(20))
                positionY = mm_to_pixels(basePositionY)
                # 四角形の左上と右下の座標を指定
                rectangle_position = [(positionX, positionY),
                                      (positionX + mm_to_pixels(baseSizemm), positionY+mm_to_pixels(baseSizemm))]
                # 四角形を描画
                draw.rectangle(rectangle_position, fill=colorHex)

                # 凡例の表示
                text_color = (0, 0, 0)  # 黒色
                font = ImageFont.truetype("GenEiNuGothic-EB.ttf", 80)
                draw.text((positionX+mm_to_pixels(
                    baseSizemm+2), positionY), priorityRank_jp, font=font, fill=text_color)

        new_image.save(os.path.join("out", "buyListImage",
                       f"buylist_Day{day}_{originHall}_{i}.png"))
        fileList.append(os.path.join("out", "buyListImage",
                        f"buylist_Day{day}_{originHall}_{i}.png"))

    pdfFileName = os.path.join("out", f'buylist_day{day}_{originHall}.pdf')

    if fileList:  # fileListが空でないことを確認
        with open(pdfFileName, "wb") as f:
            f.write(img2pdf.convert(fileList))
    else:
        logging.warning(f"{pdfFileName} は空のためスキップされました。")


def mm_to_pixels(mm_size):
    # 1インチ = 25.4ミリメートル
    inches_per_mm = 25.4
    # ミリメートルからインチに変換
    inches_size = mm_size / inches_per_mm
    # ピクセル数の計算
    pixels_size = inches_size * 600

    return round(pixels_size)
