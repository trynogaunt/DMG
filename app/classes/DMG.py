from app.classes.Match import Match
from app.classes.Player import Player
import random

class DMG():
    def __init__(self , message_id , guild_id , channel_id) -> None:
        self.__match_list : list[Match]= []
        self.__player_list : list[Player] = []
        self.__winner_list : list[Player] = []
        self.__played_match : list[int] = []
        self.__first_match : int = None
        self.__current_match : int = None
        self.__message_id : int = message_id
        self.__message_link : str  = f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"
        self.msg = f"Nouveau DMG démarré (Id de message: {self.__message_id })"
    

    def get_played_match(self) -> list[int]:
        '''Return list of played matchs in current branch'''

        return self.__played_match
    
    def set_played_match(self, match_number : 0):
        '''Add match in played'''
        if match_number != 0:
            self.__played_match.append(match_number)
        else:
            self.__played_match = []

    def get_current_match(self) -> int:
        '''Return number of current match played'''

        return self.__current_match
    
    def get_first_match(self) -> int:
        '''Return number of first match'''

        return self.__first_match
    
    def set_current_match(self, current_match) -> int:
        '''Return number of current match played'''

        self.__current_match = current_match
    
    def set_first_match(self, first_match) -> int:
        '''Set first match'''

        self.__first_match = first_match

    def get_register_message_id(self) -> int:
        '''Return id of registering message'''

        return self.__message_id
    
    def get_register_message_link(self):
        '''Return link of registering message'''

        return self.__message_link
    
    def get_player_list(self) -> list[object]:
        '''Return a list of DMG players'''

        return self.__player_list

    def fetch_player(self, name):
        '''Return Player with name'''

        for player in self.__player_list:
            if player.get_name() == name:
                return player

    def add_player(self, name : str , msg_id : int) -> bool:
        '''Add player in player list'''
        try: 
            player = Player(name , msg_id)
            self.get_player_list().append(player)
            print(f"{player.get_name()} a été ajouté")
            return 1
        except:
            return 0

    
    def remove_player(self, name : str) -> bool :
        '''Remove player from player list, return true if player exist and got removed'''
        response = 0
        for player in self.__player_list:
            if player.get_name() == name:
                self.__player_list.remove(player)
                print(f"{player.get_name()} a été retiré")
                response = 1
        return response

    
    def check_player_number(self) -> bool :
        '''Check if number player is under 8 places'''

        if len(self.get_player_list) < 8:
            return 1
        else:
            return 0
    
    def get_match_list(self) -> list[Match]:
        '''Return a list of DMG matchs'''
        
        return self.__match_list

    def set_match_list(self, list : list[Match]) -> None:
        '''Set value to match list'''

        self.__match_list = list
    
    def add_match(self , match : Match) -> str:
        self.get_match_list().append(match)
        number , player1 , player2  , winner, next_match = match.get_match_info()
        return f"Match n°{number} ajouté , participants: {player1.get_name()} et {player2.get_name()}"

    def create_match(self, number : int, player1 : Player, player2 : Player) -> Match:
        '''Return a match between 2 players and write inside txt files'''

        f = open(f"Matchs/Match_{number}/J1.txt" , "w")
        f.write(player1.get_name())
        f.close()
        f = open(f"Matchs/Match_{number}/J2.txt" , "w")
        f.write(player2.get_name())
        f.close()
        print(f"Match n°{number}: {player1.get_name()} contre {player2.get_name()}")
        return Match(number, player1 , player2)
    
    def show_match(self, number):
        '''Write inside selected txt files for OBS HUD'''

        for match in self.get_match_list():
            if match.get_number() == number:
                f = open(f"Matchs/Selected/J1.txt" , "w")
                f.write(match.get_player1().get_name())
                f.close()
                f = open(f"Matchs/Selected/J2.txt" , "w")
                f.write(match.get_player2().get_name())
                f.close()

    def random_player_list(self) -> list[Player]:
        '''Randomize player list'''

        for i in range(3):
            random.shuffle(self.__player_list)
        return self.__player_list
    
    def get_winner_list(self) -> list[Player]:
        '''return winner list'''
        return self.__winner_list
    
    def add_winner(self, player : Player) -> None:
        '''Add a player in winner list'''

        self.__winner_list.append(player)
    
    def get_winner_list(self) -> list[Player]:
        '''Return winner list'''

        return self.__winner_list

    def write_last_winner(self , player : str) -> None:
        '''Write winner of tourney'''
        f = open(f"Matchs/Winner.txt" , "w")
        f.write(player)
        f.close()
    
    def reset_matchs_display(self) -> None:
        for i in range(1,8):
            for n in range(1,3):
                f = open(f"Matchs/Match_{i}/J{n}.txt" , "w")
                f.write("")
                f.close()
        for i in range(1,3):
            f = open(f"Matchs/Selected/J{i}.txt" , "w")
            f.write("")
            f.close()
        f = open(f"Matchs/Winner.txt" , "w")
        f.write("")
        f.close()  