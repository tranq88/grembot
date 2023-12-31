import discord
from discord.ext import commands
import asyncio

import os
from env import BOT_TOKEN, BOT_TEST_SERVER, GREMLIN_ID


class Bot(commands.Bot):
    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!',
                         intents=intents,
                         help_command=None)

        asyncio.run(self.load_cogs())

        self.synced = False

    async def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')

    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            # await self.tree.sync()
            await self.tree.sync(
                guild=discord.Object(id=BOT_TEST_SERVER))
            await self.tree.sync(
                guild=discord.Object(id=GREMLIN_ID))
            self.synced = True

        print(f'Logged in as {self.user}')


if __name__ == '__main__':
    bot = Bot()
    bot.run(BOT_TOKEN)
