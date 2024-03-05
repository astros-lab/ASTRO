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
NAME = os.environ['name']

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
    lowered_content = str(message.content).lower()
    if lowered_content == "hi" or "<@1213876646315171841>" in lowered_content: 
        if str(message.author) != "ASTRO#8574":
            await message.channel.send("hi")

    content = message.content
    command, inputs = functions.get_command(content)
    joinedinputs = " ".join(inputs)
    if command != "":
        if "@here" in content or "@everyone" in content:
                pass
        elif command[0] == "$" and str(message.author) != "ASTRO#8574":
            action = command[1:]

            extracmds = {}

            global NAME
            with open(f"/home/{NAME}/workspace/ASTRO/commands.txt", "r+") as cmdsText:
                cmds = cmdsText.read()
                if cmds != "":
                    lines = cmds.split(";")
                    for i in range(len(lines)):
                        if lines[i] != "":
                            cmd = lines[i].split(",")
                            cmdName = cmd[0]
                            cmdOut = cmd[1]
                            # print(cmdName, cmdOut, cmd)
                            extracmds[cmdName] = cmdOut

            # print(extracmds, message.author, command, action, inputs, joinedinputs)
            
            if action == "help":
                output = f"'$' commands: praise, {', '.join(extracmds.keys())}"
            elif action == "praise":
                thing = joinedinputs
                praise1 = f"{thing} is the best, everybody should pray to {thing}"
                praise2 = f"We all live to love {thing}"
                praise3 = f"We must all pray to {thing}"
                praise4 = f"Nobody should disrespect {thing}"
                praise5 = f"ALL HAIL {thing.upper()}"
                praises = [praise1, praise2, praise3, praise4, praise5]
                output = random.choice(praises)
            elif action == "add" and str(message.author) == "gaming4cats":
                name = inputs[0]
                out = inputs[1:]
                with open(f"/home/{NAME}/workspace/ASTRO/commands.txt", "a+") as cmds:
                    cmds.write(f"{name},{' '.join(out)};")
                    # print(f"{name},{' '.join(out)}\n")
                output = f"Created command: {name}\nOutput: {' '.join(out)}"
            else:
                if action in extracmds.keys():
                    output = extracmds[action]
                else:
                    output = "Invalid command, see $help."
            await message.channel.send(output)

@bot.tree.command(name="say", description="make bot say something")
@app_commands.describe(string="thing")
async def say(message: discord.Interaction, string: str):
    await message.response.send_message(string)

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
    if inputs > 10:
        await message.response.send_message("too much")
    else:
        output = f"{functions.generate_decoder(inputs)}"
        if len(output) > 1000:
            buffer = StringIO(output)
            f = discord.File(buffer, filename="output.txt")
            await message.response.send_message(file=f)
        else:
            await message.response.send_message(f"```{output}```")

@bot.tree.command(name="suggest", description="suggest an idea for the bot")
@app_commands.describe(topic="what do you want to suggest")
async def suggest(message: discord.Interaction, topic: str):
    global NAME
    with open(f"/home/{NAME}/workspace/ASTRO/suggestions.txt", "a+") as s:
        s.write(f"Name: {message.user}, Suggestion: {topic}\n")
    await message.response.send_message("Added suggestion")

bot.run(TOKEN)
