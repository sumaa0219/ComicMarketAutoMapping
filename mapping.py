import openpyxl
import webcolors
import json

# 設定ファイルの読み込み
with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)


def mapping(excelFileName, circlePlace, rank, outFileName):
    # ワークブックを読み込む
    workbook = openpyxl.load_workbook(excelFileName)
    colorName = settings["rankColor"]["rank" + str(rank)]

    colorHex = webcolors.name_to_hex(colorName)
    # 名前'_a09a'が定義されたセルを探す
    if circlePlace in workbook.defined_names:
        sheet_title, cell_coordinate = next(
            workbook.defined_names[circlePlace].destinations)
        target_cell = workbook[sheet_title][cell_coordinate]

        # セルの色を変更
        target_cell.fill = openpyxl.styles.PatternFill(
            start_color=colorHex, end_color=colorHex, fill_type='solid')

        # 保存
        workbook.save(outFileName)
