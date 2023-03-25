import Logic_v2_1 as Logic
import AI_v2_1 as AI
import random
import itertools
import time

def byGroup(k):
    k = sorted(sorted(x) for x in k)
    return [k for k,_ in itertools.groupby(k)]


#Testing Functions:
def printBoardInfo(Board:Logic.Board):
    print(f" - Board Info: - ")
    print(f"Positions = {Board.PositionListPoints} // Bar = {Board.PositionListBar} // Off = {Board.PositionListOff}")

def RunGame(AiType1,AiType2):

    Board.setStartPositions()

    print(" --- New Game --- ")
    startingPlayer = random.randint(1,2)
    gameOver = False
    turnNumber = 1

    printBoardInfo(Board)

    Turn = Logic.Turn(startingPlayer,"AI",None,First=True)
    Moves = AI.Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
    Board.updateWithMoves(Moves,Turn.player)

    printBoardInfo(Board)

    while not gameOver:

        print(" ----- New Turn -----")

        Turn = Logic.Turn(1 if Turn.player == 2 else 2,"AI",None)
        turnNumber = turnNumber + 1
        Turn.updatePossibleMoves(Board)
        Moves = AI.Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
        Board.updateWithMoves(Moves,Turn.player)

        print(Board.PositionListPoints)
        # printBoardInfo(Board)

        if Board.pip[1 if Turn.player == 2 else 0] == 0:
            gameOver = True
            winner = Turn.player

        print(" ----- Turn Over -----")

    print(" --- Game Over ---")
    print(f"Turn Number = {turnNumber}")

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
        print(f"game number = {i}")
        i = i + 1
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
Board = Logic.Board()
Board.setStartPositions()

# Board.PositionListPoints = [[],[],[],[],[],[2,2,2,2,2],[],[],[],[],[],[],[],[],[],[],[],[],[1,1,1,1,1],[],[],[],[],[]] 
# TestAIMoveUpdates(Board,1,(4,2))

# RunGames("Random","PBP",10)
# RunGames("Random","Random",1000)
RunGame("PBP","PBP")

#Notes: 