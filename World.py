# =========================================================================
# File:                      World.py
#
# Title:                     Multi User Dungeon World
#
# Instruction:              In real game
#                           you should only be able to see the Room you current in, so that
#                           the 3x3 room is what you will see in real game. Starting Locatin
#                           should be random, but (0,0) for now for Test convience.
#
#
# Author:                    Yuanke Zhang
#
# Description:               This file is the Contain the world class, which is
#                            responsible for take the input and generate the world
#                            you can see the world before you get into it, After you
#                            have been placed in one Room, you can not see anything
#                            except your Room. But you Can Share information with
#                            Other User by chat with them.
#
#                            I tried to make the player only can see his own room
#                            Find the Monster and kill it to get out there.
#                            There is one Misery Item May help you, go find it.
#
# Notes:                     None
#
#===========================================================================

import random
from Agent import Agent
from UserControl import UserControl
import time
import socket
import threading
import json


class World():

    class __Tile:
        Monster = False;
        Sword = False;#bumb
        OtherUser = False;
        stench = False;
        transparent = False;
        getitem = False;
        Solid = False;

    # ==========================================================
    # = Constructor
    # ==========================================================

    def __init__(self,  file = None):
        # Operation Flags
        # Agent Initialization
        self.__SwordLooted = False
        self.__bump = False
        self.blood = 100
        self.__agentDir = 0
        self.__agentX = 0       #can be random or input
        self.__agentY = 0       #can be random or input
        self.MonsterKilled = False
        self.MonsterBlood = 5000
        self.user_count = 0
        self.Solid = False
        self.UserName = ''
        self.ServerName = ''
        self.inString = ''
        self.outString = ''
        self.Stop = True


        if file != None:
            self.__colDimension, self.__rowDimension = [int(x) for x in next(file).split()]
            print("The Maximun Row for the world is :", self.__rowDimension,
                  "\nAnd the Maximun Col for the world is: ", self.__colDimension)

            self.__board = [[self.__Tile() for j in range(self.__rowDimension)] for i in range(self.__colDimension)]
            self.__addFeatures(file)
        else:
            self.__colDimension = 4
            self.__rowDimension = 4
            self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
            self.__addFeatures()


        self.__agent = UserControl()


    # ===============================================================
    # =                 Engine Function
    # ===============================================================

    def run(self):

        #self.__printWorldInfo()  Real Game place here
        self.UserName = input("Please Input a user name you want to use In this Game: Ex YuankeZ \n")

        while(self.MonsterKilled != True):

            # To seprate the console input to chat and command
            if self.Stop == True:

                # Print World at each step for test convience
                self.__printWorldInfo()


                # Print Current Room Information
                self.__printRoomInfo()

                # Print Player Information

                self.__printUserInfo()

                # Get the move
                self.__lastAction = self.__agent.getAction(
                    self.__board[self.__agentX][self.__agentY].stench,
                    self.__board[self.__agentX][self.__agentY].Sword,
                    self.__bump,
                    self.__board[self.__agentX][self.__agentY].Solid
                )

                self.__bump = False;

                #chat
                if self.__lastAction == Agent.Action.CHAT:
                    self.Starttochat()
                if self.__lastAction == Agent.Action.TURN_LEFT:
                    self.__agentDir -= 1
                    if (self.__agentDir < 0):
                        self.__agentDir = 3

                elif self.__lastAction == Agent.Action.TURN_RIGHT:
                    self.__agentDir += 1
                    if self.__agentDir > 3:
                        self.__agentDir = 0

                elif self.__lastAction == Agent.Action.FORWARD:
                    if self.__agentDir == 0 and self.__agentX + 1 < self.__colDimension and self.__board[self.__agentX+1][self.__agentY].Solid == False:
                        self.__agentX += 1
                    elif self.__agentDir == 1 and self.__agentY - 1 >= 0 and self.__board[self.__agentX][self.__agentY-1].Solid == False:
                        self.__agentY -= 1
                    elif self.__agentDir == 2 and self.__agentX - 1 >= 0 and  self.__board[self.__agentX-1][self.__agentY].Solid == False:
                        self.__agentX -= 1
                    elif self.__agentDir == 3 and self.__agentY + 1 < self.__rowDimension  and self.__board[self.__agentX][self.__agentY+1].Solid == False:
                        self.__agentY += 1
                    else:
                        print(" The room you try to reach may be solid or not exit.")
                        self.__bump = True
                        print(" The room you try to reach may be solid or not exit.")

                    if self.__board[self.__agentX][self.__agentY].Monster:
                        fight = self.Meet_monster()
                        if fight == True:
                            if self.__SwordLooted == False:
                                time.sleep(1)
                                print("You hit Monster with your face! Monster feels Sweat lool")
                                self.blood = self.blood - 50
                                self.MonsterBlood = self.MonsterBlood - 5
                                time.sleep(1)
                                print("Your HP: ", self.blood, "Monster HP: ", self.MonsterBlood)
                                fight = self.Meet_monster()
                                if fight == True:
                                    self.blood = 0
                                    print("You have been killed. HP = ", self.blood)
                                    time.sleep(1)
                                    return "Game Over"
                                else:
                                    pass
                            else:
                                print("Monster: How dare you challange me!!")
                                time.sleep(1)
                                print("You: What a punny Monster")
                                time.sleep(1)
                                print("killed with Monster with one hit. ")
                                self.MonsterKilled = True
                                return self.MonsterKilled
                        if fight == False:
                            pass


                elif self.__lastAction == Agent.Action.GRAB:
                    if self.__board[self.__agentX][self.__agentY].Sword:
                        self.__board[self.__agentX][self.__agentY].Sword = False
                        self.__SwordLooted = True
                        time.sleep(1)
                        print(self.UserName, " Got an Legenary Weapon")
                    else:
                        time.sleep(1)
                        print("There is nothing to pickup ")


    # ===============================================================
    # =             World Generation Functions
    # ===============================================================

    def __addFeatures(self, file=None):
        if file == None:
            # Generate Monster
            wc = self.__randomInt(self.__colDimension)
            wr = self.__randomInt(self.__rowDimension)

            while wc == 0 and wr == 0:
                wc = self.__randomInt(self.__colDimension)
                wr = self.__randomInt(self.__rowDimension)

            self.__addMonster(wc, wr);

            # Generate Sword
            gc = self.__randomInt(self.__colDimension)#item
            gr = self.__randomInt(self.__rowDimension)#item

            while gc == 0 and gr == 0:
                gc = self.__randomInt(self.__colDimension)
                gr = self.__randomInt(self.__rowDimension)

            self.__addSword(gc, gr)


        else:
            # Add the Monster
            c, r = [int(x) for x in next(file).split()]
            self.__addMonster(c, r)

            # Add the Sword
            cS, rS = [int(x) for x in next(file).split()]
            self.__addSword(cS, rS)

            # Add Solid Room
            for i in range(int(self.__randomInt(self.__colDimension * self.__rowDimension)/2)):
                cSolid = self.__randomInt(self.__colDimension - 1)
                rSolid = self.__randomInt(self.__rowDimension - 1)
                if cSolid != cS and rSolid != rS or cSolid != c and rSolid != r or rSolid != 0 and cSolid != 0:
                    self.__addSold(cSolid, rSolid)

            file.close()


    def __addMonster(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].Monster = True
            self.__addStench(c + 1, r)
            self.__addStench(c - 1, r)
            self.__addStench(c, r + 1)
            self.__addStench(c, r - 1)

    def __addSword(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].Sword = True

    def __addSold(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].Solid = True

    def __addStench(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].stench = True

    def __isInBounds(self, c, r):
        return c < self.__colDimension and r < self.__rowDimension and c >= 0 and r >= 0

    # ===============================================================
    # =             World Printing Functions
    # ===============================================================

    def __printWorldInfo(self):
        self.__printBoardInfo()


    def __printBoardInfo(self):
        for r in range(self.__rowDimension - 1, -1, -1):
            for c in range(self.__colDimension):
                self.__printTileInfo(c, r)
            print("")
            print("")

    def __printTileInfo(self, c, r):
        tileString = ""

        if self.__board[c][r].Monster: tileString += "W"
        if self.__board[c][r].Sword:   tileString += "?"
        if self.__board[c][r].stench: tileString += "S"
        if self.__board[c][r].Solid: tileString += "X" #solid room not able to go through
        if self.__agentX == c and self.__agentY == r:
            tileString += "@"


        tileString += "."

        print(tileString.rjust(8), end="")
    def __printCurrentRoom(self, c, r):
        for row in range(3, -1 , -1):
            for col in range(3):
                if row == 1 and col == 1:
                    self.__printFog(True,c,r)
                else:
                    self.__printFog(False,col,row)
            print("")
            print("")

    def __printFog(self, bool, c, r):
        fogstring = ""
        if bool == True:

            if self.__board[c][r].Monster: fogstring += "W"
            if self.__board[c][r].Sword:   fogstring += "?"
            if self.__board[c][r].stench: fogstring += "S"
            if self.__board[c][r].Solid: fogstring += "X"

            if self.__agentX == c and self.__agentY == r:
                fogstring += "@"

            fogstring += "."
        else:
            fogstring += "~"
        print(fogstring.rjust(8), end="")

    def __printUserInfo(self):
        print("Blood: " + str(self.blood))
        print("Items: " + str(self.__SwordLooted))
        self.__printDirectionInfo()
        self.__printPerceptInfo()

    def __printDirectionInfo(self):
        if self.__agentDir == 0:
            print("AgentDir: Right")

        elif self.__agentDir == 1:
            print("AgentDir: Down")

        elif self.__agentDir == 2:
            print("AgentDir: Left")

        elif self.__agentDir == 3:
            print("AgentDir: Up")

        else:
            print("AgentDir: Invalid")

    def __printActionInfo(self):
        if self.__lastAction == Agent.Action.TURN_LEFT:
            print("Last Action: Turned Left")

        elif self.__lastAction == Agent.Action.TURN_RIGHT:
            print("Last Action: Turned Right")

        elif self.__lastAction == Agent.Action.FORWARD:
            print("Last Action: Moved Forward")


        elif self.__lastAction == Agent.Action.USESWORD:
            print("Last Action: Used the Sowrd")

        elif self.__lastAction == Agent.Action.PickItem:
            print("Last Action: Pick up Items")


        else:
            print("Last Action: Invalid")

    def __printPerceptInfo(self):
        perceptString = "Percepts: "

        if self.__board[self.__agentX][self.__agentY].stench: perceptString += "Stench, "
        if self.__board[self.__agentX][self.__agentY].Sword:   perceptString += "Glitter, "
        if self.__bump:                         perceptString += "Bump, "

        if perceptString[-1] == ' ' and perceptString[-2] == ',':
            perceptString = perceptString[:-2]

        print(perceptString)
    def __printRoomInfo(self):
        print("Now your Room is: ", [self.__agentX, self.__agentY])
        print("There are 1: ", self.user_count, "In the room")
        self.__printCurrentRoom(self.__agentX, self.__agentY)

        pass


    # ===============================================================
    # =                 Helper Functions
    # ===============================================================

    def __randomInt(self, limit):
        return random.randrange(limit)




    def Starttochat(self):
        self.Stop = False
        self.ServerName = '127.0.0.1'

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ServerName, 1111))
        sock.send(self.UserName.encode())

        thin = threading.Thread(target= self.DealIn, args=(sock,))
        thin.start()

        thout = threading.Thread(target=self.DealOut, args=(sock,))
        thout.start()


    def DealIn(self, sock):
        while True:
            try:
                self.inString = sock.recv(1024)
                if not self.inString:
                    break
                if self.outString != self.inString.decode():
                    print(self.inString.decode())

            except:
                break
    def DealOut(self, sock):
        while True:
            self.outString = input()
            if self.outString == 'exit':
                self.Stop = True
            # if self.outString == 'eixt':
            #     self.Stop = True
            #     #threading.Event()
            #     break
            self.outString = self.UserName + ':' + self.outString
            sock.send(self.outString.encode())

    # ================================================================
    # =               Room Setting Function
    # ================================================================

    def Meet_monster(self):
        while(1):
            if self.blood == 100:
                Death_Move = input("Monster!!!! Do You want to fight ?  y/n")

                if Death_Move == 'y' or Death_Move == 'yes' or Death_Move == 'y':
                    return True
                elif Death_Move == 'N' or Death_Move == 'No' or Death_Move == 'n':
                    return False
                else:
                    print("Input is not correct! Please try again! ")
            else:
                Death_Move = input("Monster: Human you still want to fight me?? ")
                if Death_Move == 'y' or Death_Move == 'yes' or Death_Move == 'y':
                    return True
                elif Death_Move == 'N' or Death_Move == 'No' or Death_Move == 'n':
                    return False
                else:
                    print("Input is not correct! Please try again! ")

