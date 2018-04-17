import argparse
import re
import getpass
from dateparser.search import search_dates


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '-password_blacklist',
        help='enter path of a file containing password blacklist'
    )
    args = parser.parse_args()
    return args


def check_case_sensitivity(password):
    lower_letter = any(symbol.islower() for symbol in password)
    upper_letter = any(symbol.isupper() for symbol in password)
    case_sensitivity = lower_letter and upper_letter
    return case_sensitivity


def check_digits(password):
    if password.isdigit():
        return False
    digit_in_password = any(symbol.isdigit() for symbol in password)
    return digit_in_password


def check_special_characters(password):
    if re.search(r'\W', password):
        return True
    return False


def check_underlines_minuses_brackets(password):
    if re.search(r'[()_-]', password):
        return True
    return False


def check_password_length(password):
    improvement_by_password_length = 0
    password_length = len(password)
    if password_length >= 8:
        improvement_by_password_length += 1
    if password_length >= 12:
        improvement_by_password_length += 1
    return improvement_by_password_length


def check_common_numbers(password):
    if re.search(r'\d{4+}', password):
        return True
    return False


def check_date(password):
    if search_dates(password):
        return True
    return False


def check_password_blacklist(password, blacklist_file=None):
    if not blacklist_file:
        return False
    try:
        with open(blacklist_file, 'r', encoding='utf-8') as blacklist_file:
            blacklist = blacklist_file.read()
    except FileNotFoundError:
        return None
    if password in blacklist:
        return True
    return False


def check_good_features(password_points, password):
    if check_case_sensitivity(password):
        password_points += 2
    if check_digits(password):
        password_points += 2
    if check_special_characters(password):
        password_points += 2
    if check_underlines_minuses_brackets(password):
        password_points += 1
    password_points = password_points + check_password_length(password)
    return password_points


def check_bad_features(password_points, password, blacklist_path):
    if check_common_numbers(password):
        password_points -= 1
    if check_date(password):
        password_points -= 1
    password_in_blacklist = check_password_blacklist(password, blacklist_path)
    if password_in_blacklist is None:
        return None
    if password_in_blacklist:
        password_points -= 1
    return password_points


def get_password_strength(password, blacklist_path=None):
    password_strength = 1
    password_strength = check_good_features(password_strength, password)
    password_strength = check_bad_features(
        password_strength,
        password,
        blacklist_path
    )
    if password_strength < 1:
        password_strength = 1
    if password_strength > 10:
        password_strength = 10
    return password_strength


if __name__ == '__main__':
    console_arguments = get_console_arguments()
    password_blacklist_file = console_arguments.b
    user_password = getpass.getpass(prompt='Password: ')
    password_score = get_password_strength(
        user_password,
        password_blacklist_file
    )
    if password_score is None:
        print('Can not find the file containing a password blacklist.')
    else:
        print(
            'Your password gets {} point(s) out of 10.'.format(password_score)
        )
