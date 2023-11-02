#!/usr/bin/env python3
## create file object in "r"ead mode
filename = input("Please enter the name of file you wish to read: ")
with open(filename, "r") as configfile:
    ## readlines() creates a list by reading target
    ## file line by line
    configlist = configfile.readlines()

## file was just auto closed (no more indenting)

## each item of the list now has the "\n" characters back
print(configlist)
print("Number of lines in the file:", len(configlist)-1)
