
from dataclasses import dataclass
import random
from typing import List, Any

# Создаю свой класс для хранения координат
@dataclass
class Point:
    x: int = 0
    y: int = 0

    # переопределяю сравнение для более удобного использования
    def __eq__(self, other: Any) -> bool:
        return self.x == other.x and self.y == other.y
    # то же самое проделываю с методом печати
    def __str__(self) -> str:
        return f"X:{self.x}  Y:{self.y}"


# создаю свой класс исключений
class MyException(Exception):
    def __str__(self) -> str:
        return f"(My exception class)"

# Создаю свои классы исключений для пользовательских ошибок
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

# /////////////////////////////////////////////////
# Класс игрока
class Player:
    # в игроке записываю количество кораблей в виде списка целых чисел
    def __init__(self, ship_count: List[int] = [3, 2, 1]) -> None:
        # создаю список в котором буду хранить объекты класса Ship
        self.ships: List[Ship] = []     
        # список точек корабля для упрощения отрисовки на этапе заполнения доски
        self.ship_points: List[Point] = []
        # лист с количеством кораблей, далее по числам буду определять количество палуб
        self.ship_count: List[int] = ship_count
    # функция для добавления объекта класса ship в лист кораблей
    def add_ship(self, ship: "Ship"):
        self.ships.append(ship)

    # метод для извлечения всех точек кораблей
    def extract_ship_points(self) -> None:
        self.ship_points: List[Point] = []
        for ship in self.ships:
            for point in ship.points:
                self.ship_points.append(point)


# класс ИИ (так называть классы не рекомендуется, но Ai режет гла)
class AI(Player):
    def __init__(self, ship_count: List[int] = [3, 2, 1]) -> None:
        super().__init__(ship_count)
    # функция стрельбы 
    def shoot(self, enemy: "Board") -> Any:
        # переменная для выхода из цикла
        _exit: bool = False
        # пока переменная = False вызывается тело цикла
        while not _exit:
            # этот блок не только для отлова но и помогает закончить цикл, если все прошло гладко то
            #  _exit = True
            try:
                print('Ход ИИ')

                # переменная которая указывает было ли попадание
                _hited: bool = False
                # тут храню количество уничтоженных кораблей для проверки условий победы
                #  т.к. не нашел способа проще для проверки условий победы при попадании
                # в последний корабль(точку)
                _destroyed: int = 0

                    
                _x: int = random.randint(1,6)
                _y: int = random.randint(1,6)

                # если точка за границей то выкидываю свою ошибку и повторяю тело цикла
                if (_x < 1 or _x > 6) or (_y < 1 or _y > 6):
                    raise OutOfRange
                
                # создаю объект Point с координатами только если ошибок нет
                _p : "Point" = Point(_x-1,_y-1)

                # проверяю есть ли эта точка в списке точек в которые уже стрелял
                if _p in enemy.shooted_points:
                    # усли да то повторяю тело цикла
                    raise OccupiedPoint
                else:
                    # если все гладко то добавляю точку в массив точек в которые стрелял
                    enemy.add_hitted_point(_p)

                    # прохожу по всем точкам всех кораблей врага
                    for ship in enemy.player.ships:
                        for point in ship.points:
                            # если точка совпадает с точкой корабля то:
                            if point == _p:
                                # уменьшаю хп этого корабля
                                ship.decrease_health
                                # добавляю ему эту точку как подбитую
                                ship.hited_points.append(_p)
                                # обозначаю что было попадание
                                _hited = True

                    # проверяю сколько кораблей уничтожено
                    for ship in enemy.player.ships:
                        if ship.destroyed:
                            _destroyed += 1
                    # если все уничтожены то выхожу из цикла без последущего хода
                    if _destroyed >= len(enemy.player.ships):
                        _exit = True
                    # если попал то запускаю след итерацию с сохраненными точками
                    elif _hited:
                        print("Есть попадание")
                        print(Point(_x,_y))
                        continue
                    else:
                        print("Мимо")
                        print(Point(_x,_y))

            except Exception as e:
                pass

            else:
                _exit = True
            
            finally:
                pass
            

