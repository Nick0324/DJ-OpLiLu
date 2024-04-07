import functions
import discord
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(intents=intents, command_prefix="!")


@client.command()
async def join(ctx):
    role = discord.utils.get(ctx.author.roles, name="dj")
    if role:
        await functions.join_channel(ctx)
    else:
        await ctx.send("You don't have the required role for that")




