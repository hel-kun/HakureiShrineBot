import discord
from discord.ext import tasks
from discord import app_commands
import time, os, random
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv("TOKEN")

client = discord.Client(
  intents=discord.Intents.default(),
  activity=discord.Game("異変解決")
)
tree=app_commands.CommandTree(client)

omikuji_list: list = json.load(open('src/omikuji.json', 'r', encoding="utf-8"))

def get_omikuji() -> dict:
  omikuji: dict = {}
  time.sleep(0.001)
  random.seed(time.time() * 1000)
  total_probability = sum(item['probability'] for item in omikuji_list)
  pick = random.uniform(0, total_probability)
  current = 0
  for item in omikuji_list:
    current += item['probability']
    if current > pick:
      omikuji = item
      break
  return omikuji

@tree.command(name="omikuji", description="今日の運勢を占うわよ")
async def omikuji(interaction: discord.Interaction):
  omikuji: dict = get_omikuji()

  omikuzi_embed = discord.Embed(
    title=omikuji['name'],
    description=random.choice(omikuji['description']),
    color=int(omikuji['color'], 0)
  )
  await interaction.response.send_message(embed=omikuzi_embed)

@tree.command(name="omikuji_x10", description="10回連続でおみくじを引くわよ")
async def omikuji_x10(interaction: discord.Interaction):
  omikuji_x10_embed: list = []
  for i in range(10):
    omikuji: dict = get_omikuji()
    omikuji_x10_embed.append(discord.Embed(
      title=omikuji['name'],
      description=random.choice(omikuji['description']),
      color=int(omikuji['color'], 0)
    ))
  
  await interaction.response.send_message(embeds=omikuji_x10_embed)

@client.event
async def on_ready():
  await tree.sync()
  print('Hakurei Shrine Bot is ready')

client.run(TOKEN)
