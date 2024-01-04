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
        return f"(Out of range)"


class OccupiedPoint(MyException):
    def __str__(self) -> str:
        return f"(Point is occupied)"


class Player:
    def __init__(self, board: "Board") -> None:
        self.ships: List[Point] = []
        self.ship_points: List[Point] = []
        self.ship_count: int = 7
        self.board: "Board" = board

    def add_ship(self, point: Point) -> None:
        self.ships.append(point)

    def add_points(self) -> None:
        pass

    def get_points(self) -> None:
        pass


class AI(Player):
    def shoot(self) -> None:
        pass


class User(Player):
    def shoot(self) -> None:
        pass


class Ship:
    def __init__(self, size: int, align: str, hp: int) -> None:
        self.__size: int = size
        self.__align: str = align
        self.__hp: int = hp


class Board:
    def __init__(self, size: int = 6) -> None:
        self.__size: int = size
        self.__field: List[List[str]] = [
            ["o" for i in range(self.__size)] for j in range(self.__size)
        ]

    def create_ship(self) -> None:
        _i: bool = True
        while _i:
            try:
                ...
            except Exception as e:
                raise Exception(e)
            else:
                ...
            finally:
                ...
            # end try

    def create_ships(self, player: Player) -> None:
        for i in range(player.ship_count):
            player.add_ship(self.create_ship())

    def add_ships_to_board(self) -> None:
        pass

    @property
    def drow_board(self) -> None:
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


b1: Board = Board(6)
p1: Player = Player(b1)

p1.board.drow_board
p1.board.add_ships(p1)


class Game:
    pass
