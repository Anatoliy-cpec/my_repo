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
        return f"(Точка занята)"


class Player:
    def __init__(self, ship_count: List[int] = [3, 2, 1]) -> None:
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
    def __init__(self, ship_count: List[int] = [3, 2, 1]) -> None:
        super().__init__(ship_count)
    
    def shoot(self, enemy: "Board") -> Any:
        # print('Ваша очередь ходить')
        # _x: int = int(input("X: "))
        # _y: int = int(input("Y: "))
        # _p : "Point" = Point(_x-1,_y-1)
        ...


class User(Player):
    def __init__(self, ship_count: List[int] = [3, 2, 1]) -> None:
        super().__init__(ship_count)
    def shoot(self, enemy: "Board") -> Any:
        try:
            _exit: bool = False
            while not _exit:
                print('Ваша очередь ходить')
                _x: int = int(input("X↓: "))
                _y: int = int(input("Y→: "))

                if (_x < 1 or _x > 6) or (_y < 1 or _y > 6):
                                raise OutOfRange

                _p : "Point" = Point(_x-1,_y-1)

                if _p in enemy.shooted_points:
                    raise OccupiedPoint
                else:
                    enemy.add_hitted_point(_p)

                    for ship in enemy.__player.ships:
                        for point in ship.points:
                            if point == _p:
                                ship.decrease_health
                                ship.hited_points.append(_p)





        except Exception as e:
            print(e)


class Ship:
    def __init__(self, size: int, points: "Point", hp: int) -> None:
        self.__size: int = size
        self.points: "Point" = points
        self.hited_points: List[Point] = []
        self.__hp: int = hp
        self.destroyed: bool = False

    @property   
    def decrease_health(self):
        self.__hp -= 1
        if self.__hp <= 0:
            self.destroyed = True

        


class Board:
    def __init__(self, size: int = 6, player: "Player" = Player) -> None:
        self.__player: "Player" = player
        self.__size: int = size
        self.__field: List[List[str]] = [
            ["o" for i in range(self.__size)] for j in range(self.__size)
        ]

        self.shooted_points: List[Point] = []

    def add_hitted_point(self, point: "Point"):
        self.shooted_points.append(Point(point.x, point.y))
    
    def point_is_valid(self, point: Point,) -> bool:
        
        _points = [Point(point.x-1, point.y-1),Point(point.x-1, point.y),Point(point.x-1, point.y+1),
                    Point(point.x, point.y-1),Point(point.x, point.y),Point(point.x, point.y+1),
                    Point(point.x+1, point.y-1),Point(point.x+1, point.y),Point(point.x+1, point.y+1),]
        
        if any([point.x > 5 or point.x < 0, point.y > 5 or point.y < 0]):
            return False

        for i in self.__player.ship_points:
            if i in _points:
                return False
            
        return True

    def create_ship(self, ship_size: int) -> Ship:
        _exit: bool = False
        while not _exit:



            
            try:
                
                if type(self.__player) is type(AI()):
                    
                    _allign: str = random.choice('hv')

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

                    print(f'Сейчас {ship_size} палубный корабль')

                    if ship_size > 1:
                        _allign: str = input("Ориентация корабля: h/v") 
                        if 'h' in _allign:
                            _allign = 'h'
                        elif 'v' in _allign:
                            _allign = 'v'
                        else:
                            raise NotAllign
                    else: 
                        _allign = 'h'

                    _x: int = int(input("X↓: "))
                    _y: int = int(input("Y→: "))

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
                if (type(self.__player) is type(User())):
                    print(e)

            else:
                _exit = True
                return Ship(ship_size, _points, ship_size)
            finally:
                ...
            

    def create_ships(self) -> None:
        if type(self.__player) is type(User()):
            for ship_size in self.__player.ship_count:
                self.__player.add_ship(self.create_ship(ship_size))
                self.__player.extract_ship_points()
                self.drow_board
        elif type(self.__player) is type(AI()):
            for ship_size in self.__player.ship_count:
                self.__player.add_ship(self.create_ship(ship_size))
                self.__player.extract_ship_points()
            self.drow_board

    def drow_points(self) -> None:

        if type(self.__player) is type(User()):
            # выстрелы
            if not len(self.shooted_points) == 0:
                for point in self.shooted_points:
                    self.__field[point.x][point.y] = '⁐'
            # корабли
            for ship in self.__player.ships:
                if ship.destroyed:
                    for point in ship.points:
                        self.__field[point.x][point.y] = '✖'
                elif not len(ship.hited_points) == 0:
                    for point in ship.points:
                        if point in ship.hited_points:
                            self.__field[point.x][point.y] = '•'
                        else:
                             self.__field[point.x][point.y] = '■'
                else:
                    for point in ship.points:
                        self.__field[point.x][point.y] = '■'


        if type(self.__player) is type(AI()):
            # выстрелы
            if not len(self.shooted_points) == 0:
                for point in self.shooted_points:
                    self.__field[point.x][point.y] = '⁐'

            for ship in self.__player.ships:
                if ship.destroyed:
                    for point in ship.points:
                        self.__field[point.x][point.y] = '✖'
                elif not len(ship.hited_points) == 0:
                    for point in ship.hited_points:
                        self.__field[point.x][point.y] = '•'
                        


    @property
    def drow_board(self) -> None:

        self.__field: List[List[str]] = [
            ["o" for i in range(self.__size)] for j in range(self.__size)
        ]

        self.drow_points()
        

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



p1: User = User([3, 2, 1])

b1: Board = Board(6, p1)
b1.drow_board
b1.create_ships()





class Game:
    pass
