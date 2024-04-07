import functions
import discord
from discord.ext import commands

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

intents = discord.Intents.all()

client = commands.Bot(intents=intents, command_prefix="!")
@client.command(name="join", pass_ctx=True)
async def join(ctx):

    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    role = discord.utils.get(ctx.author.roles, name="dj")

    if role:
        if voice == None:
            await functions.join_channel(ctx)
        else:
            await ctx.send(f"I'm already connected to **{ctx.author.voice.channel}** !")
    else:
        await ctx.send("You don't have the required role for that")


@client.command(name="disconnect", pass_ctx=True)
async def disconnect(ctx):
    role = discord.utils.get(ctx.author.roles, name="dj")
    if role:
        vc = ctx.message.guild.voice_client
        await vc.disconnect()
    else:
        await ctx.send("I'm not connected to any channels")