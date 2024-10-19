import discord
from discord.ext import tasks
from discord import app_commands
import time, os, random
from dotenv import load_dotenv

load_dotenv()

client = discord.Client(
  intents=discord.Intents.default(),
 activity=discord.Game("異変解決")
)
tree=app_commands.CommandTree(client)

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

omikuzi_list: list = ["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶", "大福吉"]
# 5, 15, 20, 30, 20, 15, 5, 1

@tree.command(name="omikuzi", description="今日の運勢を占うわよ")
async def omikuzi(interaction: discord.Interaction):
  fortune: str
  description: str
  color: int

  random.seed(time.time())
  random_int = random.randint(0, 111)

  if random_int < 5:
    fortune = omikuzi_list[0]
    description = "やったわね！大吉よ！"
    color = 0xff0000
  elif random_int < 20:
    fortune = omikuzi_list[1]
    description = "中吉ね！なんかいいことあるかもしれないわ！"
  elif random_int < 40:
    fortune = omikuzi_list[2]
    description = "小吉よ！"
  elif random_int < 70:
    fortune = omikuzi_list[3]
    description = "吉ね！今日もいつも通りの一日になりそうね"
  elif random_int < 90:
    fortune = omikuzi_list[4]
    description = "末吉よ。ちょっとだけいいことがあるかもね"
  elif random_int < 105:
    fortune = omikuzi_list[5]
    description = "凶ね...めげないでね..."
  elif random_int < 110:
    fortune = omikuzi_list[6]
    description = "まずいわ...大凶よ...気をつけてね..."
  elif random_int < 111:
    fortune = omikuzi_list[7]
    description = "これは...なんかよくわからないけどおめでとう...？"
    color = 0xffff00

  omikuzi_embed = discord.Embed(
    title=fortune,
    description=description,
    color=color
  )
  channel = client.get_channel(CHANNEL_ID)
  await interaction.response.send_message(embed=omikuzi_embed)

@client.event
async def on_ready():
  await tree.sync()
  print('Hakurei Shrine Bot is ready')

client.run(TOKEN)