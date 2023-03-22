import Logic_v2_1 as Logic
import AI_v2_1 as AI
import random
import itertools

def byGroup(k):
    k = sorted(sorted(x) for x in k)
    return [k for k,_ in itertools.groupby(k)]


#Testing Functions:
def printBoardInfo(Board:Logic.Board):
    print(f" - Board Info: - ")
    print(f"Positions = {Board.PositionListPoints} // Bar = {Board.PositionListBar} // Off = {Board.PositionListOff}")

def RunGame():

    Board.setStartPositions()

    print(" --- New Game --- ")
    startingPlayer = random.randint(1,2)
    gameOver = False
    turnNumber = 0

    printBoardInfo(Board)

    Turn = Logic.Turn(startingPlayer,"AI",None,First=True)
    turnNumber = turnNumber + 1
    Turn.updatePossibleMoves(Board)
    Moves = AI.Main(Board,Turn,"Random")
    Board.updateWithMoves(Moves,Turn.player)

    printBoardInfo(Board)

    while not gameOver:

        Turn = Logic.Turn(1 if Turn.player == 2 else 2,"AI",None)
        turnNumber = turnNumber + 1
        Turn.updatePossibleMoves(Board)
        Moves = AI.Main(Board,Turn,"Random")
        Board.updateWithMoves(Moves,Turn.player)

        printBoardInfo(Board)

        if Board.pip[1 if Turn.player == 2 else 0] == 0:
            gameOver = True

    print(" --- Game Over ---")
    print(f"Turn Number = {turnNumber}")

    return turnNumber

def RunGames():
    i = 0
    turns = []
    while i < 1000:
        turnNum = RunGame()
        turns.append(turnNum)
        print(f"game number = {i}")
        i = i + 1
    average = sum(turns) / len(turns)
    print(f"Turns: Max = {max(turns)} // Average = {average} // Min = {min(turns)}")

def TestAIMoveUpdates(Board:Logic.Board,player,roll):
    Turn = Logic.Turn(player,"AI",None,roll=roll)
    Turn.updatePossibleMovesAI(Board,player)
    print(f"PossibleMoves = {Turn.current_possible_moves}")


#Current Test Code
Board = Logic.Board()
Board.setStartPositions()
Board.PositionListPoints = [[],[],[],[],[],[2,2,2,2,2],[],[],[],[],[],[],[],[],[],[],[],[],[1,1,1,1,1],[],[],[],[],[]] 
TestAIMoveUpdates(Board,1,(4,2))


