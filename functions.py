async def join_channel(ctx):
    await ctx.author.voice.channel.connect()
