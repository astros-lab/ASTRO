import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()

NAME = os.environ['name']

def lchelp():
    embed = discord.Embed(title="Info", description="Welcome to LogiClicker, here are the available commands.", color=0x0000FF)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1209277476426088458/1224430071033368676/simple-hand-cursor-free-png.png?ex=661d765d&is=660b015d&hm=cfe25bbbd52e3f5ebe97ce4274306ec57e4e4972e9f2e3a4c4bfc3c2ce716378&")
    embed.add_field(name="Click", value="Clicks. $lc click", inline=False)
    embed.add_field(name="Shop", value="Shows available bulidings and upgrades. $lc shop", inline=False)
    embed.add_field(name="Upgrade", value="Upgrades a building type. $lc upgrade {upgrade name}", inline=False)
    embed.add_field(name="Buy", value="Buys a building. $lc buy {building name} {amount}", inline=False)
    embed.add_field(name="Stats", value="Shows stats. $lc stats", inline=False)
    return embed

def get_stats():
    global NAME
    with open(f"/home/{NAME}/workspace/ASTRO/stored_info/logiclicker.json") as lgc:
        lgc_stats = json.load(lgc)
        stats = lgc_stats["stats"]

    return stats

def update_stats():
    global NAME
    with open(f"/home/{NAME}/workspace/ASTRO/stored_info/logiclicker.json", "r+") as lgc:
        lgc_stats = json.load(lgc) 
        lgc_stats["stats"]["total"] += 1
        lgc_stats["stats"]["current"] += (1 * lgc_stats["multipliers"]["click"])
        lgc.seek(0)
        json.dump(lgc_stats, lgc, indent=4)

def upgrade(stat):
    global NAME
    stat = stat.lower()
    with open(f"/home/{NAME}/workspace/ASTRO/stored_info/logiclicker.json", "r+") as lgc:
        lgc_stats = json.load(lgc) 
        try:
            if lgc_stats["stats"]["current"] >= 10:
                lgc_stats["multipliers"][stat] *= 1
                lgc_stats["stats"]["current"] -= 10
        except Exception:
            return "Invalid upgrade."
        lgc.seek(0)
        json.dump(lgc_stats, lgc, indent=4)
        return discord.Embed(title=f"Upgraded {stat}.")

def interact(content):
    try:
        action = content[0]
        inputs = content[1:]
    except Exception:
        action = inputs = None

    output = None
    if action == "help":
        output = lchelp()
    elif action == "click":
        update_stats()
        embed = discord.Embed(title="Clicked!", description=f"Current amount of logic gates: {get_stats()['current']}")
        output = embed
    elif action == "upgrade":
        output = upgrade(inputs[0])
    else: output = discord.Embed(title="Welcome to LogiClicker!", description="For help, use '$lc help'.", colour = 0x00FF00)
        
    return output
