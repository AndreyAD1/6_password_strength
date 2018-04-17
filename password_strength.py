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


def check_all_digits(password):
    all_digits = password.isdigit()
    return all_digits


def check_case_sensitivity(password):
    # if check_all_digits(password):
    #     return False
    # case_sensitivity = not(password.islower() or password.isupper())
    # print(case_sensitivity)
    lower_letter = any(letter.islower() for letter in password)


    return True


def check_digits(password):
    if check_all_digits(password):
        return False
    if re.search(r'\d', password):
        return True
    return False


def check_special_characters(password):
    if re.search(r'\W', password):
        return True
    # \s - whitespace


def check_password_blacklist(password, blacklist_file=None):
    if not blacklist_file:
        return
    with open(blacklist_file, 'r', encoding='utf-8') as blacklist_file:
        blacklist = blacklist_file.read()
    if password in blacklist:
        return False
    return True


def check_common_numbers(password):
    if re.search(r'\d{4+}', password):
        return False
    return True


def check_password_length(password):
    improvement_by_password_length = 0
    password_length = len(password)
    if password_length >= 8:
        improvement_by_password_length += 1
    if password_length >= 12:
        improvement_by_password_length += 2
    return improvement_by_password_length


def check_underlines_minuses_brackets(password):
    if re.search(r'[()_-]', password):
        return True
    return False


def check_date(password):
    print(search_dates(password))
    if not search_dates(password):
        return True
    return False


def get_password_strength(password, blacklist_path = None):
    password_strength = 1
    if check_case_sensitivity(password):
        password_strength += 1
    if check_digits(password):
        password_strength += 1
    if check_special_characters(password):
        password_strength += 1
    if check_password_blacklist(password, blacklist_path):
        password_strength += 1
    if check_common_numbers(password):
        password_strength += 1
    if check_underlines_minuses_brackets(password):
        password_strength += 1
    if check_date(password):
        password_strength += 1
    password_strength = password_strength + check_password_length(password)
    return password_strength


if __name__ == '__main__':
    console_arguments = get_console_arguments()
    password_blacklist_file = console_arguments.b
    # user_password = console_arguments.password
    user_password = getpass.getpass(prompt='Password: ')
    password_score = get_password_strength(user_password, password_blacklist_file)
    print('Your password get {} points out of 10.'.format(password_score))
