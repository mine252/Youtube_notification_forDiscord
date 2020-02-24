import discord
from discord.ext import tasks,commands
import asyncio
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

'''
15,16,26,27,48行目を各自書き換え
'''

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "Developper　KEY　API"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
timestamp=""

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'Discord Access Token'
CHANNEL_ID="Discord test chat channelID"
# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')
    await loop()


async def loop():
  while True:
    global timestamp
    res = youtube.search().list(
      part="snippet",
      channelId="Youtube Channel ID",
      type="video",
      eventType="live",
    ).execute()
            #チャンネルがライブ状態のときの処理
            
    try:
      if res["items"][0]["snippet"]["liveBroadcastContent"]:
          if not res["items"][0]["snippet"]["publishedAt"]==timestamp:
            channel = client.get_channel(CHANNEL_ID)
            await channel.send('https://www.youtube.com/watch?v='+res["items"][0]["id"]["videoId"])
            timestamp=res["items"][0]["snippet"]["publishedAt"]
            pass
          else:
            print("一回通知したﾖ")
            pass
    except IndexError:
          # 何も放送していない場合
          print("放送していないﾖ")
          pass
    await asyncio.sleep(60)
@client.event
async def on_message(message): 
    if message.content.startswith('!SHUTDOWN_BOT'):#!SHUTDOWN_BOTが入力されたら強制終了
        await client.logout()


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
