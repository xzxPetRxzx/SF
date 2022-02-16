def ask(n):
# ввод хода и проверка корректности/свободности
    while True:
        if n == 0:
            print('Ход 0')
        else:
            print('Ход X')
        x, y = map(int, input('введите координаты хода через пробел\n').split())
        if 0 <= x <= 2 and 0 <= y <= 2 and Game_field[x][y] == ' ':
            return x,y
        else: print('сюда сходить нельзя')

def print_field():
# Печать игрового поля
    print('|   | 0 | 1 | 2 |')
    print('-----------------')
    for i in range(3):
        print(f"| {i} | {' | '.join(Game_field[i])} |")
        print('-----------------')

def check_win(n):
# Проверка победы/ничьей
    if n == 0:
        win = ['0', '0', '0']
    else:
        win = ['X', 'X', 'X']
    #проверка комбинации по горизонтали
    for i in range(3):
        if Game_field[i] == win:
            print_field()
            if n == 0:
                print('Победили 0')
                print('Конец игры')
            else:
                print('Победили X')
                print('Конец игры')
            return True
    #проверка комбинации по вертикали
    for j in range(3):
        vert = []
        for i in range(3):
            vert.append(Game_field[i][j])
        if vert == win:
            print_field()
            if n == 0:
                print('Победили 0')
                print('Конец игры')
            else:
                print('Победили X')
                print('Конец игры')
            return True
    #проверка диагонали слева направо
    diag = []
    for i in range(3):
        diag.append(Game_field[i][i])
    if diag == win:
        print_field()
        if n == 0:
            print('Победили 0')
            print('Конец игры')
        else:
            print('Победили X')
            print('Конец игры')
        return True
    # проверка диагонали справа налево
    diag = []
    for i in range(3):
        diag.append(Game_field[i][2-i])
    if diag == win:
        print_field()
        if n == 0:
            print('Победили 0')
            print('Конец игры')
        else:
            print('Победили X')
            print('Конец игры')
        return True
    #Проверка заполненности поля в случае заполненности выводим ничью
    for i in range(3):
        for j in range(3):
            if Game_field[i][j] == ' ':
                return False
    print_field()
    print('Игра закончилась ничьей')
    return True

def game_alg():
#основной алгоритм игры
    count = 0
    #инициализация счетчика определяющего очередность
    while True:
        count += 1
        print_field()
        if count % 2 == 0:
        # Четный Ход О, нечетный крестиков
            x, y = ask(count % 2)
            Game_field[x][y] = '0'
        else:
            x, y = ask(count % 2)
            Game_field[x][y] = 'X'
        if check_win(count % 2):
            break
            #сброс цикла игры в случае победы/ничьей

while True:
    Game_field = [[' ' for i in range(0, 3)] for j in range(0, 3)]
    # инициализация списка игрового поля
    if  input('Хотите сыграть?(Y/N)\n').upper() == 'Y':
        game_alg()
    else:
        break