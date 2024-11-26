"""
Lab 1 - User Login and Access Levels
Lindsay Hall
CS2660 / Fall 2024

This program requires users to enter a username and password
to be given a list of options. They will then be given or
denied access based on the data in access.csv
"""


import csv
import sys


APPROVED = "1"
DENIED = "0"


def back_to_menu():
    """Gives the user the options to return to the menu
    by pressing zero or to exit the program entirely by
    typing quit.
    Returns the user's choice as a string."""
    choice = input("Press 0 to return to the menu or type \"quit\" " +
                   "to end the program: ")
    while choice.lower() != "quit" and choice != '0':
        choice = input("Invalid option. Press 0 or type \"quit\": ")
    if choice.lower() == "quit":
        sys.exit()
    return choice


def get_user_info():
    """ Prompts user to enter their username and password
    and validates the input. User will be prompted to try
    again if their username or password does not exist.
    Returns a string of the username"""
    # username
    print("Welcome to your portal.")
    username = input("Please enter your username or type \"quit\" to" +
                 " end program: ")
    while username not in user_passwords.keys():
        if username.lower() == "quit":
            sys.exit()
        print("\nUser does not exist")
        username = input("Please enter a valid username: ")

    # password
    password = input("Please enter your password: ")
    while password != user_passwords[username] and password.lower() != "exit":
        print("\nIncorrect Password")
        password = input("Please enter your password: ")
  
    return username


if __name__ == "__main__":

    user_passwords = {}
    options = []
    access = {}

    # get access data from CSV file
    try:
        with open('access.csv', 'r') as access_levels:
            reader = csv.reader(access_levels)
            for row in reader:
                access[row[0]] = row[1:len(row)]
        # remove the user header from the array
        options = access.pop('ï»¿User')
    except FileNotFoundError:
        print("Our system is down right now. Please try again later")
        sys.exit()

    # get user and password data
    try:
        with open('password.csv', 'r') as passwords:
            pass_reader = csv.reader(passwords)
            # skip header
            next(pass_reader)
            for row in pass_reader:
                user_passwords[row[0]] = row[1]
    except FileNotFoundError:
        print("Our system is down right now. Please try again later")
        sys.exit()

    user = get_user_info()

    user_choice = "0"
    while user_choice == "0":
        # display options
        counter = 1
        for option in options:
            print(f"\nPress {counter} for {option}.")
            counter += 1

        # ask user to choose options and ensure choice is within valid range
        user_choice = -1
        print("")
        while user_choice < 1 or user_choice > len(options):
            try:
                user_choice = int(input("Type number here: "))
                if user_choice < 1 or user_choice > len(options):
                    print("\nInvalid option.")
            except ValueError:
                print("\nInvalid input.")

        # accept or deny user access based on data
        if access[user][user_choice - 1] == APPROVED:
            print(f"\nYou have now accessed the {options[user_choice - 1]}" +
                  " application.")
            user_choice = back_to_menu()
        elif access[user][user_choice - 1] == DENIED:
            print(f"\nYou are not authorized the {options[user_choice - 1]}" +
                  " application.")
            user_choice = back_to_menu()
        else:
            print("There has been an error in our system. " +
                  "Please contact your supervisor.")
