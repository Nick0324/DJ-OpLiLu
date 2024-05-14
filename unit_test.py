import unittest
from unittest.mock import AsyncMock, MagicMock
from command_implementations import skip, pause_resume

class TestMusicCommands(unittest.TestCase):
    def setUp(self):
        self.ctx = MagicMock()
        self.player = MagicMock()
    async def test_skip(self):
        self.ctx.voice_client = self.player
        self.player.playing = True
        await skip(self.ctx)
        self.player.skip.assert_called_once_with(force=True)
        self.ctx.message.add_reaction.assert_called_once_with("\u2705")
    async def test_resume(self):
        self.ctx.voice_client = self.player
        self.player.paused = True
        await pause_resume(self.ctx)
        self.player.pause.assert_called_once_with(False)
        self.ctx.message.add_reaction.assert_called_once_with("\u2705")
if __name__ == '__main__':
    unittest.main()
