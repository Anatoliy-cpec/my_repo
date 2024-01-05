from dataclasses import dataclass
import random
from typing import List, Any


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __eq__(self, other: Any) -> bool:
        return self.x == other.x and self.y == other.y


class MyException(Exception):
    def __str__(self) -> str:
        return f"(My exception class)"


class OutOfRange(MyException):
    def __str__(self) -> str:
        return f"(Точка выходит за границы доски!)"
    
class NotValid(MyException):
    def __str__(self) -> str:
        return f"(Вокруг этой точки уже есть корабль!)"
    
class NotAllign(MyException):
    def __str__(self) -> str:
        return f"(Введите h/v!)"
    
class NotInt(MyException):
    def __str__(self) -> str:
        return f"(Целое число от 1 до 6)"


class OccupiedPoint(MyException):
    def __str__(self) -> str:
        return f"(Point is occupied)"


class Player:
    def __init__(self, ship_count: List[int] = [3, 2, 2, 1, 1, 1]) -> None:
        self.ships: List[Ship] = []
        self.ship_points: List[Point] = []
        self.ship_count: List[int] = ship_count
        
    def add_ship(self, ship: "Ship"):
        self.ships.append(ship)


    def extract_ship_points(self) -> None:
        
        self.ship_points: List[Point] = []

        for ship in self.ships:
            for point in ship.points:
                self.ship_points.append(point)



class AI(Player):
    def __init__(self, ship_count: List[int] = [3, 2, 2, 1, 1, 1]) -> None:
        super().__init__(ship_count)
    def shoot(self) -> Any:
        pass


class User(Player):
    def __init__(self, ship_count: List[int] = [3, 2, 2, 1, 1, 1]) -> None:
        super().__init__(ship_count)
    def shoot(self) -> Any:
        pass


class Ship:
    def __init__(self, size: int, points: "Point", hp: int) -> None:
        self.__size: int = size
        self.points: "Point" = points
        self.hited_points: List[Point]
        self.__hp: int = hp


class Board:
    def __init__(self, size: int = 6, player: "Player" = Player) -> None:
        self.__player: "Player" = player
        self.__size: int = size
        self.__field: List[List[str]] = [
            ["o" for i in range(self.__size)] for j in range(self.__size)
        ]
    
    def point_is_valid(self, point: Point) -> bool:
        
        _points = [Point(point.x-1, point.y-1),Point(point.x-1, point.y),Point(point.x-1, point.y+1),
                    Point(point.x, point.y-1),Point(point.x, point.y),Point(point.x, point.y+1),
                    Point(point.x+1, point.y-1),Point(point.x+1, point.y),Point(point.x+1, point.y+1),]

        for i in self.__player.ship_points:
            if i in _points:
                return False
            
        return True

    def create_ship(self, ship_size: int) -> Ship:
        _exit: bool = False
        while not _exit:
            try:
                
                if type(self.__player) is type(AI()):
                    
                    _allign: str = random.choice(['h','v'])

                    _x: int = random.randint(1,6)
                    _y: int = random.randint(1,6)

                    _p : "Point" = Point(_x-1,_y-1)
                    _points: List[Point] = []

                    if _allign == 'h':
                        for i in range(ship_size):
                            if self.point_is_valid(Point(_p.x, _p.y + i)):
                                _points.append(Point(_p.x, _p.y + i))
                            else:
                                raise 
                            
                    elif _allign == 'v':
                        for i in range(ship_size):
                            if self.point_is_valid(Point(_p.x+i, _p.y)):
                                _points.append(Point(_p.x+i, _p.y))
                            else:
                                raise 

                else:
                    
                    _allign: str = input("Ориентация корабля: h/v") 
                    if 'h' in _allign:
                        _allign = 'h'
                    elif 'v' in _allign:
                        _allign = 'v'
                    else:
                        raise NotAllign

                    _x: int = int(input("X: "))
                    _y: int = int(input("Y: "))

                    _p : "Point" = Point(_x-1,_y-1)
                    _points: List[Point] = []

                    if (_x < 1 or _x > 6) or (_y < 1 or _y > 6):
                            raise OutOfRange

                    if _allign == 'h':
                        for i in range(ship_size):
                            if self.point_is_valid(Point(_p.x, _p.y + i)):
                                _points.append(Point(_p.x, _p.y + i))
                            else:
                                raise NotValid
                            
                    elif _allign == 'v':
                        for i in range(ship_size):
                            if self.point_is_valid(Point(_p.x+i, _p.y)):
                                _points.append(Point(_p.x+i, _p.y))
                            else:
                                raise NotValid

            except Exception as e:
                print(e)

            else:
                _exit = True
                return Ship(ship_size, _points, ship_size)
            finally:
                ...
            

    def create_ships(self) -> None:
        for ship_size in self.__player.ship_count:
            self.__player.add_ship(self.create_ship(ship_size))
            self.__player.extract_ship_points()
            self.drow_board

    def add_ships_to_board(self) -> None:
        pass

    @property
    def drow_board(self) -> None:

        print(self.__player.ship_points)

        self.__field: List[List[str]] = [
            ["o" for i in range(self.__size)] for j in range(self.__size)
        ]

        for point in self.__player.ship_points:
            self.__field[point.x][point.y] = '■'


        print()
        _str: str = "__|"
        for i in range(self.__size):
            _str += f" {i+1} |"
        print(_str)
        _str = "  |"
        for i in range(self.__size):
            _str = f"{i+1} |"
            for j in range(self.__size):
                _str += f" {self.__field[i][j]} |"
            print(_str)
        print()



p1: AI = AI([3,1])

b1: Board = Board(6, p1)
b1.create_ships()





class Game:
    pass
