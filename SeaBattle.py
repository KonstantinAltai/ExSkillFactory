"""Морской бой"""
from random import randint, choice


class SeaBattleException(Exception):
    """Класс пользовательского прерываний"""
    pass

class BoardOutException(SeaBattleException):
    def __init__(self, text):
        self.txt = text

class Dot:
    """Класс точек на поле"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    # Метод переопределяет стандартное сравнение, для проверки на равенство
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    # Метод переопределяет однозначное представление объекта в виде строки, которое можно использовать, чтобы воссоздать точно такой же объект
    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

class Ship:
    """Класс корабля, пар-ры:, длина, точка носа, направление"""
    def __init__(self, length:int, point:Dot, direction:str = 'h'):
        self.length = length
        self.point = point
        self.direction = direction

    # метод возвращает список всех точек корабля.
    def dot(self):
        dot_ship = []
        for i in range(self.length):
            coord_X = self.point.x
            coord_Y = self.point.y
            if self.direction == 'h':
                coord_Y+=i
            else:
                coord_X+=i
            dot_ship.append(Dot(coord_X,coord_Y))
        return dot_ship

class Board:
    """Клаcс игровой доски, пар-ры: список состояния клеток, список кораблей доски, скрыть корабли или нет, кол-во живых"""
    def __init__(self, condition:list, hid = False):
        self.condition = condition # Состояние доски (O, X, T, █)
        self.list_ship = [] # Список кораблей доски
        self.hid = hid  # False - скрыть корабли на доске
        self.live_ship = 0 # кол-во живых кораблей
        self.contour = []

    # ставит корабль на доску (если ставить не получается, выбрасываем исключения).
    # координаты точек корабля Dot(x,y), изменяем состояние клеток на █
    def add_ship(self, ship):
        list =[d for d in ship if d in self.contour or d in self.list_ship]
        out_ = [o for o in ship if not self.out(o)]
        if list or out_:
            return False
        for sh in ship:
            if self.out(sh):
                self.condition[sh.x][sh.y]= chr(9608)
                for h in range(3):
                    if not(0 <= sh.y - 1 + h <= 5):
                        continue
                    for v in range(3):
                        if not(0 <= sh.x - 1 + v <= 5):
                            continue
                        if self.condition[sh.x - 1 + v][sh.y - 1 + h] != chr(9608):
                            self.condition[sh.x - 1 + v][sh.y - 1 + h] = '.'
                            self.contour.append(Dot(sh.x - 1 + v,sh.y - 1 + h))
            else:
                return False
        self.list_ship.extend(ship)
        self.live_ship += 1
        return True

    # возвращает False, если точка выходит за пределы поля
    @staticmethod
    def out(val):
        return (0 <= val.x <= 5) and (0 <= val.y <= 5)

    def near(self, val):
        lim = [(-1, 0), (1, 0), (0 , 1),(0, -1)]
        for x_, y_ in lim:
            coordinat = Dot(val.x + x_, val.y + y_)
            if self.out(coordinat) and self.condition[coordinat.x][coordinat.y] == chr(9608):
                return False
        return True

    # делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, нужно выбрасывать исключения)
    def shot(self, shoot:Dot):
        if self.out(shoot):
            missed = self.condition[shoot.x][shoot.y]
            if missed == 'X' or missed == 'T':
                print('Туда уже стрелял, повтори.')
                return True
            elif missed == chr(9608):
                print('Попал!')
                self.condition[shoot.x][shoot.y] = 'X'
                self.list_ship.remove(shoot)
                if self.near(shoot):
                    print('Корабль потоплен!')
                    self.live_ship -= 1
                    if self.live_ship == 0:
                       return False
                return True
            else:
                print('Мимо! Переход хода.')
                self.condition[shoot.x][shoot.y] = 'T'
        else:
            raise BoardOutException('Координаты за полем, будь внимателен!')
        return False

    # выводит доску, если hid - False, отображаются корабли
    def __str__(self):
        line_ = ''
        line_ += '  | 1| 2| 3| 4| 5| 6|'
        for i, j in enumerate(self.condition):
            line_ += f'\n{i + 1} | ' + '  '.join(j)
            line_ = line_.replace('.', 'O')
        if self.hid:
            line_ = line_.replace(chr(9608), 'O')
        return line_

class Player:
    """Класс игроков"""
    def __init__(self, board):
        self.board = board

    def ask(self):
        raise NotImplementedError()

    # Ход в игре
    def move(self, rival_board):
        while True:
            if rival_board.shot(self.ask()):
                print(rival_board)
            else:
                 break

class Al(Player):
    # Выбор случайной координаты выстрела, возвращает точку Dot
    def ask(self):
        point = Dot(randint(0, 5), randint(0, 5))
        print(f'Выстрел противника в точку {point.x + 1}{point.y + 1}')
        return point

class User(Player):
    # Запрос координаты стрельбы
    def ask(self):
        while True:
            shoot = input('Твой ход (например 11): ')
            if len(shoot) != 2 or not(shoot.isdigit()):
                print('Некорректное значение')
                continue
            return Dot(int(shoot[0]) - 1, int(shoot[1]) - 1)

class Game:
    """Класс игры"""
    def __init__(self):
        self.user = User(self.new_board())
        self.comp = Al(self.new_board(True))

    # доска - начало
    def new_board(self, visibil = False):
        board = None
        while board is None:
            board = self.random_board()
        board.hid = visibil
        return board

    # Заполнение доски
    def random_board(self):
        board = Board([['O' for i in range(6)] for j in range(6)])
        count = 0
        num_ship = [3, 2, 2, 1, 1, 1, 1]
        while num_ship:
            desk = choice(num_ship)
            while True:
                pl_ship = Ship(desk, Dot(randint(0, 5), randint(0, 5)), choice(['h', 'v']))
                if board.add_ship(pl_ship.dot()):
                    break
                if count > 2000:
                    return None
                count += 1
            num_ship.remove(desk)
        return board

    # Приветствие и правила
    def greet(self):
        print("""«Морской бой» — игра для двух участников, в которой игроки
        по очереди называют координаты на неизвестной им карте соперника.
        Если у соперника по этим координатам имеется корабль (координаты заняты),
        то корабль или его часть «топится», а попавший получает право сделать ещё один ход.""")

    # Игровой цикл
    def loop(self):
        step = True #True - ход игрока
        while True:
            print('Доска игрока')
            print(self.user.board)
            print('Доска противника')
            print(self.comp.board)
            print('Кораблей у игрока:', self.user.board.live_ship)
            print('Кораблей у копьютера:', self.comp.board.live_ship)
            if step:
                print('Твой ход')
                self.user.move(self.comp.board)
                step = False
            if self.comp.board.live_ship == 0:
                print('Поздравляю, ты победил!')
                break
            if not step:
                print('Ход противника: ')
                step = True
                self.comp.move(self.user.board)
            if self.comp.board.live_ship == 0:
                print('Извини, ты проиграл!')
                break

    # Запуск игры
    def start(self):
        self.greet()
        self.loop()

game = Game()
game.start()
