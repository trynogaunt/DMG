from datetime import datetime
from typing import Any
import discord
from discord.ext import commands
from discord.components import *
from discord import app_commands
import toml
from app.classes.DMG import DMG
from app.classes.Player import Player

class registerButton(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle = discord.ButtonStyle.green, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        for embed in interaction.message.embeds:
            if embed.title == "DMG":
                embed_dict = embed.to_dict()
        for field in embed_dict["fields"]:
            if field["name"] == "Partcipants":
                if field["value"].find(interaction.user.global_name) != -1:
                    await interaction.response.send_message("Vous êtes déjà inscris", ephemeral=True)
                else:
                    field["value"] += interaction.user.global_name
                    embed = discord.Embed.from_dict(embed_dict)
                    await interaction.message.edit(embed=embed)
                    await interaction.response.defer(thinking=False, ephemeral=True)

class unregisterButton(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle = discord.ButtonStyle.danger, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
    
    async def callback(self, interaction: discord.Interaction) -> Any:
         for embed in interaction.message.embeds:
            if embed.title == "DMG":
                embed_dict = embed.to_dict()
            for field in embed_dict["fields"]:
                if field["name"] == "Partcipants":
                    if field["value"].find(interaction.user.global_name) != -1:
                        field["value"] = field["value"].replace(interaction.user.global_name, '')
                        embed = discord.Embed.from_dict(embed_dict)
                        await interaction.message.edit(embed=embed)
                        await interaction.response.defer(thinking=False, ephemeral=True)
                    else:
                        await interaction.response.send_message("Vous n'êtes pas inscris", ephemeral=True)


class RegisteringView(discord.ui.View):
    def __init__(self, *,  timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.add_item(registerButton(label="Je m'inscris"))
        self.add_item(unregisterButton(label="Je me désinscris"))

class RegisteringEmbed(discord.Embed):
    def __init__(self):
        super().__init__(title ="DMG", description="S'inscrire")
        self.add_field(name="Partcipants", value="")