import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import functions
from io import StringIO

load_dotenv()

TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix="", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    game = discord.Game("Circuit Maker π")
    await bot.change_presence(activity=game)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    content = str(message.content).lower()
    if content == "hi" or "<@1213876646315171841>" in content: 
        if str(message.author) != "ASTRO#8574":
            if str(message.author.display_name).lower() != "none":
                await message.channel.send(f"hi {str(message.author.display_name).lower()}")
            else:
                await message.channel.send(f"hi {str(message.author).lower()}")

@bot.tree.command(name="help", description="Shows available commands and what they do")
async def help(message: discord.Interaction):
    helpMessage = """```Commands:
/dpaste: Returns raw dpaste link
/text_cm2: Returns a save string with your text```"""

    await message.response.send_message(helpMessage)

@bot.tree.command(name="say", description="make bot say something")
@app_commands.describe(string="thing")
async def say(message: discord.Interaction, string: str):
    await message.response.send_message(string)

@bot.tree.command(name="praise", description="praise something")
@app_commands.describe(thing="thing to praise")
async def praise(message: discord.Interaction, thing: str):
    praise1 = f"{thing} is the best, everybody should pray to {thing}"
    praise2 = f"We all live to love {thing}"
    praise3 = f"We must all pray to {thing}"
    praise4 = f"Nobody should disrespect {thing}"
    praise5 = f"ALL HAIL {thing.upper()}"
    praises = [praise1, praise2, praise3, praise4, praise5]
    await message.response.send_message(random.choice(praises))

@bot.tree.command(name="dpaste", description="get a raw dpaste link")
@app_commands.describe(input="text you want to send to dpaste")
async def dpaste(message: discord.Interaction, input: str):
    link = functions.dpaste(input)
    await message.response.send_message(link)
    
@bot.tree.command(name="text_cm2", description="create text in cm2")
@app_commands.describe(text="text to convert", step="space between text, default:0.5")
async def text_cm2(message: discord.Interaction, text: str, step: float=0.5):
    output = f"{functions.make_text(text, step)}"
    if len(output) > 1000:
        buffer = StringIO(output)
        f = discord.File(buffer, filename="output.txt")
        await message.response.send_message(file=f)
    await message.response.send_message(f"```{output}```")

@bot.tree.command(name="decoder_generator", description="generate a decoder")
@app_commands.describe(inputs="amount of inputs")
async def decoder_generator(message: discord.Interaction, inputs: int):
    output = f"{functions.generate_decoder(inputs)}"
    if len(output) > 1000:
        buffer = StringIO(output)
        f = discord.File(buffer, filename="output.txt")
        await message.response.send_message(file=f)
    await message.response.send_message(f"```{output}```")

bot.run(TOKEN)
