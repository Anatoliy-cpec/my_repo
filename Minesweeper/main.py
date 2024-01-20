from tkinter import *

from dataclasses import dataclass
import random
from typing import List, Any


@dataclass
class Point:

    x: int = 0
    y: int = 0

    def __eq__(self, other: Any) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"X:{self.x}  Y:{self.y}"


class Cell():
    def __init__(self, point: 'Point') -> None:
        
        self.point: 'Point' = point
        self.mined: bool = False
        self.mines_around_count: int = Any
        self.hidden: bool = True
        self.flagged: bool = False


    def get_cell_point(self) -> Point:
        return self.point
    
    def get_is_mined(self) -> bool:
        return self.mined
    
    def get_mines_around(self) -> str:
        if self.mined:
            return 'X'
        else:
            return self.mines_around_count
    
    def get_cell_color(self):
        pass

class Field():
    def __init__(self, field_size: int, mines: int) -> None:

        self.cell_matrix: List[List['Cell']] = []
        self.field_size: int = field_size
        self.cell_width: float = 25.0
        self.cell_height: float = 25.0
        self.mines: list['Point'] = []
        self.all_cell_points: list['Point'] = []
        self.frame: 'Frame' = Any
        self.canvas: 'Canvas' = Any
        self.mines_count: int = mines


    def mines_equal_flagged(self) -> bool:
        _flagged_mines: int = 0

        for i in self.mines:
            
            if self.cell_matrix[i.x][i.y].flagged:
                _flagged_mines += 1

        return _flagged_mines == self.mines_count


    def create_cells_field(self):
        self.mines: list['Point'] = []
        self._create_cells_matrix()
        self.add_all_cells_points()
        self.create_mines()
        self.add_mines_to_cell_matrix()
        self.set_mines_num_around_to_cells()

    def _create_cells_matrix(self):
        self.cell_matrix = [[Cell(Point(j,i)) for i in range(self.field_size)] for j in range(self.field_size)]
    
    def add_all_cells_points(self) -> None:

        for i in self.cell_matrix:
            for j in i:
                self.all_cell_points.append(j.get_cell_point())

    def create_mines(self):
    
        _i: int = 0
        
        while _i < self.mines_count:
            _mine = Point(random.randint(0, self.field_size-1), random.randint(0, self.field_size-1))
            if _mine in self.mines:
                continue
            else:
                self.mines.append(_mine)
                _i += 1

    def add_mines_to_cell_matrix(self) -> None:
        for mine in self.mines:
            self.cell_matrix[mine.x][mine.y].mined = True

    def check_mines_around_point(self, point: 'Point') -> int:

        _mines_count: int = 0

        _points = [Point(point.x-1, point.y-1),Point(point.x-1, point.y),Point(point.x-1, point.y+1),
                    Point(point.x, point.y-1),Point(point.x, point.y),Point(point.x, point.y+1),
                    Point(point.x+1, point.y-1),Point(point.x+1, point.y),Point(point.x+1, point.y+1),]
        
        for i in _points:
            if i in self.all_cell_points and i != point:
                if self.cell_matrix[i.x][i.y].mined:
                    _mines_count += 1

        return _mines_count

    def set_mines_num_around_to_cells(self) -> None:

        for i in self.all_cell_points:
            self.cell_matrix[i.x][i.y].mines_around_count = self.check_mines_around_point(i)


