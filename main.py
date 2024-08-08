import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import datetime
import json
import requests
import mapGen
import listGen


load_dotenv()
TOKEN = os.environ['token']
logServer = os.environ['logServer']
logChannel = os.environ['logChannel']

intents = discord.Intents.all()  # 適当に。
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    # await send_console("起動しました")
    await tree.sync()  # スラッシュコマンドを同期
    print("起動しました")


@tree.command(name="generate", description="地図と買い物リストを生成します")
async def generate(interaction: discord.Interaction):
    await interaction.response.defer()
    # 設定ファイルの読み込み
    with open('settings.json', 'r', encoding="utf-8") as json_file:
        settings = json.load(json_file)

    # cookie = settings["url"]["cookie"]

    circleInfoJson = requests.get(
        "https://com-fork-c104.vercel.app/api/db/circle", allow_redirects=False).json()
    print("サークル情報の読み込みが完了しました。")

    itemInfoJson = requests.get(
        "https://com-fork-c104.vercel.app/api/db/item", allow_redirects=False).json()
    print("購入物情報の読み込みが完了しました。")

    userInfoJson = requests.get(
        "https://com-fork-c104.vercel.app/api/db/user", allow_redirects=False).json()
    print("ユーザー情報の読み込みが完了しました。")

    Info, itemIDperCircle = mapGen.genCircleInfoList(
        circleInfoJson, itemInfoJson)

    for day in [1, 2]:
        listGen.circleInfoImageGen(
            Info, itemInfoJson, itemIDperCircle, day, userInfoJson)
        print("サークル情報の画像生成が完了しました。")
        for hallOption in settings["block"]:
            hall = settings["block"][hallOption]
            mapGen.mapGen(hall, Info, day, f"out/map_day{day}_{hall}.png")

            # print(Info, itemIDperCircle)

            pathlist = listGen.buylistImageGen(Info, day, hall)

    # outディレクトリのフォルダー以外を取得する
    # outディレクトリのパス
    out_dir = 'out'
    # outディレクトリ内のフォルダー以外のファイルを取得
    files = [f for f in os.listdir(
        out_dir) if os.path.isfile(os.path.join(out_dir, f))]

    await interaction.followup.send("地図と購入リストを生成しました", files=files)


async def send_console(message):
    guild = client.get_guild(int(logServer))
    channel = guild.get_channel(int(logChannel))
    await channel.send(message)


client.run(TOKEN)
