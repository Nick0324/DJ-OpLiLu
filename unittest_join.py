import unittest
from unittest.mock import MagicMock, AsyncMock
from functions import join_channel, disconnect_channel

class TestBotFunctions(unittest.IsolatedAsyncioTestCase):

    async def test_join_channel(self):
        ctx = MagicMock()
        ctx.author.voice.channel = MagicMock()
        ctx.author.voice.channel.connect = AsyncMock()

        await join_channel(ctx)

        ctx.author.voice.channel.connect.assert_called_once()

    async def test_disconnect_channel(self):
        ctx = MagicMock()
        ctx.author.voice.channel = MagicMock()
        ctx.author.voice.channel.disconnect = AsyncMock()

        await disconnect_channel(ctx)

        ctx.author.voice.channel.disconnect.assert_called_once()

if __name__ == "__main__":
    unittest.main()
