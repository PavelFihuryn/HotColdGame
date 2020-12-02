# cold-hot
import random
import os

max_guess = 10
num_digits = 3


def clear():
    """
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. Useful for managing
    menu screens in terminal applications.
    """
    os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')

    print('A bunch of garbage so we can garble up the screen...')
    clear()


# Same effect, less characters...


def clear():
    """
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. Useful for managing
    menu screens in terminal applications.
    """
    os.system('cls||echo -e \\\\033c')


def say_rules(num_digits, max_guess):
    return print(f"Я загадаю {num_digits}-х значное чило, которое вы должны отгадать.\n"
                 "Я дам несколько подсказок...\n\n"
                 "Когда я говорю:      Это означает:\n\n"
                 "Холодно              Ни одна цифра не отгадана\n"
                 "Тепло                Одна цифра отгадана, но не отгадана позиция\n"
                 "Горячо               Одна цифра и ее позиция отгаданы\n\n"
                 "Помните: цифры в числе могут повторяться!\n"
                 "Итак, я загадал число.\n\n"
                 f"У Вас есть {max_guess} попыток, чтобы его отгадать")


def get_secret_number(num_digits):
    str_num = []
    count = 0
    while count < num_digits:
        numbers = '1 2 3 4 5 6 7 8 9 0'.split()
        random.shuffle(numbers)
        if numbers[0] not in str_num:
            if numbers[0] == '0' and len(str_num) == 0:
                continue
            else:
                str_num.append(numbers[0])
        else:
            continue
        count += 1
    return ''.join(str_num)


def count_attempts(num):
    count = 0
    while count <= num:
        count += 1
        yield count


def make_player_number(num, num_digits):
    print(f'Попытка №{next(num)}')
    while True:
        try:
            value = input()
            if len(value) == num_digits and value.isdigit():
                return value
            print(f'Вводить необходимо {num_digits}-значное число! Попробуйте еще раз:', end=' ')
            continue
        except ValueError:
            print(f'Необходимо ввесли {num_digits}-значное число! Попробуйте еще раз:', end=' ')


def is_number(num_comp: str, num_pl: str) -> str:
    res = []
    for i in range(len(num_pl)):
        if num_comp[i] == num_pl[i]:
            res.append('Горячо')
        elif num_comp[i] in num_pl:
            res.append('Тепло')
    if len(res) == 0:
        res.append('Холодно')
    res.sort()
    return ' '.join(res)


if __name__ == '__main__':
    while True:
        say_rules(num_digits, max_guess)
        val = count_attempts(max_guess)
        counter = 0
        number = get_secret_number(num_digits)
        while counter < max_guess:
            player_number = make_player_number(val, num_digits)
            result = is_number(number, player_number)
            print(result)
            print('\n')
            if player_number == number:
                print(f"Вы победили. Загаданное число действительно: {number}")
                break
            counter += 1
        else:
            print(f"Жаль, но Вы проиграли. Загаданное число было: {number}")
        if input('\n\nХотите сыграть еще раз (Да/Нет?)  ') not in 'yes y да д'.lower().split():
            break
        else:
            clear()
            print('Напомню правила\n\n')