class Board():
    
    def __init__(self, field: 'Field'):
        self.field: 'Field' = field
        self.rectangles_matrix: List[List[int]] = [[i for i in range(self.field.field_size)] for j in range(self.field.field_size)]
        self.labels_matrix: List[List[int]] = [[i for i in range(self.field.field_size)] for j in range(self.field.field_size)]
        self.root = Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.frame = Frame(self.root, bg='green', bd=5, width=round(self.screen_width/2), height=round(self.screen_height/2))
        self.upper_frame = Frame(self.frame, bg='gray', borderwidth=5, highlightbackground='#ff0000', width=round(self.field.cell_width * self.field.field_size), height=50)
        self.canvas = Canvas(self.frame, height=self.field.cell_height * self.field.field_size, width=self.field.cell_width * self.field.field_size, bg='gray', borderwidth=0, highlightthickness=0)
        self.game: 'Game' = Any

    def get_valid_points_around(self, point: 'Point')-> List['Point']:

        _points = [Point(point.x-1, point.y-1),Point(point.x-1, point.y),Point(point.x-1, point.y+1),
                    Point(point.x, point.y-1),Point(point.x, point.y),Point(point.x, point.y+1),
                    Point(point.x+1, point.y-1),Point(point.x+1, point.y),Point(point.x+1, point.y+1),]
        
        points = []
        
        for i in _points:
            if i in self.field.all_cell_points: 
                points.append(i)

        return points


    def open_cells_around(self, point: 'Point'):

        _points: List['Point'] = self.get_valid_points_around(point)
        self.field.cell_matrix[point.x][point.y].hidden = False
        
        for i in _points:
            _mines_count = self.field.cell_matrix[i.x][i.y].get_mines_around()

            if self.field.cell_matrix[i.x][i.y].hidden:
                self.canvas.itemconfig(self.rectangles_matrix[i.x][i.y], fill='white')
                self.canvas.itemconfig(self.labels_matrix[i.x][i.y], text=_mines_count, fill=self.get_mines_color(_mines_count) )
                if _mines_count == 0:
                    self.open_cells_around(Point(i.x,i.y))
                else:
                    self.field.cell_matrix[i.x][i.y].hidden = False
                    
            
    
    def open_cell(self, mined: bool, mines: int, color: str, x: int, y: int):
        
        if mined:
            self.canvas.itemconfig(self.rectangles_matrix[x][y], fill='red')
            self.game_over()
        else:
            if mines == 0:
                
                self.canvas.itemconfig(self.rectangles_matrix[x][y], fill='white')
                self.open_cells_around(Point(x,y))
            else:
                
                self.field.cell_matrix[x][y].hidden = False
                self.canvas.itemconfig(self.rectangles_matrix[x][y], fill='white')
                self.canvas.itemconfig(self.labels_matrix[x][y], text=mines, fill=color )

    def game_over(self):
        self.clear_events()
        


    def clear_board(self):
        self.field.create_cells_field()
        self.canvas.delete('all')

    def clear_events(self):
        for i in self.rectangles_matrix:
            for j in i:
                self.canvas.tag_unbind(j, '<Button-1>')
                self.canvas.tag_unbind(j, '<Button-3>')

        for i in self.labels_matrix:
            for j in i:
                self.canvas.tag_unbind(j, '<Double-Button-1>')
                
                
        


    def get_mines_color(self, mines: int) -> str:

        _color: str = 'white'

        if mines == 1:
            _color = 'blue'
        elif mines == 2:
            _color = 'green'
        elif mines == 3:
            _color = 'red'
        elif mines == 4:
            _color = 'maroon'
        elif mines == 5:
            _color = 'brown'
        elif mines == 6:
            _color = 'black'

        return _color

    def check_cell(self, point: 'Point') -> None:
        _x: int = point.x
        _y: int = point.y
        _mined: bool = self.field.cell_matrix[_x][_y].get_is_mined()
        _cell: 'Cell' = self.field.cell_matrix[_x][_y]
        _cell_mines: int = _cell.get_mines_around()
        _flagged = _cell.flagged
        _color: str = self.get_mines_color(_cell_mines)
        _hidden = self.field.cell_matrix[_x][_y].hidden

        if _hidden and not _flagged:
            self.open_cell(_mined, _cell_mines, _color, _x, _y)

    def check_cell_around_flagged(self, point: 'Point'):

        _points: List['Point'] = self.get_valid_points_around(point)
        
        for i in _points:
            _x: int = i.x
            _y: int = i.y
            _mined: bool = self.field.cell_matrix[_x][_y].get_is_mined()
            _cell: 'Cell' = self.field.cell_matrix[_x][_y]
            _cell_mines: int = _cell.get_mines_around()
            _color: str = self.get_mines_color(_cell_mines)
            _hidden = self.field.cell_matrix[_x][_y].hidden
            _flagged = _cell.flagged

            

            if not _flagged:
                if _hidden:
                    self.open_cell(_mined, _cell_mines, _color, _x, _y)

    def set_cell_flaged(self, point: 'Point'):
        _x: int = point.x
        _y: int = point.y
        _hidden = self.field.cell_matrix[_x][_y].hidden
        _flagged: bool = self.field.cell_matrix[_x][_y].flagged
        if _hidden:
            if _flagged:
                self.field.cell_matrix[_x][_y].flagged = False
                self.canvas.itemconfig(self.rectangles_matrix[_x][_y], fill='gray')
                self.game.check_win_condition()
            else:
                self.field.cell_matrix[_x][_y].flagged = True
                self.canvas.itemconfig(self.rectangles_matrix[_x][_y], fill='blue')
                self.game.check_win_condition()

    def board_press(self, event: 'Event', tag):
        _tags = event.widget.gettags(tag)
        _column: int = int(_tags[0])
        _row: int =  int(_tags[1])
        self.check_cell(Point(_column, _row))

    def board_right_press(self, event: 'Event', tag):
        _tags = event.widget.gettags(tag)
        _column: int = int(_tags[0])
        _row: int =  int(_tags[1])
        self.set_cell_flaged(Point(_column, _row))
        
    def board_double_press(self, event: 'Event', tag):
        _tags = event.widget.gettags(tag)
        _column: int = int(_tags[0])
        _row: int =  int(_tags[1])
        
        self.check_cell_around_flagged(Point(_column, _row))

    def create_board(self):
        self.root.geometry(f"{round(self.field.cell_height * (self.field.field_size + 1))}x{round(self.field.cell_width * (self.field.field_size + 5))}")
        self.frame.pack(anchor=CENTER, expand=1)
        self.canvas.pack_propagate(0)
        self.upper_frame.pack(anchor=CENTER, expand=1)
        self.upper_frame.pack_propagate(0)
        button1=Button(self.upper_frame,text='ok',width=10,height=2,bg='black',fg='red',font='arial 7')
        button1.grid(row=1, column=1, sticky='e')
        button2=Button(self.upper_frame,text='ok',width=10,height=2,bg='black',fg='red',font='arial 7')
        button2.grid(row=1, column=2, sticky='w')
        self.canvas.pack(anchor=CENTER, expand=1)
        
        

    def create_rectangles(self, column: int, row: int ,x1, y1, x2, y2):
        rectangle = self.canvas.create_rectangle(x1,y1,x2,y2, fill='gray', tags=[column, row])

        press = lambda event, tag=rectangle: self.board_press(event, tag)
        self.canvas.tag_bind(rectangle, '<Button-1>', press)

        right_button_press = lambda event, tag=rectangle: self.board_right_press(event, tag)
        self.canvas.tag_bind(rectangle, '<Button-3>', right_button_press)

        self.rectangles_matrix[column][row] = rectangle

    def create_labels(self, column: int, row: int, x1, y1):
        
        label = self.canvas.create_text(((x1 + self.field.cell_width/2), (y1+self.field.cell_height/2)), font='bold', tags=[column, row])
        double_press = lambda event, tag=label: self.board_double_press(event, tag)
        self.canvas.tag_bind(label, '<Double-Button-1>', double_press)
        self.labels_matrix[column][row] = label

    def create_figures_and_add_to_matrix(self):
        for column in range(self.field.field_size):
            for row in range(self.field.field_size):
                x1 = column*self.field.cell_width
                y1 = row * self.field.cell_height
                x2 = x1 + self.field.cell_width
                y2 = y1 + self.field.cell_height
                self.create_rectangles(column, row, x1, y1, x2, y2)

        for column in range(self.field.field_size):
            for row in range(self.field.field_size):
                x1 = column*self.field.cell_width
                y1 = row * self.field.cell_height
                x2 = x1 + self.field.cell_width
                y2 = y1 + self.field.cell_height
                self.create_labels(column, row, x1, y1)

    def draw_board(self):
        
        self.create_figures_and_add_to_matrix()
        self.root.mainloop()
    
    

class Game():
    def __init__(self, field: 'Field', board: 'Board'):
        self.board: 'Board' = board
        self.field: 'Field' = field
        self.board.game = self

    def new_game(self):
        self.field.create_cells_field()
        self.board.create_board()
        self.board.draw_board()

    def start_game(self):

        self.new_game()

    def restart_game(self):
        pass

    def close_game(self):
        pass

    def check_win_condition(self):
        
        if self.field.mines_equal_flagged():
            self.board.clear_events()
            print('win')

    

f1 = Field(15, 15)

b1 = Board(f1)

g1 = Game(f1, b1)

b1.game.start_game()

