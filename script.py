from dataclasses import dataclass
import random

@dataclass
class Point:
    x: int = 0
    y: int = 0

def __eq__(self, other) -> bool:
     return self.x == other.x and self.y == other.y

class MyException(Exception):
    def __str__(self):
        return f'(My exception class)'

class OutOfRange(MyException):
    def __str__(self):
        return f'(Out of range)'
    
class OccupiedPoint(MyException):
    def __str__(self):
        return f'(Point is occupied)'


class Player:
    def __init__(self, board) -> None:
        self.ships = []
        self.ship_points = []
        self.ship_count = 7
        self.board = board
    def add_ship(self, point):
        self.ships.append(point)
    def add_points(self):
        pass
    def get_points(self):
        pass
    

class AI(Player):
    def shoot():
        pass


class User(Player):
    def shoot():
        pass

class Ship:
    def __init__(self, size, align, hp) -> None:
        self.__size = size
        self.__align = align
        self.__hp = hp


class Board:
    def __init__(self, size = 6) -> None:
        self.__size = size
        self.__field = [['o' for i in range(self.__size)] for j in range(self.__size)]

    def create_ship(self):
        _i = True
        while _i:
            try:
                # comment: 
            except Exception as e:
                raise
            else:
                # comment: 
            finally:
                # comment: 
            # end try

    def create_ships(self, player):
        for i in player.ship_count:
            player.add_ship(self.create_ship(self))


    def add_ships_to_board(self):
        pass
        
                   



        






    @property
    def drow_board(self):
        print()
        _str = '__|'
        for i in range(self.__size):
            _str += f' {i+1} |'
        print(_str)
        _str = '  |'
        for i in range(self.__size):
            _str = f'{i+1} |'
            for j in range(self.__size):
                _str += f' {self.__field[i][j]} |'
            print(_str)
        print()

b1 = Board(6)
p1 = Player(b1)

p1.board.drow_board
p1.board.add_ships(p1)





class Game:
    pass
