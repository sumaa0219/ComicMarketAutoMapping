import openpyxl
import webcolors
import json

# 設定ファイルの読み込み
with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)

# ワークブックを読み込む
workbook = openpyxl.load_workbook('c103.xlsm')

# 名前'_a09a'が定義されたセルを探す
if '_シ37b' in workbook.defined_names:
    sheet_title, cell_coordinate = next(
        workbook.defined_names['_シ27a'].destinations)
    target_cell = workbook[sheet_title][cell_coordinate]

    # セルの色を赤に変更
    target_cell.fill = openpyxl.styles.PatternFill(
        start_color='FF0000', end_color='FF0000', fill_type='solid')

    # 保存
    workbook.save('c103_map.xlsx')
