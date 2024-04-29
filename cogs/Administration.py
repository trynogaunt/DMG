import discord
from discord.ext import commands
from discord.components import *
from discord import app_commands

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Suprimme les messages non épinglés d'un channel")
    async def reset(self, interaction : discord.Interaction):
        def not_pinned(m):
            return not m.pinned
        purged = await interaction.channel.purge(limit=100, check=not_pinned)
        msg = await interaction.channel.send(f"{len(purged)} messages supprimés (Ce message s'auto-détruira 10 secondes après son envoi)", delete_after=10)
 

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Administration(bot),  guild=discord.Object(id=1173979647889920010))