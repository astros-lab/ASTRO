import discord, os

def main(attributes):
    commands = [i.name.replace(".py", "") for i in os.scandir("./src/commands") if i.is_file()]

    embed = discord.Embed(title="Commands:", color=0x6bd160)
    embed.add_field(name="**Programmed Commands:**",value=" **|** ".join(commands), inline=False)        
    return embed