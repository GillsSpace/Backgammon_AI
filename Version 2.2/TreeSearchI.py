import time
import random
import copy
import collections
from Logic_v2_2 import Board

#Data:
Data_rollOptions = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),(5,5),(5,6),(6,6)]

#Helper Functions:
def fromMoveToDie(start,end,roll,player):
    if start == 1001:
        die = end if player == 1 else (25 - end)
    elif end == 2002:
        die = start if start in roll else (25 - start)
        if die not in roll:
            die = max(roll)
    else:
        diff = end - start
        die = diff if diff > 0 else (diff * -1)
    return die
def average(inputList):
    return sum(inputList) / len(inputList)

#Classes:
class FastTurn:
    def __init__(self,player,roll) -> None:
        self.player = player
        self.roll = roll

class TurnSolution:
    def __init__(self, Board:Board, MoveSequence) -> None:
        self.Board = copy.deepcopy(Board)
        self.MoveSequence = MoveSequence
        self.expectedPipDiff = 0

class SubTurn:
    #Represents a possible turn of the opponent's
    def __init__(self, Board:Board, PrimaryMoveSequence, Roll, Player) -> None:
        self.Board = copy.deepcopy(Board)
        self.PrimaryMoveSequence = PrimaryMoveSequence
        self.Roll = Roll
        self.Player = Player
        self.largestPipDiff = 0 #represents the largest pip difference opponent can generate from the subTurn.

def ReturnTurnSolutions(inputBoard:Board,inputTurn:FastTurn):
    turnSolutions = []
    playerTurnSequences = inputBoard.returnMoveSequences(inputTurn.player,inputTurn.roll)
    for moveSequence in playerTurnSequences:
        instanceTurnSolution = TurnSolution(inputBoard,moveSequence)
        instanceTurnSolution.Board.makeMoves(moveSequence,inputTurn.player)
        turnSolutions.append(instanceTurnSolution)
    return turnSolutions

def PipMinMaxBasic(subTurn:SubTurn,player,Max=True): 
    #From an input of a SubTurn, returns either the maximum or minimum pip difference that can be generated in the courses of the subTurn

    pipList = []
    PossibleMovesList = subTurn.Board.returnMoveSequences(player,subTurn.Roll)

    for moves in PossibleMovesList:
        algoBoard = copy.deepcopy(subTurn.Board)
        algoBoard.makeMoves(moves,player)
        algoBoard.updatePip()
        pipDiff = (algoBoard.pip[1] - algoBoard.pip[0]) if player == 1 else (algoBoard.pip[0] - algoBoard.pip[1])
        pipList.append(pipDiff)
    
    if len(pipList) == 0:
        pipDiff = (subTurn.Board.pip[1] - subTurn.Board.pip[0]) if player == 1 else (subTurn.Board.pip[0] - subTurn.Board.pip[1])
        return pipDiff
    
    maxPipDiff = max(pipList)
    minPipDiff = min(pipList)

    if Max == True:
        return maxPipDiff
    else:
        return minPipDiff

#Running:
def Full_Run(inputBoard:Board,inputTurn:FastTurn):
    #Takes a input of a FastBoard and a FastTurn and returns the optimal move for the current player to make. 
    initialTurnSolutions = ReturnTurnSolutions(inputBoard,inputTurn)
    possiblePipDiffs = []
    for turnSolution in initialTurnSolutions:
        subTurnsList = []
        for roll in Data_rollOptions:
            instanceSubTurn = SubTurn(turnSolution.Board,turnSolution.MoveSequence,roll,(1 if inputTurn.player == 2 else 2))
            subTurnsList.append(instanceSubTurn)
        MaxPipDiffs = []
        for subTurn in subTurnsList:
            subTurn.largestPipDiff = PipMinMaxBasic(subTurn,subTurn.Player)
            MaxPipDiffs.append(subTurn.largestPipDiff)
            if subTurn.Roll[0] != subTurn.Roll[1]:
                #accounts fot weighted average of non-double rolls, appends the value twice:
                MaxPipDiffs.append(subTurn.largestPipDiff)
        turnSolution.expectedPipDiff = average(MaxPipDiffs)
        possiblePipDiffs.append(turnSolution.expectedPipDiff)

    if len(possiblePipDiffs) != 0:
        maxPipDiff = min(possiblePipDiffs)
        #Using min function because possible pip differences are calculated for opponents. 
        indexOfTurn = possiblePipDiffs.index(maxPipDiff)
        return initialTurnSolutions[indexOfTurn].MoveSequence 
    else:
        return [] 
