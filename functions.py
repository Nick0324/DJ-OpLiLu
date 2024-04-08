import asyncio

import discord
import yt_dlp
from youtubesearchpython import VideosSearch

is_playing = False
is_paused = False

music_queue = []
YDL_OPTIONS = {'format': 'bestaudio/best'}
FFMPEG_OPTIONS = {'options': '-vn'}

ytdl = yt_dlp.YoutubeDL(YDL_OPTIONS)

vc = None


async def join_channel(ctx):
    await ctx.author.voice.channel.connect()


async def disconnect_channel(ctx):
    await ctx.author.voice.channel.disconnect()


def search_yt(item):
    if item.startswith("https://"):
        title = ytdl.extract_info(item, download=False)["title"]
        return {'source': item, 'title': title}

    search = VideosSearch(item, limit=1)
    return {'source': search.result()["result"][0]["link"], 'title': search.result()["result"][0]["title"]}


async def play_next(client):
    global is_playing
    global vc
    if len(music_queue) > 0:
        is_playing = True

        # get the first url
        m_url = music_queue[0][0]['source']

        # remove the first element as you are currently playing it
        music_queue.pop(0)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(m_url, download=False))
        song = data['url']
        vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",options="-vn"),
                     after=lambda e: asyncio.run_coroutine_threadsafe(play_next(client), client.loop))
    else:
        is_playing = False


async def play_music(ctx, client):
    if len(music_queue) > 0:
        global is_playing
        is_playing = True

        m_url = music_queue[0][0]['source']
        # try to connect to voice channel if you are not already connected
        global vc
        if vc is None or not vc.is_connected():
            vc = await music_queue[0][1].connect()

            # in case we fail to connect
            if vc is None:
                await ctx.send("```Could not connect to the voice channel```")
                return
        else:
            await vc.move_to(music_queue[0][1])
        # remove the first element as you are currently playing it
        music_queue.pop(0)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(m_url, download=False))
        song = data['url']
        vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **FFMPEG_OPTIONS),
                     after=lambda e: asyncio.run_coroutine_threadsafe(play_next(client), client.loop))

    else:
        is_playing = False
