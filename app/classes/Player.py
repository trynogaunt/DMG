class Player():
    def __init__(self , name : str, message_id : int = 0) -> None:
        self.__name : str = name
        self.__message_id : int = message_id
    
    def get_name(self) -> str:
        '''Return the name of player'''

        return self.__name
    
    def get_message_id(self) -> int:
        '''Return ID of inscription message'''

        return self.__message_id