#!/usr/bin/python3
import requests
from dotenv import load_dotenv
import os

# Define NEOW URL
NEOURL = "https://api.nasa.gov/neo/rest/v1/feed?"

# Load environment variables from .env file
load_dotenv()

def get_api_key():
    """
    Retrieves NASA API key from environment variables.
    """
    return os.getenv('NASA_API_KEY')

def build_api_url(start_date, end_date=None):
    """
    Constructs the API URL with the given start date and optional end date.
    """
    api_key = get_api_key()
    url = f"{NEOURL}start_date={start_date}"
    if end_date:
        url += f"&end_date={end_date}"
    url += f"&api_key={api_key}"
    return url

def get_neo_data(api_url):
    """
    Makes a GET request to the NASA API and returns the data.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def main():
    """
    Main function to handle user input and display NEO data.
    """
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD) or press enter to skip: ")

    api_url = build_api_url(start_date, end_date)
    neo_data = get_neo_data(api_url)

    if neo_data:
        print(neo_data)

if __name__ == "__main__":
    main()
