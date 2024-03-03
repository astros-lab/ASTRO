import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

load_dotenv()

TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    game = discord.Game("testing")
    await bot.change_presence(activity=game)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="sneeze", description="sneeze")
async def sneeze(interaction: discord.Interaction):
    o = "o"
    await interaction.response.send_message(f"ach{o * random.randint(1,25)}")

bot.run(TOKEN)
