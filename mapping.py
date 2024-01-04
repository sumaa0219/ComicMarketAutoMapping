import openpyxl
import webcolors
import json

# 設定ファイルの読み込み
with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
print("settings loaded")


def mapping(workbook, circlePlace, priority, outFileName):
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

        print("mapping: " + circlePlace + " " +
              colorName, "priority: " + str(priority))

    return workbook
