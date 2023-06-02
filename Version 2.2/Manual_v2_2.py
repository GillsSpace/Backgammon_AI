import arcade
from typing import Optional, Tuple
import pyglet
import Logic_v2_2 as Logic
import AI_v2_2 as AI
import Graphics_v2_2 as Graphics
import TreeSearchI
import random, itertools, time, copy

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
    Board.makeMoves(Moves,Turn.player)

    while not gameOver:

        Turn = Logic.Turn(1 if Turn.player == 2 else 2,"AI",None)
        turnNumber = turnNumber + 1
        Moves = AI.Main(Board,Turn,AiType2 if Turn.player == 2 else AiType1)
        Board.makeMoves(Moves,Turn.player)

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

def RunVisualGame(AiType1,AiType2):

    Board.setStartPositions()
    startingPlayer = random.randint(1,2)

    class Game_Window(arcade.Window):
        def __init__(self):
            super().__init__(1200,800,"Backgammon")
            arcade.set_background_color(arcade.color.DARK_SCARLET)
            self.turnNumber = 1
            self.Turn = Logic.Turn(startingPlayer,"AI",None,First=True)
            self.Moves = AI.Main(Board,self.Turn,AiType2 if self.Turn.player == 2 else AiType1)
            Board.makeMoves(self.Moves,self.Turn.player,True)
            self.gameOver = False
            self.frame = 0

        def on_draw(self):
            Graphics.drawBoard()
            Graphics.drawPieces(Board.positions,Board.pip)
            Graphics.DrawMoveLines(Board.MoveLineData)
            if not self.gameOver and (self.frame%100 == 0):
                self.Turn = Logic.Turn(1 if self.Turn.player == 2 else 2,"AI",None)
                self.turnNumber = self.turnNumber + 1
                self.Moves = AI.Main(Board,self.Turn,AiType2 if self.Turn.player == 2 else AiType1)
                Board.makeMoves(self.Moves,self.Turn.player,True)

                Graphics.drawBoard()
                Graphics.drawPieces(Board.positions,Board.pip)
                Graphics.DrawMoveLines(Board.MoveLineData)

                if Board.pip[1 if self.Turn.player == 2 else 0] == 0:
                    winner = self.Turn.player
                    print(f"####Game Over: Number of Turns = {self.turnNumber}, Winner = {winner}")
                    arcade.exit()
    
    game = Game_Window()
    arcade.run()

def TestAIMoveUpdates(Board:Logic.Board,player,roll):
    Turn = Logic.Turn(player,"AI",None,roll=roll)
    Turn.updatePossibleMovesAI(Board,player)
    print(f"PossibleMoves = {Turn.current_possible_moves}")


##### Current Test Code #####

Board = Logic.Board()

RunGames("Tree Search I","Tree Search I",1000) 
# RunVisualGame("Tree Search I","Tree Search I")


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