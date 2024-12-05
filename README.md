# cs-2660-catamount-community-bank

Lindsay Hall

---
## Vulnerability
The original create_search_query method is vulnerable due to the "%{search_term}%" used in the like clause. An 
attacker can exploit this by adding a second clause within the those percent symbols. They would do so by 
finishing the first clause and closing the like statement, then adding another clause that can end with a 
'%"'. For example: 

    //well behaved user enters:
    VISA 
    //generates 
    SELECT * FROM trnsaction 
        WHERE trnsaction.account_id = 1234 
        AND 
        trnsaction.memo LIKE "%VISA%"

shows how the SQL statement would function if used responsibly. However, an attack could easily be perpetrated 
on this code:
    
    //misbehaved user enters:
    VISA%" OR "1" LIKE "%1
    //generates
    SELECT * FROM trnsaction 
        WHERE trnsaction.account_id = 1234 
        AND 
        trnsaction.memo LIKE "%VISA%" OR "1" LIKE "%1%"

As shown by the code above, a user can maintain proper format while creating a new sql statement by closing, 
then re-opening double quotes.

## Mitigating the Vulnerability
To mitigate this vulnerability, I used the find method for strings to look for a double quote character 
in the user's input. If a double quote was present, I set the string equal to null instead. This placeholder 
value works for the elements in the database at the moment, but might have to be readjusted if there was a 
larger or different database. The steps are as follows:

1. Look for a double quote in the user's inputted string and get the index
2. Check to see if a double quote was found (find method will return -1 as index if not)
3. If there was a double quote, set the sanitized string equal to null
4. If there is no double quote, set the sanitized string equal to the original

The following describes how one might rewrite the code to still run a search with the portion of the input 
that is valid.

If there was a double quote, I cut off any part of the input after that point, so they would only 
be able to enter the singular search term (VISA, for example). So, anything typed by the user will either 
be cut off my the program or included in the string being searched for, meaning it will have no impact on 
the functionality of the query. 

Steps: 

1. Look for a double quote in the user's inputted string and get the index
2. Check to see if a double quote was found (find method will return -1 as index if not)
3. If there was a double quote found, cut off the rest of the string, including that character
4. Set the santiized string variable equal to the sliced string (or the original if no quotes found)
5. Run the SQL statement with the santized string

## Source
Sqlite: https://docs.python.org/3/library/sqlite3.html
Sessions: https://flask.palletsprojects.com/en/stable/quickstart/#sessions
          https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
Django: https://www.w3schools.com/django/django_tags_if.php
Random Numbers: https://www.geeksforgeeks.org/random-numbers-in-python/
                https://www.w3schools.com/python/ref_random_randint.asp