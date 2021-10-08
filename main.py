import random

Field = ['-' for i in range(9)]
first = False
symbol_man = '0'
symbol_comp = '0'
WIN = False


# ф-ия вывода на экран игрового поля
def board():
    print('  0 1 2 ')
    for i in range(3):
        print(i, Field[3 * i], Field[3 * i + 1], Field[3 * i + 2])


# ф-ия анализа сделанного хода и окончания игры
def winner(sym):
    move = Field[:]
    move_index = [index for index, v in enumerate(move) if v == sym]
    win_combination = [(0, 1, 2),
                       (3, 4, 5),
                       (6, 7, 8),
                       (0, 3, 6),
                       (1, 4, 7),
                       (2, 5, 8),
                       (0, 4, 8),
                       (2, 4, 6)]
    for comb in win_combination:
        if list(comb) == [x for x in move_index if x in comb]:
            print('WINNER!!!', sym)
            return True
    if '-' not in Field:
        print('DRAW')
        return True
    return False


# Ход игрока
def move_player(symbol):
    global first
    list_sq = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
    move = input('Your move: ')
    while True:
        if move not in list_sq or Field[int(move[0]) * 3 + int(move[1])] != '-':
            move = input('Invalid value, Try again: ')
        else:
            break
    Field[int(move[0]) * 3 + int(move[1])] = symbol
    first = False
    board()


# Ход компьютера
def move_comp(symbol):
    global first
    mov = random.randrange(0, 9)
    print('Move computer..')
    while True:
        if Field[mov] == '-':
            break
        else:
            mov = random.randrange(0, 9)
    Field[mov] = symbol
    first = True
    board()


# Main, Правил немного, определяем кто первый начинает и выводим пустую доску
print('''Кре́стики-но́лики — логическая игра между двумя противниками на квадратном поле 3 на 3 клетки.
Один из игроков играет «крестиками», второй — «ноликами». Начинают ход крестики. Ход - производится 
вводом координат игрового поля (напримен 01)  
''')
board()
start_player = input('You will start - X? (y/n): ')
while start_player != 'y' or start_player != 'n':
    if start_player == 'y':
        print('Start you')
        first = True
        symbol_man = 'x'
        break
    elif start_player == 'n':
        print('Start computer')
        symbol_comp = 'x'
        break
    else:
        start_player = input('Must click y or n: ')
while not WIN:
    if first:
        move_player(symbol_man)
        WIN = winner(symbol_man)
    else:
        move_comp(symbol_comp)
        WIN = winner(symbol_comp)
