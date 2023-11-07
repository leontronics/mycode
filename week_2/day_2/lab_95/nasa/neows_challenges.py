#!/usr/bin/python3
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

NASA_API_KEY = os.getenv('NASA_API_KEY')
NEO_FEED_URL = 'https://api.nasa.gov/neo/rest/v1/feed?'


def get_asteroid_data(start_date, end_date):
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': NASA_API_KEY
    }
    response = requests.get(NEO_FEED_URL, params=params)
    response.raise_for_status()
    return response.json()


def find_extreme_asteroids(asteroid_data):
    largest = {'name': '', 'diameter': 0}
    fastest = {'name': '', 'speed': 0}
    closest = {'name': '', 'distance': float('inf')}

    for daily_asteroids in asteroid_data.values():
        for asteroid in daily_asteroids:
            diameter = asteroid['estimated_diameter']['meters']['estimated_diameter_max']
            speed = float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])
            distance = float(asteroid['close_approach_data'][0]['miss_distance']['kilometers'])

            if diameter > largest['diameter']:
                largest.update({'name': asteroid['name'], 'diameter': diameter})
            if speed > fastest['speed']:
                fastest.update({'name': asteroid['name'], 'speed': speed})
            if distance < closest['distance']:
                closest.update({'name': asteroid['name'], 'distance': distance})

    return largest, fastest, closest


def main():
    try:
        start_date = input('Enter the start date (YYYY-MM-DD): ')
        end_date = input('Enter the end date (YYYY-MM-DD) or press enter to skip: ') or start_date

        asteroid_data = get_asteroid_data(start_date, end_date)['near_earth_objects']
        largest, fastest, closest = find_extreme_asteroids(asteroid_data)

        print(f'The largest asteroid is {largest["name"]} with a diameter of {largest["diameter"]} meters.')
        print(f'The fastest asteroid is {fastest["name"]} with a speed of {fastest["speed"]} kilometers per hour.')
        print(f'The closest asteroid is {closest["name"]} with a distance of {closest["distance"]} kilometers.')
    except requests.RequestException as e:
        print(f'Error fetching data from NASA API: {e}')
    except ValueError as e:
        print(f'Invalid date format: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


if __name__ == '__main__':
    main()
