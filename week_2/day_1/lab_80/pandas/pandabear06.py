#!/usr/bin/python3
"""Alta3 Research | RZFeeser@alta3.com
   Challenge Solution 01 - JSON to CSV"""

import pandas

def json_to_csv():

    # create a dataframe from json
    df = pandas.read_json("5movies.json")

    # writeout dataframe to CSV
    df.to_csv("5movies-translated-from-json.csv")


def csv_to_excel():

    # create a dataframe from csv
    df = pandas.read_csv("5movies.csv")

    # writeout dataframe to excel
    df.to_excel("5movies-translated-from-json.xlsx")


def json_to_excel():

    # create a dataframe from json
    df = pandas.read_json("5movies.json")

    # writeout dataframe to excel
    df.to_excel("5movies-translated-from-json.xlsx")


def main():
    json_to_csv()
    #csv_to_excel()
    #json_to_excel()

if __name__ == "__main__":
    main()
