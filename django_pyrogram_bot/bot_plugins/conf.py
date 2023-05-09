from pyrogram import Client, filters

from decouple import config

api = 19663899
hash = "af0b19d19293e57b1b74cabcf6dcbbd6"
bot = "5029205621:AAGWw2fkjLpLOT1m2nXVNB-rPoEgJe0Q8T0"
owner = str("675889933 406793949 506779415").split()
group = "-1001644715256"
block = "1 2 3"
try:
    api = config("api", cast=int)
    hash = config("hash")
    bot = config("bot")
    owner = str(config("owner", default="1 2")).split()
    group = config("group")

    block = str(config("Block", default="1 2")).split()
except:
    print("error config")
#app = Client("bot", api_id=api, api_hash=hash, bot_token=bot)
download_dir = "download"
codec_dir = "codec"


