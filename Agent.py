# ======================================================================
# FILE:        Agent.py
#
# AUTHOR:      Yuanke Zhang
#
# DESCRIPTION: This file contains the abstract agent class, which
#              details the interface for the user, and help to make action
#
# ======================================================================

from abc import ABCMeta, abstractmethod
#from enum import Enum


class Agent():
    # Actuators
    class Action():
        TURN_LEFT = 1
        TURN_RIGHT = 2
        FORWARD = 3
        SHOOT = 4
        GRAB = 5
        CLIMB = 6
        GoNorth = 7
        GoSouth = 8
        GoEast = 9
        GoWest = 10
        MOVE_UP = 11
        MOVE_DOWN = 12
        CHAT = 13

    @abstractmethod
    def getAction(self,

                  # Sensors
                  stench,
                  Sword,
                  glitter,
                  bump,
                  scream,
                  Solid
                  ):
        pass