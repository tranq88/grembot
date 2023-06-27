import discord
from discord.ext import commands
import asyncio

from env import (
    BOT_TEST_SERVER,
    GREMLIN_ID,
    BTS_TEMP_CHANNEL,
    GREMLIN_TEMP_CHANNEL
)


class TempChannel(commands.Cog):
    """Delete messages in #temp-channel after 30 minutes."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in [BTS_TEMP_CHANNEL, GREMLIN_TEMP_CHANNEL]:
            await asyncio.sleep(1800)
            await message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(TempChannel(bot),
                      guilds=[discord.Object(id=BOT_TEST_SERVER),
                              discord.Object(id=GREMLIN_ID)])