# тут то же что и выше только для игрока
class User(Player):
    def __init__(self, ship_count: List[int] = [3, 2, 1]) -> None:
        super().__init__(ship_count)

    def shoot(self, enemy: "Board") -> Any:
        _exit: bool = False
        while not _exit:
            try:
                print('Ход Игрока')

                _hited: bool = False
                _destroyed: int = 0

                    
                _x: int = int(input("X↓: "))
                _y: int = int(input("Y→: "))

                if (_x < 1 or _x > 6) or (_y < 1 or _y > 6):
                    raise OutOfRange

                _p : "Point" = Point(_x-1,_y-1)

                if _p in enemy.shooted_points:
                    raise OccupiedPoint
                else:
                    enemy.add_hitted_point(_p)

                    for ship in enemy.player.ships:
                        for point in ship.points:
                            if point == _p:
                                ship.decrease_health
                                ship.hited_points.append(_p)
                                _hited = True
                                enemy.drow_board
                    
                    for ship in enemy.player.ships:
                        if ship.destroyed:
                            _destroyed += 1

                    if _destroyed >= len(enemy.player.ships):
                        _exit = True
                        
                    elif _hited:
                        print("Есть попадание")
                        print(Point(_x,_y))
                        continue
                    else:
                        print("Мимо")
                        print(Point(_x,_y))

            except Exception as e:
                print(e)

            else:
                _exit = True
            
            finally:
                pass
            


# класс корабля, нужен для хранения точек, подбитых точек, хп и состояния уничтожен или нет
class Ship:
    def __init__(self, size: int, points: "Point", hp: int) -> None:
        self.__size: int = size
        self.points: "Point" = points
        self.hited_points: List[Point] = []
        self.__hp: int = hp
        self.destroyed: bool = False
    # метод уменьшающий хп корабля при попадании мо нему
    @property   
    def decrease_health(self):
        self.__hp -= 1
        if self.__hp <= 0:
            self.destroyed = True

# Основной класс в игре, тут хранятся почти все методы
class Board:
    def __init__(self, size: int = 6, player: "Player" = Player) -> None:
        # записываю в переменную хозяина доски
        self.player: "Player" = player
        # определяю размер доски, по умолчанию 6 но можно и больше, хотя не рекомендую больше 10
        self.__size: int = size
        # поле, тут оно только для отрисовки точек, они не хранятся в нем по индексам как строки а каждый
        # раз перезаписываются из точек (я так делал крестики нолики)
        self.__field: List[List[str]] = [
            ["o" for i in range(self.__size)] for j in range(self.__size)
        ]

        # подбитые точки
        self.shooted_points: List[Point] = []


    def add_hitted_point(self, point: "Point"):
        self.shooted_points.append(Point(point.x, point.y))
    
    # проверка на валидность точки для размещения корабля
    def point_is_valid(self, point: Point,) -> bool:
        
        # массив точек вокруг той что подал на вход
        _points = [Point(point.x-1, point.y-1),Point(point.x-1, point.y),Point(point.x-1, point.y+1),
                    Point(point.x, point.y-1),Point(point.x, point.y),Point(point.x, point.y+1),
                    Point(point.x+1, point.y-1),Point(point.x+1, point.y),Point(point.x+1, point.y+1),]
        
        # проверяю не выходит ли точка за границу т.е. если первая точка трехпалубника 6.6 она валидна
        # а 6.7, 6.8 уже нет
        if any([point.x > 5 or point.x < 0, point.y > 5 or point.y < 0]):
            return False

        # проверяю все точки вокруг той что подал на вход 
        for point in self.player.ship_points:
            if point in _points:
                return False

        # если все упешно возвращаю True
        return True

    # функция создания одного корабля
    def create_ship(self, ship_size: int) -> Ship:
        # на вход подаю один элемент из списка кораблей игрока

        # аналогично способу выше, не тольк оловлю ошибки но и выхожу из цикла только если все хорошо
        _exit: bool = False
        while not _exit:
            try:
                # в зависимости от владельца доски меняю код
                if type(self.player) is type(AI()):
                    
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

                # код для игрока
                elif type(self.player) is type(User()):

                    print(f'Сейчас {ship_size} палубный корабль')

                    if ship_size > 1:
                        _allign: str = input("Ориентация корабля: h/v ") 
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
                if (type(self.player) is type(User())):
                    print(e)

            else:
                _exit = True
                return Ship(ship_size, _points, ship_size)
            finally:
                ...

    # метод создания кораблей, тоесть всех сразу с использованием метода создания одного корабля
    @property
    def create_ships(self) -> None:
        if type(self.player) is type(User()):
            self.drow_board
            # для каждого элемента списка кораблей передаю его как значение длинны корабля
            for ship_size in self.player.ship_count:
                self.player.add_ship(self.create_ship(ship_size))
                self.player.extract_ship_points()
                self.drow_board
        elif type(self.player) is type(AI()):
            for ship_size in self.player.ship_count:
                self.player.add_ship(self.create_ship(ship_size))
                self.player.extract_ship_points()
            
    # метод отрисовки всех точек на доске
    def drow_points(self) -> None:

        if type(self.player) is type(User()):
            # выстрелы
            if not len(self.shooted_points) == 0:
                for point in self.shooted_points:
                    self.__field[point.x][point.y] = '✲'
            # корабли
            # прохожу по всем кораблям 
            for ship in self.player.ships:
                # если корабль уничтожен
                if ship.destroyed:
                    for point in ship.points:
                        self.__field[point.x][point.y] = '✖'
                # если есть подбитые точки
                elif not len(ship.hited_points) == 0:
                    # прохожу по всем точкам корабля
                    for point in ship.points:
                        # рисую подбитые точки
                        if point in ship.hited_points:
                            self.__field[point.x][point.y] = '✹'
                        # рисую точки корабля
                        else:
                            self.__field[point.x][point.y] = '■'
                # если нет подбитых точек рисую точки корабля
                else:
                    for point in ship.points:
                        self.__field[point.x][point.y] = '■'


        if type(self.player) is type(AI()):
            # выстрелы
            if not len(self.shooted_points) == 0:
                for point in self.shooted_points:
                    self.__field[point.x][point.y] = '✲'
            # корабли
            # то же самое что и выше но без точек корабля т.к. это компьютер
            for ship in self.player.ships:
                if ship.destroyed:
                    for point in ship.points:
                        self.__field[point.x][point.y] = '✖'
                elif not len(ship.hited_points) == 0:
                    for point in ship.hited_points:
                        self.__field[point.x][point.y] = '✹'
                        

    # метод который отрисовывает доску в консоль
    @property
    def drow_board(self) -> None:

        # каждый раз при отрисовке отчищаю доску
        self.__field: List[List[str]] = [
            ["o" for i in range(self.__size)] for j in range(self.__size)
        ]

        # потом добавляю в массив точки
        self.drow_points()
        
        # и гибко отрисовываю все что получилось
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

