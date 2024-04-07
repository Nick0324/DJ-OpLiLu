import discord
from discord.ext import commands

client = commands.Bot(intents=discord.Intents.default(), command_prefix="!")


def test_main():
    print("Hello")


file = open('token.txt', 'r')
client.run(file.readline())
file.close()
