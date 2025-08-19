import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import datetime
import json
import requests
import mapGen
import listGen
from PIL import Image
import PyPDF2
import os
from setup import MapImageDownloader
from areaImage import genAllAreaMapImage
from imgGen import png_to_pdf


load_dotenv()
TOKEN = os.environ['token']
logServer = os.environ['logServer']
logChannel = os.environ['logChannel']

intents = discord.Intents.all()  # 適当に。
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

guildID = None
channelID = None

with open('settings.json', 'r', encoding="utf-8") as json_file:
    settings = json.load(json_file)
    

# マップ画像ダウンローダーの初期化
downloader = MapImageDownloader()
# 全エリア・全日の自動ダウンロード
downloader.download_all_areas()

genAllAreaMapImage()



@client.event
async def on_ready():
    # await send_console("起動しました")
    await tree.sync()  # スラッシュコマンドを同期
    print("起動しました")


@tree.command(name="generate", description="地図と買い物リストを生成します")
async def generate(interaction: discord.Interaction, day: int):
    await interaction.response.defer()
    # 設定ファイルの読み込み

    # cookie = settings["url"]["cookie"]

    circleInfoJson = requests.get(
        str(settings["url"]["webapp"]["domainOrigin"] + settings["url"]["webapp"]["circleList"]), allow_redirects=False).json()
    print("サークル情報の読み込みが完了しました。")

    itemInfoJson = requests.get(
        str(settings["url"]["webapp"]["domainOrigin"] + settings["url"]["webapp"]["itemList"]), allow_redirects=False).json()
    print("購入物情報の読み込みが完了しました。")

    userInfoJson = requests.get(
        str(settings["url"]["webapp"]["domainOrigin"] + settings["url"]["webapp"]["user"]), allow_redirects=False).json()
    print("ユーザー情報の読み込みが完了しました。")

    Info, itemIDperCircle = mapGen.genCircleInfoList(
        circleInfoJson, itemInfoJson)

    listGen.circleInfoImageGen(
        Info, itemInfoJson, itemIDperCircle, day, userInfoJson)
    print("サークル情報の画像生成が完了しました。")
    for hallOption in settings["block"]:
        hall = settings["block"][hallOption]
        mapGen.mapGen(hall, Info, day,
                      f"out/maplist/map_day{day}_{hall}.png")
        png_to_pdf(
            f"out/maplist/map_day{day}_{hall}.png", f"out/maplist/map_day{day}_{hall}.pdf")
        os.remove(f"out/maplist/map_day{day}_{hall}.png")
        # print(Info, itemIDperCircle)
        aaaa = listGen.buylistImageGen(Info, day, hall)

        pathlist = [os.path.join("out", "maplist", f"map_day{day}_{hall}.pdf"), os.path.join(
            "out", "buylist", f"buylist_day{day}_{hall}.pdf")]
        merge_pdfs(pathlist, f"out/day{day}_{hall}.pdf")

    global guildID, channelID
    guildID = interaction.guild.id
    channelID = interaction.channel.id

    await interaction.followup.send(content=f"{day}日目の地図と購入リストを生成しました")


@tree.command(name="send", description="地図と買い物リストを送信します")
async def send(interaction: discord.Interaction, day: int):
    global guildID, channelID
    # outディレクトリのフォルダー以外を取得する
    # outディレクトリのパス
    out_dir = 'out'
    # outディレクトリ内のフォルダー以外のファイルを取得
    file_objects = []
    await interaction.response.defer()
    if guildID is None or channelID is None:
        guildID = interaction.guild.id
        channelID = interaction.channel.id

    for hallNum in settings["block"].keys():
        hall = settings["block"][hallNum]
        pathlist = os.path.join(out_dir, f"day{day}_{hall}.pdf")
        file_object = discord.File(pathlist)
        guild = client.get_guild(guildID)
        channel = guild.get_channel(channelID)
        await channel.send(f" ", file=file_object)

    await interaction.followup.send(content="地図と購入リストを送信しました")


async def send_console(message):
    guild = client.get_guild(int(logServer))
    channel = guild.get_channel(int(logChannel))
    await channel.send(message)


def merge_pdfs(pdf_list, output_pdf):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        if os.path.exists(pdf):
            merger.append(pdf)
    merger.write(output_pdf)
    merger.close()


client.run(TOKEN)
