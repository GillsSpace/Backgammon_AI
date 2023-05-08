import Logic_v2_1 as Logic
import AI_v2_1 as AI
import TreeSearchI
import random
import itertools
import time
import copy

#Testing Functions:
def printBoardInfo(Board:Logic.Board):
    print(f" - Board Info: - ")
    print(f"Positions = {Board.PositionListPoints} // Bar = {Board.PositionListBar} // Off = {Board.PositionListOff}")

def RunGame(AiType1,AiType2):

    Board.setStartPositions()

    startingPlayer = random.randint(1,2)
    gameOver = False
    turnNumber = 1

    Turn = Logic.Turn(startingPlayer,"AI",None,First=True)
    Moves = AI.Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
    Board.updateWithMoves(Moves,Turn.player)

    while not gameOver:

        Turn = Logic.Turn(1 if Turn.player == 2 else 2,"AI",None)
        turnNumber = turnNumber + 1
        Turn.updatePossibleMoves(Board)
        Moves = AI.Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
        Board.updateWithMoves(Moves,Turn.player)

        if Board.pip[1 if Turn.player == 2 else 0] == 0:
            gameOver = True
            winner = Turn.player


    return turnNumber, winner

def RunGames(AiType1,AiType2,iterations):
    i = 0
    turns = []
    wins = [0,0]

    st = time.time()
    while i < iterations:
        turnNum, winner = RunGame(AiType1,AiType2)
        turns.append(turnNum)
        wins[winner - 1] = wins[winner - 1] + 1
        i = i + 1
        print(f" Game Number = {i}  // winner = {winner} // Number of Turns = {turnNum}")
    et = time.time()

    elapsed_time = et - st

    print("##### Games Stats #####")
    average = sum(turns) / len(turns)
    print(f"Games Played = {iterations} // Elapsed Time = {elapsed_time}")
    print(f"Turns: Max = {max(turns)} // Average = {average} // Min = {min(turns)}")
    print(f"Player 1 Wins = {wins[0]} // Player 2 Wins = {wins[1]}")

def TestAIMoveUpdates(Board:Logic.Board,player,roll):
    Turn = Logic.Turn(player,"AI",None,roll=roll)
    Turn.updatePossibleMovesAI(Board,player)
    print(f"PossibleMoves = {Turn.current_possible_moves}")


#Current Test Code
# Board = TreeSearchI.FastBoard()
Board = Logic.Board()
Board.setStartPositions()
Board.PositionListPoints = [[2],[2,2,2,2],[2,2,2],[],[],[2,2,2,2,2,2],[],[],[],[2],[],[],[],[],[],[],[],[],[],[],[1,1],[1,1,1,1],[],[1,1,1,1,1,1]] #DEBUG

print(Board.PositionListPoints)

fatsBoard = AI.from_Board_to_FastBoard(Board)
fastTurn = TreeSearchI.FastTurn(1,(2,2))

print(fatsBoard.returnMoveSequences(1,(2,2)))

# moves = TreeSearchI.Full_Run(fatsBoard,fastTurn)
# print(moves)

