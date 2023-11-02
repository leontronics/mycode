#!/usr/bin/python3

# parse keystone.common.wsgi and return number of failed login attempts
loginfail = 0 # counter for fails
successful_post = 0

# open the file for reading
with open("/home/student/mycode/attemptlogin/keystone.common.wsgi") as kfile:

    # loop over the file
    for line in kfile:
        # if this 'fail pattern' appears in the line...
        if "- - - - -] Authorization failed" in line:
            loginfail += 1 # this is the same as loginfail = loginfail + 1
            print("Authorization failed - IP Address: " + line.split(" ")[-1])

        elif "POST" in line:
            successful_post += 1 

print("The number of failed log in attempts is", loginfail)
print("\nThe number of successful POST is", successful_post)

