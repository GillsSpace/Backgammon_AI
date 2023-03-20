import random
import copy
from Logic_v2_1 import Board,Turn

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
        print(Move1) #DEBUG
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

def Main(Main_Board:Board,Main_Turn:Turn):
    AI_player = Main_Turn.settings["AI Player"]
    if AI_player == "Random":
        Moves = randomMove(Main_Board,Main_Turn)
        print(f"Final Move list = {Moves}") #DEBUG
        return Moves
    elif AI_player == "Tree":
        pass
    elif AI_player == "DRL":
        pass