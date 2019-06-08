# =========================================================================
# File:                      Main.py
#
# Title:                     Multi User Dungeon
#
# Instruction:
#
# Author:                    Yuanke Zhang
#
# Description:               This file is the entry point for the program. The main
#                            function serves with couple purposes:
#                            (1) It is the interface with the command line
#                            (2) It will read a input map file, contains all the information needed
#                            (3) It will read user's each Move.
#                            (4) It is in charge of outputing information
#
# Notes:                     - Syntax :
#         
#
#                              Input File:
#                               InputFile: A path to a valid Mud World File,
#
#                              Input:
#                                User Input Movements: West, East, North, South, Up, Down
#
#===========================================================================

import sys
import os
import math
from World import World


def main():

    args = sys.argv


    # Important Variables
    # Example path: /Users/Yuank/PycharmProjects/MutileUserD/src/world4x4_2.txt
    worldFile = input("please input a valid wold test case path: \n")

    if worldFile == "":
        if worldFile == '':
            print ( "[WARNING] No file specified; running on a 4*4 world." )
        world = World ()
        Win = world.run()
        if Win:
            print("Thx for playing the game")
            exit()
    else:
        try:
            newLineDelim = "\n"
            if "\r\n".encode() in open(worldFile, "rb").read():
                newLineDelim = "\r\n"

            world = World(open(worldFile, 'rt', newline=newLineDelim))
            print()
            Win = world.run()
            if Win:
                print("Thx for playing the game")
                exit()

        except Exception:
            print("[ERROR] Failure to open file.")


main()

