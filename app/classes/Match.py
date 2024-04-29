from app.classes.Player import Player

class Match():
    def __init__(self , number, player1, player2):
        self.__number : int = number
        self.__player1 : Player = player1
        self.__player2 : Player = player2
        self.__winner : Player = None
        self.__next_match : int = None


    def get_number(self):
        return self.__number
    
    def get_player1(self) -> Player:
        return self.__player1
    
    def get_player2(self) -> Player:
        return self.__player2

    def exist_winner(self) -> bool:
        if self.__winner == None:
            return 0
        else:
            return 1
    
    def set_winner(self , player : Player) -> None:
        self.__winner = player
    
    def get_winner(self) -> Player:
        return self.__winner
        
    def get_match_info(self):
        return self.__number , self.__player1 , self.__player2 , self.__winner , self.__next_match   

    def get_next_match(self) -> int:
        return self.__next_match 

    def set_next_match(self, number) -> int:
        self.__next_match = number
    
    