from random import randint

#Родительский класс
class AllIsk(Exception):
    pass

#Мимо доски
class MissBoardIsk(AllIsk):
    def __str__(self):
        return "Выстрел мимо доски"

#Повторный вытрел
class DoubleShotIsk(AllIsk):
    def __str__(self):
        return "Туда уже стреляли"

#Ошибка установки корабля
class PlaceShipIsk(AllIsk):
    pass

#Класс точек координаты(x,y)
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f'Dot:({self.x},{self.y})'

#Класс кораблей(длинна, координаты носа, направление(0-верт,1 - гориз), ХП)
class Ship:
    def __init__(self, nose, lenth,  rot):
        self.lenth = lenth
        self.nose = nose
        self.rot = rot
        self.hp = lenth

    #Метод возвращающий точки корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lenth):
            cur_x = self.nose.x
            cur_y = self.nose.y
            if self.rot == 0:
                cur_x += i
            if self.rot == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    #метод проверки попадания
    def shoten(self,shot):
        return shot in self.dots

#Класс игрового поля
class Board:
    def __init__(self, size = 6, hid = False):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    #Метод добавления корабля
    def add_ship(self, ship):
        #проверка на возможность установки
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise PlaceShipIsk()
        #установка
        for dot in ship.dots:
            self.field[dot.x][dot.y] = '∎'
            self.busy.append(dot)
        self.ships.append(ship)
        self.countur(ship)

    #Метод контура корабля
    def countur(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:
            for dx, dy in near:
                cur = Dot(dot.x + dx, dot.y +dy)
                if not(self.out(cur)) and cur not in self.busy:
                    #помечивание точек после подбития корабля
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    #Метод вывода доски в зависимости от параметра hid
    def __str__(self):
        res = ''
        #res += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        res += '   ' + ''.join([(f'| {i+1} ') for i in range(self.size)])+'|'
        for i, row in enumerate(self.field):
            res += f'\n {i+1} | ' + ' | '.join(row)+ ' |'
        if self.hid == True:
            res = res.replace('∎', 'O')
        return res

    #Метод принадлежности точки доске
    def out(self, dot):
        return not((0 <= dot.x <= self.size-1) and (0 <= dot.y <= self.size-1))

    #Метод выстрела по точке
    def shot(self, dot):
        #Выстрел мимо доски
        if self.out(dot):
            raise MissBoardIsk()
        #Повторный выстрел в точку
        if dot in self.busy:
            raise DoubleShotIsk()
        self.busy.append(dot)
        #Подбитие корабля
        for ship in self.ships:
            if dot in ship.dots:
                ship.hp -= 1
                self.field[dot.x][dot.y] = 'X'
                if ship.hp == 0:
                    self.count += 1
                    self.countur(ship, verb=True)
                    print('Корабль уничтожен!')
                    return True
                else:
                    print('Корабль ранен')
                    return True

        self.field[dot.x][dot.y] = '.'
        print('Промах')
        return False

    #Очистка списка занятых точек перед началом игры
    def begin(self):
        self.busy = []

#Материнский класс игрока(своя доска, доска врага)
class Player:
    def __init__(self, self_board, enemy_board):
        self.self_board = self_board
        self.enemy_board = enemy_board
    #Метод запроса выстрела
    def ask(self):
        raise NotImplementedError()
    #Метод определяющий повторение хода в зависимости от выстрела
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except AllIsk as e:
                print(e)

#Класс пользователя
class User(Player):
    def ask(self):
        while True:
            coords = input('Ваш ход: ').split()
            if len(coords) != 2:
                print('Введите 2 координаты!')
                continue
            y, x = coords
            if not(x.isdigit()) or not(y.isdigit()):
                print("Введите числа!")
                continue
            x, y = int(x), int(y)
            return Dot(x-1, y-1)

#Класс ИИ:
class AI(Player):
    def ask(self):
        dot = Dot(randint(0,5), randint(0,5))
        print(f"Ход компьютера: ({dot.x+1},{dot.y+1})")
        return dot

#Класс игры
class Game:

    def __init__(self, size = 6):
        self.size = size
        pb = self.gen_board()
        aib = self.gen_board()
        aib.hid = True
        self.us = User(pb, aib)
        self.ai = AI(aib, pb)



    #Метод генерации случайной доски
    def random_board(self):
        lenth = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for l in lenth:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except PlaceShipIsk:
                    pass
        board.begin()
        return board

    #Повтор генерации доски до успеха
    def gen_board(self):
        board = None
        while board is None:
            board = self.random_board()
        return board

    #Приветствие пользователя, правила игры
    def greet(self):
        print('''
        Игра морской бой
        Игровые доски генерируются автоматически
        Ход вводится в формате: x y
        X - горизонтальная координата
        Y - вертикальная координата
        Приятной игры
        ''')
    #Метод печати досок
    def game_print(self):
        print("-" * 28)
        print("Доска пользователя:")
        print(self.us.self_board)
        print("-" * 28)
        print("Доска компьютера:")
        print(self.ai.self_board)

    #Метод цикла игры
    def loop(self):
        num = 0
        while True:
            self.game_print()
            if num % 2 == 0:
                print("-" * 28)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 28)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            #проверка победы от кол-ва кораблей
            if self.ai.self_board.count == len(self.ai.self_board.ships):
                print("-" * 28)
                print("Пользователь выиграл!")
                self.game_print()
                break

            if self.us.self_board.count == len(self.us.self_board.ships):
                print("-" * 20)
                print("Компьютер выиграл!")
                self.game_print()
                break
            num += 1
    #Метод старта игры
    def start(self):
        self.greet()
        self.loop()
g=Game()
g.start()
