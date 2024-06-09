import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import json
import io
from io import StringIO
import botcommands
import cm2image
import cm2video
import importlib
import sys

load_dotenv()

TOKEN = os.environ['TOKEN']
NAME = os.environ['name']

bot = commands.Bot(command_prefix="", intents = discord.Intents.all())

converting_video = False

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

# @bot.event
# async def on_message(message):
#     def split_cmd(msg: str):
#         cmdsplit = msg.split(" ")
#         return cmdsplit[0], cmdsplit[1:]

#     if message.author == bot.user or message.author.bot:
#         return

#     content = message.content
#     lowered_content = str(content).lower()
#     command, inputs = split_cmd(content)

#     if command[1:] != "" and command[0] == "$":
#         cmd = command[1:]
#         cmdlist = [i.name.replace(".py", "") for i in os.scandir("./src/commands")]
        
#         blocked = ["@everyone", "@here"]
#         if any(ping in content for ping in blocked) or (cmd not in cmdlist):
#             return

#         attributes = {
#             "message": message,
#             "inputs": inputs,
#             "lowered": lowered_content
#         }
        
#         if cmd in sys.modules:
#             func = importlib.reload(sys.modules[cmd])
#         else:
#             func = importlib.import_module(f"commands.{cmd}")
#         output = func.main(attributes)

#         try:
#             if isinstance(output, discord.Embed):
#                 await message.channel.send(embed=output)
#                 return
#             await message.channel.send(output)
#         except:
#             await message.channel.send("Failed to send message.")
        


@bot.event
async def on_message(message):
    global NAME

    if message.author == bot.user or message.author.bot:
        return
    
    lowered_content = str(message.content).lower()

    if (str(message.author.id) == "844957879714840597" 
        and str(message.channel.id) == "1187662902610636910"
        and str(message.guild.id) == "956406294263242792") and any(attachment.width != None
        or attachment.height != None
        or attachment.content_type.startswith("video/")
        for attachment in message.attachments):
        if "me and who" in lowered_content or "me n who" in lowered_content:
            await message.reply("us")
        else:
            await message.reply("literally me")
        return

    if str(message.author.id) == "665724183094755359" and random.randint(1, 100) == 1 or "​" in message.content:
        await message.add_reaction("<:smug:1187680194727772211>")

    content = message.content
    command, inputs = botcommands.get_command(content)
    joinedinputs = " ".join(inputs)
    if command != "":
        if "@here" in content or "@everyone" in content: return
        elif command[0] == "$":
            action = command[1:]

            extracmds = []

            commands = json.load(open(f"/home/{NAME}/workspace/ASTRO/storage/commands.json", "r"))
            cmd_list = commands["commands"]
            for i in range(len(cmd_list)):
                extracmds.append(cmd_list[i]['command'])

            commands = ["$binary {number/string}", "$integer {binary}", "$ascii {binary}", "$embed", "$skmtime", "$astrotime"]

            if action == "help":
                embed = discord.Embed(title="Commands:", color=0x6bd160)
                embed.add_field(name="**Programmed Commands:**",value=" **|** ".join(commands), inline=False) 
                embed.add_field(name="**Keyword Commands:**",value=" **|** ".join('$' + i for i in extracmds), inline=False)           
                output = embed
            elif action == "embed":
                pfp_ASTRO = "https://cdn.discordapp.com/avatars/1213876646315171841/ace5c28bc758e7eeeddf76d99f736e4e.png?size=4096"
                embed = discord.Embed(title="some title", description="some description", colour=0xFF0000)
                embed.add_field(name="some name", value="some value", inline=False)
                embed.set_image(url=pfp_ASTRO)
                embed.set_footer(text="some footer", icon_url=pfp_ASTRO)
                embed.set_author(name="some name", url=pfp_ASTRO, icon_url=pfp_ASTRO)
                embed.set_thumbnail(url=pfp_ASTRO)
                output = embed
            elif action == "binary":
                try:
                    embed = discord.Embed(title="Integer to Binary:")

                    value = int("".join(inputs))
                    embed.add_field(name="", value=f"```{bin(value)[2:]}```")
                except Exception:
                    embed = discord.Embed(title="Ascii to Binary:")

                    ascii_val = []
                    value = " ".join(inputs)
                    for c in value:
                        val = bin(ord(c))
                        ascii_val.append(val[2:])
                    ascii_joined = " ".join(ascii_val)
                    embed.add_field(name="", value=f"```{ascii_joined}```")

                output = embed
            elif action == "integer":
                embed = discord.Embed(title="Binary to Integer:")
                try:
                    numbers = []
                    for n in inputs:
                        numbers.append(str(int(n, 2)))

                    nums = " ".join(numbers)
                    print(nums, numbers)
                    embed.add_field(name="", value=f"```{nums}```")

                    output = embed
                except Exception:
                    output = "Error. Input must be binary."
            elif action == "ascii":
                embed = discord.Embed(title="Binary to Ascii:")
                try:
                    characters = []
                    for c in inputs:
                        characters.append(chr(int(c, 2)))
                    chars_joined = "".join(characters)
                    if '`' in chars_joined:
                        embed.add_field(name="", value=f"nuh uh dont even try")
                    else:
                        embed.add_field(name="", value=f"```{chars_joined}```")
                except Exception:
                    output = "Error. Input must be binary."

                output = embed    
            elif action == "say" and str(message.author) == "gaming4cats":
                try:
                    replied_message = await message.channel.fetch_message(message.reference.message_id)
                    await message.delete()
                    await replied_message.reply(joinedinputs, mention_author=False)
                    return
                except:
                    await message.delete()
                    output = joinedinputs
            elif action == "react" and str(message.author) == "gaming4cats":               
                message_id = int(inputs[0].split('/')[-1])
                
                await message.delete()

                try:
                    reacted_message = await message.channel.fetch_message(message_id)
                    await reacted_message.add_reaction(inputs[1])
                except:
                    pass

                return
            elif action == "add" and str(message.author) == "gaming4cats":
                name = inputs[0]
                out = inputs[1:]
                data = {
                    "command":name,
                    "output": " ".join(out)
                }
                botcommands.json_add(data, f"/home/{NAME}/workspace/ASTRO/storage/")
                output = f"Created command: {name}\nOutput: {' '.join(out)}"
            elif action == "log" and str(message.author) == "gaming4cats":
                with open(f"/home/{NAME}/workspace/ASTRO/storage/dollarLog.txt", "r+") as log:
                    output = "Recent $ commands\n" + "".join(log.readlines()[-5:])
            elif action == "skmtime":
                output = botcommands.melbournetime()
            elif action == "astrotime":
                output = botcommands.torontotime()
            elif action in extracmds:
                output = cmd_list[extracmds.index(action)]['output']
            else:
                return


            with open(f"/home/{NAME}/workspace/ASTRO/storage/dollarLog.txt", "a+") as log:
                if str(message.author) != "gaming4cats":
                    if joinedinputs == '':
                        log.write(f"{message.author} did command ``{action}``\n")
                    else:
                        log.write(f"{message.author} did command ``{action}``, inputs: ``{joinedinputs}``\n")

            try:
                if isinstance(output, discord.Embed):
                    await message.channel.send(embed=output)
                    return
                await message.channel.send(output)
            except discord.errors.HTTPException:
                await message.channel.send("Error sending message.")

