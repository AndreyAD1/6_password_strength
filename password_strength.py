import argparse
import re
import getpass
from dateutil import parser


def get_console_arguments():
    console_parser = argparse.ArgumentParser()
    console_parser.add_argument(
        '-b',
        '-password_blacklist',
        default=None,
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
    return bool(re.search(r'\W', password))


def check_underlines_minuses_brackets(password):
    return bool(re.search(r'[()_-]', password))


def check_password_length(password):
    improvement_by_password_length = 0
    password_length = len(password)
    reliable_password_length = 8
    very_reliable_password_length = 12
    if password_length >= reliable_password_length:
        improvement_by_password_length += 1
    if password_length >= very_reliable_password_length:
        improvement_by_password_length += 1
    return improvement_by_password_length


def check_common_numbers(password):
    return bool(re.search(r'\d{4+}', password))


def check_date(password):
    try:
        data = parser.parse(password)
        return bool(data)
    except ValueError:
        return False


def check_password_blacklist(password, blacklist):
    if not blacklist:
        return False
    return password in blacklist


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


def check_bad_features(password_points, password, blacklist):
    if check_common_numbers(password):
        password_points -= 1
    if check_date(password):
        password_points -= 1
    password_in_blacklist = check_password_blacklist(password, blacklist)
    if password_in_blacklist:
        password_points -= 1
    return password_points


def get_password_strength(password, blacklist):
    password_strength = 1
    password_strength = check_good_features(password_strength, password)
    password_strength = check_bad_features(
        password_strength,
        password,
        blacklist
    )
    max_score = 10
    min_score = 1
    password_strength = max(min_score, min(max_score, password_strength))
    return password_strength


def get_password_blacklist(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as blacklist_file:
            blacklist = blacklist_file.read()
        return blacklist
    except FileNotFoundError:
        blacklist = None
        return blacklist


if __name__ == '__main__':
    console_arguments = get_console_arguments()
    password_blacklist_file = console_arguments.b
    password_blacklist = None
    if password_blacklist_file:
        password_blacklist = get_password_blacklist(password_blacklist_file)
        if password_blacklist is None:
            print(
                'Can not find the file containing a password blacklist. '
                'The script will not check the password in a blacklist.'
            )
    user_password = getpass.getpass(prompt='Password: ')
    password_score = get_password_strength(
        user_password,
        password_blacklist
    )
    print('Your password gets {} point(s) out of 10.'.format(password_score))
