import discord
from discord import ui
from discord.ext import commands
import toml
import os
import datetime


class Bot(commands.Bot):
    def __init__(self)-> None:
        super().__init__(command_prefix="/" , intents=discord.Intents.all())
        self.cogslist = []
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.cogslist.append(filename[:-3])
    
    
    async def on_ready(self)-> None:
        print(f"Logged as {self.user.name}")
        synced = await self.tree.sync(guild=discord.Object(id=1173979647889920010))
        print(f'Synced commands: {len(synced)}')
    
    async def setup_hook(self) -> None:
        for cog in self.cogslist:
            try:
                await self.load_extension(f"cogs.{cog}")
                print(f'{cog} extension is loaded')
            except Exception as e:
                print(f"{cog} extension can't be loaded -> {e}")
        return await super().setup_hook()

bot = Bot()

with open('default.toml','r', encoding="utf8") as f:
    config = toml.load(f)
                     


if __name__ == "__main__":

    bot.run(config['connect']['BotToken'])