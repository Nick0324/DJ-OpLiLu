import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import command_implementations
import functions
import discord
import wavelink

class TestIdleDisconnect(unittest.TestCase):
    def setUp(self):
        self.bot = command_implementations.client #asigns command_implementations.client to self.bot
        self.ctx = MagicMock() #simulate the context passed to command functions
        self.ctx.guild = MagicMock() #guild object contains information about the server where the command was invoked
        self.ctx.author = MagicMock() #author object  represents the user who invoked the command
        self.ctx.voice_client = AsyncMock() #voice client represents the bots conection to a voice channel in a server

    @patch('command_implementations.client.voice_clients', new_callable=AsyncMock)
    async def test_check_idle(self, mock_voice_clients):
        mock_voice_client = MagicMock()
        mock_voice_client.is_playing.return_value = False
        mock_voice_clients.return_value = [mock_voice_client]

        await command_implementations.check_idle()

        mock_voice_client.disconnect.assert_called_once()#check if idle

    @patch('command_implementations.client.voice_clients', new_callable=AsyncMock)
    async def test_check_not_idle(self, mock_voice_clients):
        mock_voice_client = MagicMock()
        mock_voice_client.is_playing.return_value = True
        mock_voice_clients.return_value = [mock_voice_client]

        await command_implementations.check_idle()

        mock_voice_client.disconnect.assert_not_called()#check if not idle

    @patch('command_implementations.client.voice_clients', new_callable=AsyncMock)
    async def test_check_alone(self, mock_voice_clients):
        mock_voice_client = MagicMock()
        mock_voice_client.channel.members = [command_implementations.client.user]
        mock_voice_clients.return_value = [mock_voice_client]

        await command_implementations.check_alone()

        mock_voice_client.disconnect.assert_called_once()#check if bot disconected

    @patch('command_implementations.client.voice_clients', new_callable=AsyncMock)
    async def test_check_not_alone(self, mock_voice_clients):
        mock_voice_client = MagicMock()
        mock_voice_client.channel.members = [command_implementations.client.user, self.ctx.author]#another user with the bot
        mock_voice_clients.return_value = [mock_voice_client]

        await command_implementations.check_alone()

        mock_voice_client.disconnect.assert_not_called()#check if bot didnt disconect

    # class TestBotDisconnect(unittest.IsolatedAsyncioTestCase):
    #
    #     async def asyncSetUp(self):
    #         self.ctx = MagicMock()
    #         self.voice_client = MagicMock()
    #         self.voice_client.is_playing.return_value = False
    #         self.voice_client.channel.members = [MagicMock(), MagicMock()]  # Two members, not alone
    #         self.voice_client.guild.voice_client = self.voice_client
    #         client.voice_clients = [self.voice_client]
    #
    #     async def test_check_idle_disconnect(self):
    #         with patch('mybot.bot.client.voice_clients', new_callable=MagicMock) as mock_voice_clients:
    #             mock_voice_clients.return_value = [self.voice_client]
    #             await check_idle()
    #             self.voice_client.disconnect.assert_called_once()
    #
    #     async def test_check_alone_disconnect(self):
    #         self.voice_client.channel.members = [MagicMock()]  # Only one member, the bot itself
    #         with patch('mybot.bot.client.voice_clients', new_callable=MagicMock) as mock_voice_clients:
    #             mock_voice_clients.return_value = [self.voice_client]
    #             await check_alone()
    #             self.voice_client.disconnect.assert_called_once()


    # async def test_join_channel(self):
    #     ctx = MagicMock()
    #     ctx.author.voice.channel = MagicMock()
    #     ctx.author.voice.channel.connect = AsyncMock()
    #
    #     await join_channel(ctx)
    #
    #     ctx.author.voice.channel.connect.assert_called_once()
    #
    # async def test_disconnect_channel(self):
    #     ctx = MagicMock()
    #     ctx.author.voice.channel = MagicMock()
    #     ctx.author.voice.channel.disconnect = AsyncMock()
    #
    #     await disconnect_channel(ctx)
    #
    #     ctx.author.voice.channel.disconnect.assert_called_once()
    #
    # async def test_pause(self):
    #     ctx = MagicMock()
    #     ctx.voice_client = MagicMock()
    #     ctx.message = MagicMock()
    #     ctx.message.add_reaction = AsyncMock()
    #
    #     await pause_resume(ctx)
    #
    #     ctx.message.add_reaction.assert_called_once_with("\u2705")
    #
    # async def test_resume(self):
    #     ctx = MagicMock()
    #     ctx.voice_client = MagicMock()
    #     ctx.message = MagicMock()
    #     ctx.message.add_reaction = AsyncMock()
    #
    #     await pause_resume(ctx)
    #
    #     ctx.message.add_reaction.assert_called_once_with("\u2705")


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
