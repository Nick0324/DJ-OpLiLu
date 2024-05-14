import unittest
from functions import join_channel, disconnect_channel
from command_implementations import pause_resume
from unittest.mock import MagicMock, AsyncMock, patch
from command_implementations import play, pause_resume

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

    async def test_pause(self):
        ctx = MagicMock()
        ctx.voice_client = MagicMock()
        ctx.message = MagicMock()
        ctx.message.add_reaction = AsyncMock()

        await pause_resume(ctx)

        ctx.message.add_reaction.assert_called_once_with("\u2705")

    async def test_resume(self):
        ctx = MagicMock()
        ctx.voice_client = MagicMock()
        ctx.message = MagicMock()
        ctx.message.add_reaction = AsyncMock()

        await pause_resume(ctx)

        ctx.message.add_reaction.assert_called_once_with("\u2705")


    # @patch('command_implementations.wavelink.Playable.search')
    # async def test_play(self, mock_search):
    #     ctx = MagicMock()
    #     ctx.author.voice.channel = MagicMock()
    #     ctx.author.voice.channel.connect = AsyncMock()
    #     ctx.voice_client = None
    #     mock_search.return_value = [MagicMock()]
    #
    #     await play(ctx, query="https://www.youtube.com/watch?v=npyiiInMA0w")
    #
    #     ctx.send.assert_called_once_with(f"Added **`{mock_search.return_value[0]}`** to the queue.")
    #
    # async def test_pause_resume(self):
    #     ctx = MagicMock()
    #     ctx.voice_client = MagicMock()
    #     ctx.message.add_reaction = AsyncMock()
    #
    #     # Test pause
    #     ctx.voice_client.paused = False
    #     await pause_resume(ctx)
    #     ctx.voice_client.pause.assert_called_once_with(True)
    #     ctx.message.add_reaction.assert_called_once_with("\u2705")
    #
    #     # Test resume
    #     ctx.voice_client.paused = True
    #     await pause_resume(ctx)
    #     ctx.voice_client.pause.assert_called_with(False)
    #     ctx.message.add_reaction.assert_called_with("\u2705")

if __name__ == "__main__":
    unittest.main()
