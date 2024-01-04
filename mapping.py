import openpyxl
import webcolors
import json
import logging

# ログの設定
logging.basicConfig(filename='generate.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# 設定ファイルの読み込み
with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
logging.info("マッピングのための設定を読み込みました。")


def mapping(workbook, circlePlace, priority):
    colorName = settings["priorityColor"]["priority" + str(priority)]
    circlePlace = circlePlace
    colorHex = webcolors.name_to_hex(colorName)
    colorHex = colorHex[1:]

    # 名前が定義されたセルを探す
    if circlePlace in workbook.defined_names:
        sheet_title, cell_coordinate = next(
            workbook.defined_names[circlePlace].destinations)
        target_cell = workbook[sheet_title][cell_coordinate]

        # セルの色を変更
        target_cell.fill = openpyxl.styles.PatternFill(
            start_color=colorHex, end_color=colorHex, fill_type='solid')

        logging.debug(
            f"mapping: {circlePlace} {colorName} {priority}: {str(priority)}")
    elif circlePlace not in workbook.defined_names:
        logging.warning(f"mapping: {circlePlace} は定義されていません。")

    return workbook
