import wavelink
import functions
import discord
from discord.ext import commands
from typing import cast

intents = discord.Intents.all()

client = commands.Bot(intents=intents, command_prefix="!")


@client.event
async def on_ready():
    print("Bot is ready.")
    client.loop.create_task(functions.node_connect())


@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node is ready.")


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
async def play(ctx, *, query: str):
    player = cast(wavelink.Player, ctx.voice_client)

    if not player:
        try:
            player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
        except AttributeError:
            await ctx.send("Please join a voice channel first before using this command.")
            return
        except discord.ClientException:
            await ctx.send("I was unable to join this voice channel. Please try again.")
            return

    player.autoplay = wavelink.AutoPlayMode.partial

    if not hasattr(player, "home"):
        player.home = ctx.channel
    elif player.home != ctx.channel:
        await ctx.send(f"You can only play songs in {player.home.mention}, as the player has already started there.")
        return

    tracks: wavelink.Search = await wavelink.Playable.search(query)
    if not tracks:
        await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
        return

    track: wavelink.Playable = tracks[0]
    await player.queue.put_wait(track)
    await ctx.send(f"Added **`{track}`** to the queue.")

    if not player.playing:
        await player.play(player.queue.get())

@client.command(name="resume")
async def pause_resume(ctx: commands.Context) -> None:
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    if not player.paused:
        await ctx.message.add_reaction("\u274C")  # add X react to command
        return
    await player.pause(False)
    await ctx.message.add_reaction("\u2705") #add ok react to command

@client.command(name="pause")
async def pause_resume(ctx: commands.Context) -> None:
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    if player.paused:
        await ctx.message.add_reaction("\u274C")  # add X react to command
        return
    await player.pause(True)
    await ctx.message.add_reaction("\u2705") #add ok react to command





