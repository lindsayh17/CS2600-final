import random

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
capitals = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*']
all_chars = nums + capitals + lowercase + special_chars

def add_char(password_list, list_name):
    curr_index = random.randint(0, len(password_list) - 1)
    while password_list[curr_index] != '':
        curr_index = random.randint(0, len(password_list) - 1)
    password_list[curr_index] = str(random.choice(list_name))

def generate_password():
    password_list = []
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

    password = ''
    for i in range(len(password_list)):
        password += password_list[i]

    return password

print(generate_password())