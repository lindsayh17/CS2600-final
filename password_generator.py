"""
Generates a password that satisfies all the requirements.
The indices and characters are picked at random.
"""

import random

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
capitals = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*']
all_chars = nums + capitals + lowercase + special_chars

def add_char(password_list, char_list):
    """
    add a specified character to the password by choosing a random index
    if the index already has a character, it picks a new index
    :param password_list: the array with password characters in it
    :param char_list: the list of characters that will be drawn from
    """
    curr_index = random.randint(0, len(password_list) - 1)
    # loop until empty index is found
    while password_list[curr_index] != '':
        curr_index = random.randint(0, len(password_list) - 1)
    # set index to a random character
    password_list[curr_index] = str(random.choice(char_list))

def generate_password():
    """
    generate a password that satisfies the requirements:
    one number, one capital, one lowercase, one special char
    :return: the generated password
    """
    password_list = []
    # fill password list with 25 blank spaces
    for i in range(25):
        password_list.append('')

    # make sure the password has one of each required char
    add_char(password_list, nums)
    add_char(password_list, capitals)
    add_char(password_list, lowercase)
    add_char(password_list, special_chars)

    # fill in the remaining spaces
    for i in range(21):
        add_char(password_list, all_chars)

    # write characters from password list to a password string
    password = ''
    for i in range(len(password_list)):
        password += password_list[i]

    return password