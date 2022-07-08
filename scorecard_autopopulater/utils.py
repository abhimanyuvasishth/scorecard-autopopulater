from scorecard_autopopulater.constants import SheetOffsetCols, game1_col


def get_letters():
    return [letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']


def num_2_str(number):
    letters = get_letters()
    result = ""
    base = len(letters)

    while number:
        number -= 1
        result = letters[number % base] + result
        number //= base

    return result


def str_2_num(column):
    letters = get_letters()
    number = 0
    for i, char in enumerate(reversed(column)):
        number += (26 ** i) * (letters.index(char) + 1)
    return number


def get_game_col(game_number):
    game1_col_num = str_2_num(game1_col)
    col = game1_col_num + (game_number - 1) * len([v for v in SheetOffsetCols])
    return num_2_str(col)
