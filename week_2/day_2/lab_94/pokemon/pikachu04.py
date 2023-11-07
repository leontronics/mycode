#!/usr/bin/python3

import argparse
import requests
import pandas as pd
import json

ITEMURL = "http://pokeapi.co/api/v2/item/"

def fetch_items(url):
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def filter_items(items, searchword):
    return [item['name'] for item in items if searchword in item['name']]

def export_data(matched_items, searchword):
    # Export to plaintext
    with open('pokemon_items.txt', 'w') as text_file:
        text_file.write('\n'.join(matched_items))

    # Export to JSON
    with open('pokemon_items.json', 'w') as json_file:
        json.dump({"matched_items": matched_items}, json_file)

    # Export to Excel with pandas
    items_df = pd.DataFrame({'matched_items': matched_items})
    items_df.to_excel("pokemon_items.xlsx", index=False)

    print(f"Data has been exported to plaintext, JSON, and Excel formats for the search word '{searchword}'.")

def main(args):
    items_data = fetch_items(f"{ITEMURL}?limit=1000")
    matched_items = filter_items(items_data.get("results", []), args.searchword)

    print(f"There are {len(matched_items)} items that contain the word '{args.searchword}' in the Pokemon Item API!")
    print(f"List of Pokemon items containing '{args.searchword}': {matched_items}")

    export_data(matched_items, args.searchword)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search the Pokemon item API for items containing a specific word.")
    parser.add_argument('--searchword', metavar='SEARCHW', type=str, default='ball', help="Word to search for in Pokemon items. Default is 'ball'.")
    args = parser.parse_args()
    main(args)
