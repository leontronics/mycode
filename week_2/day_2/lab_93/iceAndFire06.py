#!/usr/bin/python3
# Documentation for this API is at https://anapioficeandfire.com/Documentation

import requests

AOIF_CHAR = "https://www.anapioficeandfire.com/api/characters/"

# Function to fetch data from a given URL
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  
    return response.json() 

# Function to get the character's name or their first alias if the name is not available
def get_character_name_or_alias(character_data):
    return character_data.get("name") or (character_data.get("aliases")[0] if character_data.get("aliases") else "Unknown")

# Function to get names from a list of URLs (used for fetching names of books and houses)
def get_names_from_urls(url_list):
    names = []  
    for url in url_list:
        try:
            data = fetch_data(url) 
            names.append(data.get("name", "Unknown"))  
        except requests.HTTPError:
            names.append("Unknown")  
    return names

# Function to print a list of items with a title
def print_list(title, items):
    if items:
        print(f"\n{title}:")
        for item in items:
            print(f"  {item}") 
    else:
        print(f"\n{title}: None") 

def main():
    got_char_to_lookup = input("Pick a number between 1 and 1000 to return info on a GoT character! ")

    try:
        character_data = fetch_data(AOIF_CHAR + got_char_to_lookup)  
        character_name = get_character_name_or_alias(character_data).strip() or "Unknown"  

        print(f"\nCharacter Information:\nName/Alias: {character_name}")

        allegiances = get_names_from_urls(character_data.get("allegiances", [])) 
        print_list("Allegiances", allegiances)  

        # Combines 'books' and 'povBooks' lists and fetches their names
        book_urls = character_data.get("books", []) + character_data.get("povBooks", [])
        books = get_names_from_urls(book_urls)  
        print_list("Books", books) 

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
    except Exception as err:
        print(f"An error occurred: {err}")  

if __name__ == "__main__":
    main()
