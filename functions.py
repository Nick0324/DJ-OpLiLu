async def join_channel(ctx):
    await ctx.author.voice.channel.connect()
async def disconnect_channel(ctx):
    await ctx.author.voice.channel.disconnect()