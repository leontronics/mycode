#!/usr/bin/env python3

import shutil
import os

def main():
    # Change the current working directory to "/home/student/mycode/"
    os.chdir('/home/student/mycode/')
    
    # Move the file "raynor.obj" to the "ceph_storage/" directory
    shutil.move('raynor.obj', 'ceph_storage/')
    
    # Prompt the user for a new name for "kerrigan.obj"
    xname = input('What is the new name for kerrigan.obj? ')
    
    # Move and rename the file "kerrigan.obj" based on the user's input
    shutil.move('ceph_storage/kerrigan.obj', 'ceph_storage/' + xname)

if __name__ == "__main__":
    main()
