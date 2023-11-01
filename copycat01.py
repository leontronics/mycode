#!/usr/bin/env python3

import shutil
import os

def main():
    # Change the current working directory to "/home/student/mycode/"
    os.chdir("/home/student/mycode/")

    # Copy the file "5g_research/sdn_network.txt" to "5g_research/sdn_network.txt.copy"
    shutil.copy("5g_research/sdn_network.txt", "5g_research/sdn_network.txt.copy")

    # Remove the directory "/home/student/mycode/5g_research_backup/" and its contents
    os.system("rm -rf /home/student/mycode/5g_research_backup/")
    
    # Copy the entire directory "5g_research/" to "5g_research_backup/"
    shutil.copytree("5g_research/", "5g_research_backup/")

if __name__ == "__main__":
    main()
