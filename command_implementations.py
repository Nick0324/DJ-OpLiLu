import functions
import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.all()

client = commands.Bot(intents=intents, command_prefix="!")

@client.event
async def on_ready():
    print("Bot is ready")
    check_idle.start()
    check_alone.start()

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

@tasks.loop(seconds=30)
async def check_idle():
    print("Timer check idle")
    for vc in client.voice_clients: # Check for every channel that the bot is connected to
        if not vc.is_playing(): # If not playing audio
            await vc.disconnect()

@tasks.loop(seconds=15)
async def check_alone():
    print("Timer check alone")
    for vc in client.voice_clients:  # Check for every channel that the bot is connected to
        if len(vc.channel.members) == 1 and client.user in vc.channel.members:  # If only the bot is connected
            await vc.disconnect()

