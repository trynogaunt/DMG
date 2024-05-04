import discord
from discord.ext import commands
from discord.components import *
from discord import app_commands
import toml
from app.classes.DMG import DMG
from app.classes.Player import Player
from app.views.RegisterView import RegisteringView , RegisteringEmbed


class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dmg = None
    
    @app_commands.command(name="register", description="Créer un tournoi et envoie un message d'inscription")
    async def register(self, interaction : discord.Interaction):
        with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            if interaction.channel.id == config['permissions']['commands_channel']:
                if self.dmg == None:
                    channel = self.bot.get_channel(config['permissions']['register_channel'])
                    embed = RegisteringEmbed()
                    msg = await channel.send(view=RegisteringView(), embed=embed)
                    self.dmg = DMG(msg.id , msg.guild.id , msg.channel.id)
                    await interaction.response.send_message("DMG crée", ephemeral=True)
                    print("DMG créé")
                    self.dmg.reset_matchs_display()
                else:
                    await interaction.response.send_message(f"Un DMG est déjà en cours, message de référence : {self.dmg.get_register_message_link()}" , ephemeral=True)               
    
    @app_commands.command(description="Ajoute un joueur à la liste des participants")
    async def add_player(self, interaction : discord.Interaction , player_name : str):
      with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            if interaction.channel.id == config['permissions']['commands_channel']:
                if self.dmg == None: 
                    msg = "Merci de créer un DMG avec la commande /register"
                else:
                    player_register = await self.bot.get_channel(config['permissions']['register_channel']).send(f"{player_name} veut la glace")
                    self.dmg.add_player(player_name, player_register.id)
                    msg = f"{player_name} à été ajouté"
                    
                await interaction.response.send_message(msg, ephemeral= True)
    
    @app_commands.command(description="Retire un joueur de la liste des participants")
    async def remove_player(self, interaction : discord.Interaction , player_name : str):
      with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            if interaction.channel.id == config['permissions']['commands_channel']:
                if self.dmg == None: 
                    msg = "Merci de créer un DMG avec la commande /register"
                else:
                    reg_msg_id = self.dmg.fetch_player(player_name).get_message_id()
                    if self.dmg.remove_player(player_name):
                        msg = f"{player_name} à été retiré"
                        reg_msg = await interaction.channel.fetch_message(reg_msg_id)
                        await reg_msg.delete()
                    else:
                        msg = f"Le joueur n'existe pas"    
                await interaction.response.send_message(msg, ephemeral= True)

    @app_commands.command(description="Créer une bracket de tournoi")
    async def start_dmg(self, interaction : discord.Interaction):
         join_list = []
         with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            if interaction.channel.id == config['permissions']['commands_channel']:
                if self.dmg == None: 
                    msg = "Merci de créer un DMG avec la commande /register"
                else:
                    if len(self.dmg.get_player_list()) <= 8 and len(self.dmg.get_player_list()) % 2 == 0 and len(self.dmg.get_player_list()) != 6:
                        seeded_list = self.dmg.random_player_list()
                        match len(seeded_list):
                            case 8:
                                self.dmg.set_first_match(1) 
                            case 4:
                                self.dmg.set_first_match(5)
                            case 2:
                                self.dmg.set_first_match(7)
                        match_number = self.dmg.get_first_match()
                        for i in range(0,len(seeded_list),2):
                            match = self.dmg.create_match(match_number ,seeded_list[i] ,seeded_list[i+1])
                            join_list.append(self.dmg.add_match(match))
                            match_number += 1
                        msg = f"Les matchs ajoutés: \n{''.join(join_list)}"
                    else:
                        msg = config['messages']['wrong_player_number']
                await interaction.response.send_message(msg, ephemeral= True)
        
    @app_commands.command(description="Cible le match renseigné")
    async def duel(self, interaction : discord.Interaction, number : int):
          msg = "Match inexistant"
          with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            if interaction.channel.id == config['permissions']['commands_channel']:
                for match in self.dmg.get_match_list():
                    if match.get_number() == number and match.get_winner() == None:
                
                        self.dmg.set_current_match(number)
                        f = open("Matchs/Selected/J1.txt" , "w")
                        f.write(f"{match.get_player1().get_name()}")
                        f.close()
                        f = open("Matchs/Selected/J2.txt" , "w")
                        f.write(f"{match.get_player2().get_name()}")
                        f.close()
                        msg = f"Match n°{number} affiché"
                        break
                    elif match.get_number() == number and match.get_winner() != None:
                        msg = "Match déjà joué" 
                print(msg)
                await interaction.response.send_message(msg , ephemeral=True)
    
    @app_commands.command(description="Définit le gagnant du match ciblé")
    async def set_winner(self, interaction : discord.Interaction , winner_name : str):
         with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            all_match_played = 1
            if interaction.channel.id == config['permissions']['commands_channel']:
                for match in self.dmg.get_match_list():
                    if match.get_number() == self.dmg.get_current_match():
                        if winner_name != match.get_player1().get_name() and winner_name != match.get_player2().get_name():
                            msg = f"{winner_name} n'a pas joué"
                        elif winner_name == match.get_player1().get_name():
                            winner = match.get_player1()  
                            match.set_winner(match.get_player1())
                            msg = f"{match.get_player1().get_name()} a remporté le match n°{match.get_number()}"
                        else:
                            winner = match.get_player2()          
                            match.set_winner(match.get_player2())
                            msg = f"{match.get_player2().get_name()} a remporté le match n°{match.get_number()}" 

                        self.dmg.set_played_match(match.get_number())

                for match in self.dmg.get_match_list():
                    if match.exist_winner() == False:
                        all_match_played = 0
                
                if all_match_played == 1:
                    msg = f"{msg} (Vous pouvez passer aux matchs suivants avec /next_dmg)"
                
                if len(self.dmg.get_match_list()) == len(self.dmg.get_player_list())-1:
                    msg = f"Vainqueur du tournoi: {winner.get_name()}"
                    self.dmg.write_last_winner(winner.get_name())
                print(msg)      
                await interaction.response.send_message(msg , ephemeral= True)
    
    @app_commands.command(description="Passe au groupe de match suivant")
    async def next_dmg(self, interaction : discord.Interaction):
        with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            join_list = []
            if interaction.channel.id == config['permissions']['commands_channel']:
                winner_list = []
                next_match = max(self.dmg.get_played_match())+1
                for match_number in self.dmg.get_played_match():
                    for match in self.dmg.get_match_list():
                         if match.get_number() == match_number:
                            winner_list.append(match.get_winner())
                for i in range(0, len(winner_list)-1 , 2):
                    match = self.dmg.create_match(next_match ,winner_list[i] ,winner_list[i+1])
                    join_list.append(self.dmg.add_match(match))
                    next_match += 1
                self.dmg.set_played_match(0) 
                msg = f"Les matchs ajoutés: \n{''.join(join_list)}"
                await interaction.response.send_message(msg, ephemeral=True)
    
    @app_commands.command(name ="banhero", description="Créer un sondage de ban pour les héros(Séparer chaque nom avec une virgule)")
    async def banhero(self, interaction : discord.Interaction, heros : str):
        with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            if interaction.channel.id == config['permissions']['commands_channel']:
                channel = self.bot.get_channel(config['permissions']['debate_channel'])
                heros = heros.split(",")
                for hero in heros:
                        msg = await channel.send(f"Proposition de ban: {hero}")
                        await msg.add_reaction('✅')
                        await msg.add_reaction('❎')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            if user != reaction.message.author and reaction.emoji == "⚔️" and reaction.message.id == self.dmg.get_register_message_id():
                if len(self.dmg.get_player_list()) < 8:
                    player_register = await self.bot.get_channel(config['permissions']['register_channel']).send(f"{user.name} veut la glace")
                    self.dmg.add_player(user.name , player_register.id)
                    await user.send("Inscription au DMG enregistrée")
                else:
                    print(f"Trop de joueurs , {user.name} n'a pas été inscrit")
                    await user.send(config['messages']['tournament_full'])

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        with open('config.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            if user != reaction.message.author and reaction.emoji == "⚔️" and reaction.message.id == self.dmg.get_register_message_id():
                reg_msg_id = self.dmg.fetch_player(user.name).get_message_id()
                self.dmg.remove_player(user.name)
                reg_msg = await reaction.message.channel.fetch_message(reg_msg_id)
                await reg_msg.delete()
                await user.send("Désinscription au DMG enregistrée")

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Tournament(bot),  guild=discord.Object(id=1236250312185090118))