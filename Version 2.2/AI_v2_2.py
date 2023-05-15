import random
import copy
from Logic_v2_2 import Board,Turn
import TreeSearchI
import time

#AI Types:
def randomMove(ActiveBoard:Board, ActiveTurn:Turn):
    ActiveTurn.updatePossibleMovesStandardFormat(ActiveBoard)
    if ActiveTurn.current_possible_moves != []:
        Moves = random.choice(ActiveTurn.current_possible_moves)
        return Moves
    else:
        return []

def pickBestPip(ActiveBoard:Board, ActiveTurn:Turn):
    pipsList = []
    ActiveTurn.updatePossibleMovesStandardFormat(ActiveBoard)

    for Moves in ActiveTurn.current_possible_moves:
        algoBoard = copy.deepcopy(ActiveBoard)
        algoBoard.makeMoves(Moves,ActiveTurn.player)
        algoBoard.updatePip()
        pipDiff = (algoBoard.pip[1] - algoBoard.pip[0]) if ActiveTurn.player == 1 else (algoBoard.pip[0] - algoBoard.pip[1])
        pipsList.append(pipDiff)

    if len(pipsList) == 0:
        return []

    maxPipDiff = max(pipsList)
    indexOfMove = pipsList.index(maxPipDiff)

    return ActiveTurn.current_possible_moves[indexOfMove]

def treeSearchI(ActiveBoard:Board, ActiveTurn:Turn):
    fastTurn = TreeSearchI.FastTurn(ActiveTurn.player,ActiveTurn.roll)
    return TreeSearchI.Full_Run(ActiveBoard,fastTurn)

#Main Function - Called 
def Main(Main_Board:Board,Main_Turn:Turn,aiType):
    AI_player = aiType
    if AI_player == "Random":
        Moves = randomMove(Main_Board,Main_Turn)
        return Moves
    elif AI_player == "Tree Search I":
        print(f"Running Tree Search I; Roll = {Main_Turn.roll}")
        st = time.time()
        Moves = treeSearchI(Main_Board,Main_Turn)
        et = time.time()
        print(f"Finished Run; Elapsed Time = {et-st}; Final Move Set = {Moves}")
        return Moves
    elif AI_player == "DRL":
        pass
    elif AI_player == "PBP":
        Moves = pickBestPip(Main_Board,Main_Turn)
        return Moves