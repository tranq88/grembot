import discord
from discord.ext import commands, tasks
from discord import app_commands

from env import (
    BOT_TEST_SERVER,
    GREMLIN_ID,
    BTS_TEMP_CHANNEL,
    GREMLIN_TEMP_CHANNEL
)

from datetime import datetime, timedelta, timezone
from collections import deque


ME = 187679550841290752

class TempChannel(commands.Cog):
    """Delete messages in #temp-channel after 30 minutes."""
    message_queue: deque[discord.Message] = deque()

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.delete_messages.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in [BTS_TEMP_CHANNEL, GREMLIN_TEMP_CHANNEL]:
            self.message_queue.append(message)

    @tasks.loop(seconds=30)
    async def delete_messages(self):
        if not self.message_queue:
            return

        to_remove: list[discord.Message] = []
        now = datetime.now(timezone.utc)

        for m in self.message_queue:
            if (now - m.created_at) > timedelta(minutes=30):
                to_remove.append(m)

        if not to_remove:
            return

        # this should be fine because the messages in to_remove
        # should be at the front of the queue
        for _ in range(len(to_remove)):
            self.message_queue.popleft()

        # note when in prod: this will probably bug out
        # if both temp channels get messages
        channel = self.bot.get_channel(GREMLIN_TEMP_CHANNEL)

        try:
            await channel.delete_messages(to_remove)
        except discord.NotFound:  # the message was likely deleted already
            # we need to catch this error because for some reason
            # it stops the task loop
            pass

    @app_commands.command(
        name='purge',
        description='Purge messages. Only usable in #temp-channel.'
    )
    @app_commands.guilds(BOT_TEST_SERVER, GREMLIN_ID)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)

        if not (
            interaction.user.guild_permissions.administrator or
            interaction.user.id == ME
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

    @app_commands.command(
        name='queuesize',
        description=('View the number of messages in #temp-channel '
                     'awaiting deletion.')
    )
    @app_commands.guilds(BOT_TEST_SERVER, GREMLIN_ID)
    async def queuesize(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not (
            interaction.user.guild_permissions.administrator or
            interaction.user.id == ME
        ):
            await interaction.followup.send(
                'This command is admin-only.'
            )
            return

        await interaction.followup.send(len(self.message_queue))


async def setup(bot: commands.Bot):
    await bot.add_cog(TempChannel(bot),
                      guilds=[discord.Object(id=BOT_TEST_SERVER),
                              discord.Object(id=GREMLIN_ID)])
