# ======================================================================
# FILE:        UserControl.py
#
# AUTHOR:      Yuanke Zhang
#
# DESCRIPTION: This file contains the communication between the program
#              and the User The UserScontrol will return a move at every
#              turn of the game, with only one exception. If the User kill
#              the Monster or Blood below than 0 perceives glitter
#
#
# NOTES:       - Don't make changes to this file.
# ======================================================================

from Agent import Agent
import random




class UserControl(Agent):#inherence from Agent Class

    def getAction(self, stench, glitter, bump, scream):
        # Print Command Menu
        print("Press 'f' to Move Forward  'a' to 'Turn Left' 'd' to 'Turn Right'")
        print("'g' to 'Grab'  'say to talk with other' ")

        # Get Input
        userInput = input('Please input: ').strip()
        while not userInput:
            userInput = input().strip()

        # Return Action Associated with Input
        if userInput == 'say':
            return Agent.Action.CHAT

        if userInput == 'f':
            return Agent.Action.FORWARD

        if userInput == 'a':
            return Agent.Action.TURN_LEFT

        if userInput == 'd':
            return Agent.Action.TURN_RIGHT
        if userInput == 'N':
            return Agent.Action.GoNorth

        if userInput == 'S':
            return Agent.Action.GoSouth

        if userInput == 'W':
            return Agent.Action.GoWest
        if userInput == 'E':
            return Agent.Action.GoEast

        if userInput == 's':
            return Agent.Action.USESWORD

        if userInput == 'g':
            return Agent.Action.GRAB

            pass
