import os
clear = lambda: os.system('cls')



board = [[' ' for i in range (0,3)] for j in range(0,3)]

# player = "X"


#функция отрисовки доски
def draw_board(board): 
    clear()
    print("    0   1   2")
    print("  -------------")
    
    for i in range(0,3):
        print(f'{i} | {board[i][0]} | {board[i][1]} | {board[i][2]} |')# В трех шагах отрисовываю матрицу
        print("  -------------")
    print()

#функция проверки победителя
def win_condition(board, player):
    return False

#функция хода игрока
def player_move(board, X, Y, player):
    
    if player == 'X':
        board[X][Y] = player
        player = 'O'
    elif player == 'O':
        board[X][Y] = player
        player = 'X'

    draw_board(board)
    return player


def game_function():

    

    while True:
        if(input('Хотите сыграть? (Y/N)') == 'N'):
            break
        else:

            player = 'X'

            draw_board(board)

            # место для пве логики

            

            while True:

                if win_condition(board, player):
                    break
                
                print(f'сейчас ходят "{player}"')

                x, y = int(input('X ')), int(input('Y '))
                

                if all([0<=x<=2, 0<=y<=2]):
                    if board[x][y] == 'X' or board[x][y] == 'O':
                        print('Клетка уже занята!')
                    else:
                        player = player_move(board, x, y, player)
                else:
                    print('Одно из чисел вне границы сетки')

        print(f'Игра окончена, победитель - {player}')


game_function()