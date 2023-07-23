import random
import copy
from Main_Files.Logic_v3 import Board,Turn
import time

from AI_Agents.TreeSearchI_v3 import Full_Run as TreeSearchI_Full_Run
from AI_Agents.Network_Type1_v3 import Full_Run as Network_Type1_Full_Run
from AI_Agents.Pick_Best_Pip_v3 import Full_Run as PBP_Full_Run

#Helper Classes:


#AI Types:
def randomMove(ActiveBoard:Board, ActiveTurn:Turn):
    ActiveTurn.updatePossibleMovesStandardFormat(ActiveBoard)
    if ActiveTurn.current_possible_moves != []:
        Moves = random.choice(ActiveTurn.current_possible_moves)
        return Moves
    else:
        return []

def pickBestPip(ActiveBoard:Board, ActiveTurn:Turn):
    return PBP_Full_Run(ActiveBoard,ActiveTurn)

def treeSearchI(ActiveBoard:Board, ActiveTurn:Turn):
    return TreeSearchI_Full_Run(ActiveBoard,ActiveTurn)

#Main Function - Called 
def Main(Main_Board:Board,Main_Turn:Turn,aiType,networkIdent=None):
    AI_player = aiType
    if AI_player == "Random":
        print(f"Running Random Move Selection; Roll = {Main_Turn.roll}")
        st = time.time()
        Moves = randomMove(Main_Board,Main_Turn)
        et = time.time()
        print(f"Finished Run; Elapsed Time = {et-st}; Final Move Set = {Moves}")
        return Moves
    elif AI_player in ["Tree Search I","TS 1"]:
        print(f"Running Tree Search I; Roll = {Main_Turn.roll}")
        st = time.time()
        Moves = treeSearchI(Main_Board,Main_Turn)
        et = time.time()
        print(f"Finished Run; Elapsed Time = {et-st}; Final Move Set = {Moves}")
        return Moves
    elif AI_player == "PBP":
        print(f"Running PBP; Roll = {Main_Turn.roll}")
        st = time.time()
        Moves = pickBestPip(Main_Board,Main_Turn)
        et = time.time()
        print(f"Finished Run; Elapsed Time = {et-st}; Final Move Set = {Moves}")
        return Moves
    elif AI_player == "Network_Type1":
        pass

def Silent_Main(Main_Board:Board,Main_Turn:Turn,aiType,networkIdent=None):
    AI_player = aiType
    if AI_player == "Random":
        Moves = randomMove(Main_Board,Main_Turn)
        return Moves
    elif AI_player in ["Tree Search I","TS 1"]:
        Moves = treeSearchI(Main_Board,Main_Turn)
        return Moves
    elif AI_player == "PBP":
        Moves = pickBestPip(Main_Board,Main_Turn)
        return Moves
    elif AI_player == "Network_Type1":
        pass