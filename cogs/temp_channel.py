import discord
from discord.ext import commands
from discord import app_commands
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

    @app_commands.command(
        name='purge',
        description='Purge messages. Only usable in #temp-channel.'
    )
    @app_commands.guilds(BOT_TEST_SERVER, GREMLIN_ID)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)

        if not (
            interaction.user.guild_permissions.administrator or
            interaction.user.id == 187679550841290752
        ):
            await interaction.followup.send(
                'This command is admin-only.'
            )
            return

        if interaction.channel_id != GREMLIN_TEMP_CHANNEL:
            await interaction.followup.send(
                f'This command can only be used in <#{GREMLIN_TEMP_CHANNEL}>'
            )
            return

        await interaction.channel.purge(limit=amount)
        await interaction.followup.send(
            f'Deleted the last {amount} messages.'
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(TempChannel(bot),
                      guilds=[discord.Object(id=BOT_TEST_SERVER),
                              discord.Object(id=GREMLIN_ID)])
