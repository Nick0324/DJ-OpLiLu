async def join_channel(ctx):
    await ctx.author.voice.channel.connect()
    await ctx.send(f"Joined **{ctx.author.voice.channel}**")
async def disconnect_channel(ctx):
    await ctx.author.voice.channel.disconnect()