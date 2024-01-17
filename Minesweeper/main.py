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

    def get_cell_point(self) -> Point:
        return self.point

class Field():
    def __init__(self, field_size: int) -> None:

        self.cell_matrix = [[Cell(Point(j,i)) for i in range(field_size)] for j in range(field_size)]
        self.field_size: int = field_size
        self.cell_width: float = 25.0
        self.cell_height: float = 25.0
        self.mines: list['Point'] = []
        self.all_cell_points: list['Point'] = []
        self.frame = Any
        self.canvas = Any
    
    def get_all_cells_points(self) -> None:

        for i in self.cell_matrix:
            for j in i:
                self.all_cell_points.append(j.get_cell_point())

    def create_mines(self):
    
        _i: int = 0
        while _i < self.field_size*3:
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

        


    def check_cell(self, point: 'Point'):
        pass

class Board():
    def __init__(self, field: 'Field'):
        self.field: 'Field' = field

    def board_press(self, event: 'Event', tag):
        _tags = event.widget.gettags(tag)
        _column, _row = _tags[0], _tags[1]
        self.field.check_cell(Point(_column, _row))

    

    def draw_board(self):
        root = Tk()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root.geometry(f"{round(self.field.cell_height * (self.field.field_size + 1))}x{round(self.field.cell_width * (self.field.field_size + 1))}")

        self.frame = Frame(root, bg='green', bd=5, width=round(screen_width/2), height=round(screen_height/2))
        self.frame.pack(anchor=CENTER, expand=1)
        canvas = Canvas(self.frame, height=self.field.cell_height * self.field.field_size, width=self.field.cell_width * self.field.field_size, bg='gray', borderwidth=0, highlightthickness=0)
        canvas.pack(anchor=CENTER, expand=1)
        
        for column in range(self.field.field_size):
            for row in range(self.field.field_size):
                x1 = column*self.field.cell_width
                y1 = row * self.field.cell_height
                x2 = x1 + self.field.cell_width
                y2 = y1 + self.field.cell_height
                
                rectangle = canvas.create_rectangle(x1,y1,x2,y2, fill='white', tags=[column, row])
                callback = lambda event, tag=rectangle: self.board_press(event, tag)
                canvas.tag_bind(rectangle, '<Button-1>', callback)


        # for i in range(self.field.size):
        #     for j in range(self.field.size):
        #         if self.field.cell_matrix[i][j].mined:
        #             button = Button(frame, width=2, height=1, font='Arial 0', text=f'X')
        #             button.grid(row=i+1, column=j+1)
        #         else:
        #             button = Button(frame, width=2, height=1, font='Arial 0',  text='✲')
        #             button.grid(row=i+1, column=j+1)

        root.mainloop()
    
    def get_canvas(self) -> Canvas:
        return canvas

class Game():
    pass

f1 = Field(5)

b1 = Board(f1)


f1.get_all_cells_points()
f1.create_mines()
f1.add_mines_to_cell_matrix()
f1.set_mines_num_around_to_cells()
b1.draw_board()


