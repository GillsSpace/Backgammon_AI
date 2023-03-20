import Logic_v2_1 as Logic
import AI_v2_1 as AI
import random

Board = Logic.Board()

def printBoardInfo(Board:Logic.Board):
    print(f" - Board Info: - ")
    print(f"Positions = {Board.PositionListPoints} // Bar = {Board.PositionListBar} // Off = {Board.PositionListOff}")

Board.setStartPositions()

def RunGame():

    print(" --- New Game --- ")
    startingPlayer = random.randint(1,2)
    gameOver = False

    printBoardInfo(Board)

    Turn = Logic.Turn(startingPlayer,"AI",None,First=True)
    Turn.updatePossibleMoves(Board)
    Moves = AI.Main(Board,Turn)
    Board.updateWithMoves(Moves,2)

    printBoardInfo(Board)

    while not gameOver:

        Turn = Logic.Turn(1 if Turn.player == 2 else 1,"AI",None)
        Turn.updatePossibleMoves(Board)
        Moves = AI.Main(Board,Turn)
        Board.updateWithMoves(Moves,2)

        printBoardInfo(Board)

        if Board.pip[1 if Turn.player == 2 else 0] == 0:
            gameOver = True

    print(" --- Game Over ---")

    RunGame()