from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import json
import logging
import webcolors

# ログの設定
logging.basicConfig(filename='example.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
logging.info("画像生成のための設定を読み込みました。")

cookie = settings["url"]["webMapInfo"]["cookie"]


def genCircleImage(circleInfofromWeb, circleInfo, BuyItemList, itemList, imageURL, userInfo):
    # print(circleInfofromWeb, itemInfo, BuyItemList, imageURL)
    # 新しい画像のサイズを指定
    image_width = mm_to_pixels(52)
    image_height = mm_to_pixels(23)

    # 新しい画像を作成
    new_image = Image.new("RGB", (image_width, image_height), (255, 255, 255))

    # 描画オブジェクトを作成
    draw = ImageDraw.Draw(new_image)

    # 曜日、ホール、場所の表示
    font = ImageFont.truetype("meiryo.ttc", 130)
    place = circleInfofromWeb['HaichiStr']
    place = place.replace("曜日", "")
    text_position = (mm_to_pixels(16), 0)
    text_color = (0, 0, 0)  # 黒色
    draw.text(text_position, place, font=font, fill=text_color)

    # サークル名の表示
    circleName = circleInfofromWeb['Name']
    name_font_size = 120
    font = ImageFont.truetype("meiryo.ttc", name_font_size)
    position_width = mm_to_pixels(16)
    position_height = mm_to_pixels(6)
    # テキストの幅が画像の幅を超えているか確認
    while round(draw.textlength(circleName, font=font)) > image_width-position_width:
        # テキストの幅が画像の幅を超えている場合、フォントサイズを小さくする
        name_font_size -= 1
        font = ImageFont.truetype("meiryo.ttc", name_font_size)
    text_color = (0, 0, 0)  # 黒色
    draw.text((position_width, position_height),
              circleName, font=font, fill=text_color)

    # サークル主の表示
    author = circleInfofromWeb['Author']
    font = ImageFont.truetype("meiryo.ttc", 40)
    text_position = (mm_to_pixels(16), mm_to_pixels(12))
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
            text = f"単価{price}円 {itemName}{count}つ "
            for name in userNameList:
                text += f"{name} "
            # print(text)
            if text != "":
                item_font_size = 20
                font = ImageFont.truetype("meiryo.ttc", item_font_size)
                position_width = mm_to_pixels(16)
                position_height = mm_to_pixels(15+1.5*int(resultCounter))
                # テキストの幅が画像の幅を超えているか確認
                while round(draw.textlength(text, font=font)) > image_width-position_width:
                    # テキストの幅が画像の幅を超えている場合、フォントサイズを小さくする
                    item_font_size -= 1
                    font = ImageFont.truetype("meiryo.ttc", item_font_size)
                text_color = (0, 0, 0)  # 黒色
                draw.text((position_width, position_height),
                          text, font=font, fill=text_color)
            resultCounter += 1
        else:
            pass
        if int(resultCounter) > 5:
            logging.warning(
                f"サークル{circleInfofromWeb['Name']}の購入物が6つ以上あります。すべて表示されていません。確認してくさい。")
    if resultCounter != 0:
        return new_image
    else:
        return "Noimage"

    # # 新しい画像を保存
    # new_image.save("generated_image_with_url.jpg")


def mm_to_pixels(mm_size):
    # 1インチ = 25.4ミリメートル
    inches_per_mm = 25.4
    # ミリメートルからインチに変換
    inches_size = mm_size / inches_per_mm
    # ピクセル数の計算
    pixels_size = inches_size * 600

    return round(pixels_size)
