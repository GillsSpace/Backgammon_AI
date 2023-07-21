import random, itertools, time, copy, arcade
from typing import Optional, Tuple

import Main_Files.Logic_v3 as Logic
import Main_Files.AI_v3 as AI
import Main_Files.Graphics_v3 as Graphics

import AI_Agents.TreeSearchI_v3 as TreeSearchI
import AI_Agents.Network_Type1_v3 as Network_Type1

#Testing Functions:
def printBoardInfo(Board:Logic.Board):
    print(f" - Board Info: - ")
    print(f"Positions = {Board.PositionListPoints} // Bar = {Board.PositionListBar} // Off = {Board.PositionListOff}")

def RunGame(AiType1,AiType2,PrintData=False,Silent=False):

    Board.setStartPositions()

    startingPlayer = random.randint(1,2)
    gameOver = False
    turnNumber = 1

    Turn = Logic.Turn(startingPlayer,"AI",None,First=True)
    if not Silent:
        Moves = AI.Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
    else:
        Moves = AI.Silent_Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
    Board.makeMoves(Moves,Turn.player)

    while not gameOver:

        Turn = Logic.Turn(1 if Turn.player == 2 else 2,"AI",None)
        turnNumber = turnNumber + 1
        if not Silent:
            Moves = AI.Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
        else:
            Moves = AI.Silent_Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
        Board.makeMoves(Moves,Turn.player)

        if Board.pip[1 if Turn.player == 2 else 0] == 0:
            gameOver = True
            winner = Turn.player
    
    if PrintData:
        print("/// Results ///")
        print(f"Winner = player {winner} // Number of Turns = {turnNumber}")
        print(f"Final Scores: {Board.pip[0]} to {Board.pip[1]}")
        print("///////////////")


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


##### Current Test Code #####

Board = Logic.Board()

# RunGames("Tree Search I","Tree Search I",1000) 
if __name__ == "__main__":
    RunGame("PBP","TS1",True,True)

# player = 1
# roll = (2,4)

# # Board = TreeSearchI.FastBoard()
# Board = Logic.Board()
# Board.setStartPositions()
# # Board.PositionListPoints = [[2,2,2,2,2,2,2],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[1,1,1,1,1,1]] #DEBUG

# game_settings = {"1P Inputs":"Generated","Sim Delay":5,"AI Lines":True,"Display AI Info":True,"AI Player":"Tree Search I"}  
# Turn = Logic.Turn(player,"AI",game_settings,False,roll)

# print(Board.PositionListPoints)

# fatsBoard = AI.from_Board_to_FastBoard(Board)
# # fastTurn = TreeSearchI.FastTurn(1,(2,2))
# print(fatsBoard.positions)

# # print("")
# # print("Sequence Generation:")
# # print(fatsBoard.returnMoveSequences(player,roll))

# # Moves = AI.Main(Board,Turn,"Tree Search I")
# # Board.updateWithMoves(Moves,player)
# # print(Board.PositionListPoints)

# # moves = TreeSearchI.Full_Run(fatsBoard,fastTurn)
# # print(moves)

# dieData = Board.calcMovesForDie(5,1,True,True)
# print(dieData)
# Turn.updatePossibleMoves(Board)
# TurnB = Logic.FullTurn(player,"Human",roll)
# print(Turn.current_possible_moves)
# TurnB.updatePossibleMovesHumanFormat(fatsBoard)
# print(TurnB.current_possible_moves)


# from multiprocessing import Pool, cpu_count
# import time

# def f(x):
#     y = x*x
#     return y

# if __name__ == '__main__':

#     st = time.time()

#     with Pool() as pool:      

#         print(pool.map(f, range(100)))     
#         print(f"Time = {time.time()-st}")

#     print("//Completed")
#     print(f"Time = {time.time()-st}")

    
#     pool_size = cpu_count()
#     pool = Pool(processes=pool_size,)
#     startTime1 = time.time()
#     pool_outputs = pool.map(f, range(5000000))
#     endTime1 = time.time() 
#     print(endTime1 - startTime1)
#     pool.close()
#     print(endTime1 - startTime1)
#     endTime1 = time.time()    
#     print(endTime1 - startTime1)
#     print(pool_outputs)