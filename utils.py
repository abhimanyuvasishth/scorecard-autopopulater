from constants import game1_col, SheetOffsetCols

def safe_int(val):
    try:
        return int(val)
    except ValueError:
        return 0

def safe_float(val):
    try:
        return float(val)
    except ValueError:
        return 0.0

def get_letters():
    return [l for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

def number_to_letter(number):
    letters = get_letters()
    result = ""
    base = len(letters)

    while number:
        number -= 1
        result = letters[number % base] + result
        number //= base

    return result

def letter_to_number(column):
    letters = get_letters()
    number = 0
    for i, char in enumerate(reversed(column)):
        number += (26 ** i) * (letters.index(char) + 1)
    return number

def get_game_col(game_number):
    game1_col_num = letter_to_number(game1_col)
    col = game1_col_num + (game_number - 1) * len([v for v in SheetOffsetCols])
    return number_to_letter(col)
