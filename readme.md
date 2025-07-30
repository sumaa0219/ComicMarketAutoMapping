# コミケ自動宝の地図作成DiscordBot
## セットアップ
使用には専用サーバーが必要です。
- setting.jsonを変える
    ```
    "url": {
        "webapp": {
            "domainOrigin":""
        },
        "mapImage":{
            "sampleURL":""（マップの画像のURL）
        },
        "cookie": {
            ".ASPXAUTH": ""（ログインセッションcookie）
        },
        "block": {
            "1": "e456",
            "2": "e7",
            "3": "w12",
            "4": "s12"
        },
        "date": {
            "1": "土",
            "2": "日"
        },
      }
    ```
- .envを.env.sampleを参考に作成
  ```
    token=str(discord)
    logServer=str(discord)
    logChannel=str(discord)
    ```
- docker起動
  - ``docker compose up -d``