# класс игры, нужен для запуска, собирает все классы в себе
class Game:
    def __init__(self, user: "User", AI: "AI", AI_board: "Board", user_board: "Board"):
        # объявляю занчения хранящие в себе игрока, ИИ, и обе доски 
        self.user: "User" = user
        self.AI: "AI" = AI
        self.AI_board: "Board" = AI_board
        self.user_board: "Board" = user_board

    # проверяю условия победы
    def win_condition(self) -> bool:
        _user_destroyed: int = 0
        _AI_destroyed: int = 0

        for ship in self.user.ships:
            if ship.destroyed:
                _user_destroyed += 1

        for ship in self.AI.ships:
            if ship.destroyed:
                _AI_destroyed += 1

        if _user_destroyed >= len(self.user.ships):
            print('Победил ИИ')
            return True
        elif _AI_destroyed >= len(self.AI.ships):
            print('Победил Игрок')
            return True
        
        return False

    # метод вызова начала игры
    @property
    def game_start(self):
        
        print(f"\n Игра 'Морской бой' начинается")
        
        # ИИ, а потом и игрок создают корабли
        self.AI_board.create_ships
        self.user_board.create_ships
        # счетчик хода для того кто ходит
        _i: int = 1
        # все та же конструкция
        _exit = False
        while not _exit:

            # первым ходит игрок
            if _i % 2 == 1:
                print("Ход игрока ")
                # рисую доску
                self.AI_board.drow_board
                # стреляю
                self.user.shoot(self.AI_board)
                # рисую доску противника 
                self.AI_board.drow_board
                # проверяю условия победы
                _exit = self.win_condition()
            # вторым ходит ИИ
            elif _i % 2 == 0:
                print("Ход ИИ ")
                self.user_board.drow_board
                self.AI.shoot(self.user_board)
                self.user_board.drow_board
                _exit = self.win_condition()

            # увеличиваю счетчик
            _i += 1
        print(f'\n Конец игры')

# Подготавливаю все переменные


p1: "User" = User()
p2: "AI" = AI()

# в доску при создании так же передаю ее владельца
# по идее все должно работать и с разными значениями размера досок, но 6 это оптимальный
b1: "Board" = Board(6,p1)
b2: "Board" = Board(6,p2)
# передаю их в игру
game: "Game" = Game(p1, p2, b2, b1)
# запускаю игру
game.game_start