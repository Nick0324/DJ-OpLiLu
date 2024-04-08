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


@client.command(name="disconnect", pass_ctx=True)
async def disconnect(ctx):
    role = discord.utils.get(ctx.author.roles, name="dj")
    if role:
        vc = ctx.message.guild.voice_client
        await vc.disconnect()
    else:
        await ctx.send("I'm not connected to any channels")


@client.command()
async def play(ctx, *args):
    query = " ".join(args)
    try:
        voice_channel = ctx.author.voice.channel
    except:
        await ctx.send("```You need to connect to a voice channel first!```")
        return
    if functions.is_paused:
        functions.vc.resume()
    else:
        song = functions.search_yt(query)
        if type(song) == type(True):
            await ctx.send(
                "```Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.```")
        else:
            if functions.is_playing:
                await ctx.send(f"**#{len(functions.music_queue) + 2} -'{song['title']}'** added to the queue")
            else:
                await ctx.send(f"**'{song['title']}'** added to the queue")
            functions.music_queue.append([song, voice_channel])
            if not functions.is_playing:
                await functions.play_music(ctx, client)