@bot.tree.command(name="dpaste", description="get a raw dpaste link")
@app_commands.describe(input="text you want to send to dpaste")
async def dpaste(message: discord.Interaction, input: str):
    link = botcommands.dpaste(input)
    await message.response.send_message(link)

@bot.tree.command(name="decoder_generator", description="generate a decoder")
@app_commands.describe(inputs="amount of inputs")
async def decoder_generator(message: discord.Interaction, inputs: int):
    if inputs > 10:
        await message.response.send_message("too much")
    else:
        output = f"{botcommands.generate_decoder(inputs)}"
        if len(output) > 1000:
            buffer = StringIO(output)
            f = discord.File(buffer, filename="output.txt")
            await message.response.send_message(file=f)
        else:
            await message.response.send_message(f"```{output}```")

@bot.tree.command(name="textcm2", description="create text in cm2")
@app_commands.describe(text="text to convert", step="space between text, default:0.5")
async def textcm2(message: discord.Interaction, text: str, step: float=0.5):
    output = f"{botcommands.make_text(text, step)}"
    if len(output) > 1000:
        buffer = StringIO(output)
        f = discord.File(buffer, filename="output.txt")
        await message.response.send_message(file=f)
    await message.response.send_message(f"```{output}```")

@bot.tree.command(name="imagecm2", description="Convert an Image to a CM2 save string.")
@app_commands.describe(image="Image to convert", maxraw="Maximum raw size", spacingfactor="Spacing factor, example 2 means spacing of 0.5 studs")
async def imagecm2(message: discord.Interaction, image: discord.Attachment, maxraw: int=200_000, spacingfactor: int=1):
    await message.response.send_message("Converting...")
    imBytes = await image.read()
    save = cm2image.convert_image(io.BytesIO(imBytes), maxraw, spacingfactor, message.user.name)
    await message.edit_original_response(content=save)

@bot.tree.command(name="videocm2", description="Convert a video to a CM2 save string.")
@app_commands.describe(video="Video to convert", framedivision="Divides the frames, 2 means that 60fps would be 30fps", tps="Ticks between frames, 2+ recommended", height="Height of the video", threshold="Pixel brightness to choose black or white")
async def videocm2(message: discord.Interaction, video: discord.Attachment, framedivision: int=2, tps: int=2, height: int=16, threshold: int=200):
    global NAME, converting_video

    if converting_video:
        await message.response.send_message("Currently converting video, please wait and try again.")
        return
    
    converting_video = True

    if video.content_type.startswith("video"):
        integers = [framedivision, tps, height, threshold]
        names = ["fps", "tps", "height", "threshold"]
        errors = []
        if height > 32 and str(message.user.name) != "gaming4cats":
            errors.append("height over 32")
        if threshold > 255:
            errors.append("threshold over 255")
        for i, integer in enumerate(integers):
            if integer < 1:
                errors.append(f"{names[i]} under 1")

        if errors != []:
            await message.response.send_message("ERROR: " + ", ".join(errors))
            converting_video = False
            return
        
        await message.response.send_message("Converting...")

        await video.save(f"/home/{NAME}/workspace/ASTRO/storage/frames/" + video.filename)
        path = f"/home/{NAME}/workspace/ASTRO/storage/frames/" + video.filename
        save = cm2video.convertvideo(path, fps=framedivision, tps=tps, height=height, threshold=threshold)
        await message.edit_original_response(content=save)
    else:
        await message.response.send_message("Must be a video file.")  

    converting_video = False

bot.run(TOKEN)
