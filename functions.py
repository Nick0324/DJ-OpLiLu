import asyncio
import wavelink
import discord

async def join_channel(ctx):
    await ctx.author.voice.channel.connect()


async def disconnect_channel(ctx):
    await ctx.author.voice.channel.disconnect()


async def node_connect():
    from command_implementations import client
    await client.wait_until_ready()
    node: wavelink.Node = wavelink.Node(uri='https://lavalink4.alfari.id/', password='catfein')
    await wavelink.Pool.connect(nodes=[node], client=client, cache_capacity=None)
