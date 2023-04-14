import random
import copy
from Logic_v2_1 import Board,Turn
import TreeSearchI

#Conversions:
def from_Board_to_FastBoard(Board:Board):
    positionList = []
    for point in Board.PositionListPoints:
        if len(point) == 0:
            positionList.append(0)
        if len(point) > 0 and point[0] == 1:
            positionList.append(-1 * len(point))
        if len(point) > 0 and point[0] == 2:
            positionList.append(len(point))
    player1 = 0
    player2 = 0
    for item in Board.PositionListBar:
        if item == 1:
            player1 = player1 + 1
        else:
            player2 = player2 + 1
    positionList.append(player1)
    positionList.append(player2)
    positionList.append(Board.PositionListOff[0])
    positionList.append(Board.PositionListOff[1])
    New_Board = TreeSearchI.FastBoard(positionList)
    return New_Board


#AI Types:
def randomMove(ActiveBoard:Board, ActiveTurn:Turn):
    algoBoard = copy.deepcopy(ActiveBoard)

    #First Move
    ActiveTurn.updatePossibleMoves(algoBoard)
    possibleMoves = ActiveTurn.current_possible_moves
    if len(possibleMoves) == 0:
        return ()
    else:
        Move1 = random.choice(possibleMoves)
        Move1 = (Move1[0], random.choice(Move1[1]))
        roll = ActiveTurn.fromMoveToRoll(Move1[0],Move1[1],ActiveTurn.unused_dice,ActiveTurn.player)
        ActiveTurn.unused_dice.remove(roll)
        algoBoard.updateWithMove(Move1,ActiveTurn.player)
        if algoBoard.pip[ActiveTurn.player - 1] == 0:
            return [Move1]

    ActiveTurn.updatePossibleMoves(algoBoard)
    possibleMoves = ActiveTurn.current_possible_moves
    if len(possibleMoves) == 0:
        return [Move1]
    else:
        Move2 = random.choice(possibleMoves)
        Move2 = (Move2[0], random.choice(Move2[1]))
        roll = ActiveTurn.fromMoveToRoll(Move2[0],Move2[1],ActiveTurn.unused_dice,ActiveTurn.player)
        ActiveTurn.unused_dice.remove(roll)
        algoBoard.updateWithMove(Move2,ActiveTurn.player)
        if algoBoard.pip[ActiveTurn.player - 1] == 0:
            return(Move1,Move2)

    if ActiveTurn.doubles_turn == True:
        ActiveTurn.updatePossibleMoves(algoBoard)
        possibleMoves = ActiveTurn.current_possible_moves
        if len(possibleMoves) == 0:
            return (Move1,Move2)
        else:
            Move3 = random.choice(possibleMoves)
            Move3 = (Move3[0], random.choice(Move3[1]))
            roll = ActiveTurn.fromMoveToRoll(Move3[0],Move3[1],ActiveTurn.unused_dice,ActiveTurn.player)
            ActiveTurn.unused_dice.remove(roll)
            algoBoard.updateWithMove(Move3,ActiveTurn.player)
            if algoBoard.pip[ActiveTurn.player - 1] == 0:
                return (Move1,Move2,Move3)

        ActiveTurn.updatePossibleMoves(algoBoard)
        possibleMoves = ActiveTurn.current_possible_moves
        if len(possibleMoves) == 0:
            return (Move1,Move2,Move3)
        else:
            Move4 = random.choice(possibleMoves)
            Move4 = (Move4[0], random.choice(Move4[1]))
            roll = ActiveTurn.fromMoveToRoll(Move4[0],Move4[1],ActiveTurn.unused_dice,ActiveTurn.player)
            ActiveTurn.unused_dice.remove(roll)

        return (Move1,Move2,Move3,Move4)
    else:
        return (Move1,Move2)

def pickBestPip(ActiveBoard:Board, ActiveTurn:Turn):
    pipsList = []
    ActiveTurn.updatePossibleMovesAI(ActiveBoard,ActiveTurn.player)

    for Moves in ActiveTurn.current_possible_moves:
        algoBoard = copy.deepcopy(ActiveBoard)
        algoBoard.updateWithMoves(Moves,ActiveTurn.player)
        algoBoard.updatePip()
        pipDiff = (algoBoard.pip[1] - algoBoard.pip[0]) if ActiveTurn.player == 1 else (algoBoard.pip[0] - algoBoard.pip[1])
        pipsList.append(pipDiff)

    if len(pipsList) == 0:
        return []

    maxPipDiff = max(pipsList)
    indexOfMove = pipsList.index(maxPipDiff)

    return ActiveTurn.current_possible_moves[indexOfMove]

def treeSearchI(ActiveBoard:Board, ActiveTurn:Turn):
    fastBoard = from_Board_to_FastBoard(ActiveBoard)
    fastTurn = TreeSearchI.FastTurn(ActiveTurn.player,ActiveTurn.roll)

    return TreeSearchI.Full_Run(fastBoard,fastTurn)

#Main Function - Called 
def Main(Main_Board:Board,Main_Turn:Turn,aiType):
    AI_player = aiType
    if AI_player == "Random":
        Moves = randomMove(Main_Board,Main_Turn)
        return Moves
    elif AI_player == "Tree Search I":
        Moves = treeSearchI(Main_Board,Main_Turn)
        return Moves
    elif AI_player == "DRL":
        pass
    elif AI_player == "PBP":
        Moves = pickBestPip(Main_Board,Main_Turn)
        return Moves