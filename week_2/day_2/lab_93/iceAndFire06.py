#!/usr/bin/python3
# documentation for this API is at
# https://anapioficeandfire.com/Documentation

import requests

AOIF_CHAR = "https://www.anapioficeandfire.com/api/characters/"

# check on the names of data passed
def name_finder(got_list):
    names = []  # list to return back of decoded names
    for x in got_list:
        # send HTTP GET to one of the entries within the list
        r = requests.get(x)
        decodedjson = r.json()  # decode the JSON on the response
        names.append(decodedjson.get("name", "Unknown"))  # this returns the housename and adds it to our list
    return names

def main():
    # Ask user for input
    got_charToLookup = input("Pick a number between 1 and 1000 to return info on a GoT character! ")

    # Send HTTPS GET to the API of ICE and Fire character resource
    gotresp = requests.get(AOIF_CHAR + got_charToLookup)

    # Decode the response
    got_dj = gotresp.json()

    # Get the character's name or their first alias if the name is not available or is an empty string
    character_name = got_dj.get("name") if got_dj.get("name") else (got_dj.get("aliases")[0] if got_dj.get("aliases") else "Unknown")

    # Ensure that we don't print an empty string for the name
    if not character_name.strip():
        character_name = "Unknown"

    print(f"\nCharacter Information:")
    print(f"Name/Alias: {character_name}")

    # Print the names of the houses the character is allegiant to
    allegiances = name_finder(got_dj.get("allegiances", []))
    if allegiances:
        print("\nAllegiances:")
        for house in allegiances:
            print(house)
    else:
        print("\nAllegiances: None")

    # Print the names of the books the character appears in
    books = name_finder(got_dj.get("books", []))
    if books:
        print("\nBooks:")
        for book in books:
            print(book)
    else:
        print("\nBooks: None")

if __name__ == "__main__":
    main()
