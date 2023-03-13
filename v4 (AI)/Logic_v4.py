import random
import copy
from Graphics_v4 import createMoveStartSprites

def rollDice():
    num1 = random.randint(1,6)
    num2 = random.randint(1,6)
    return [num1,num2]

class Board:
    def __init__(self) -> None:
        self.PositionListPoints = [[]] * 15
        self.PositionListOff = [0,0]
        self.PositionListBar = []
        self.bearOffStatus = [False,False]
        self.pip = (0,0)
    def setStartPositions(self):
        self.PositionListPoints = [[1,1],[],[],[],[],[2,2,2,2,2],[],[2,2,2],[],[],[],[1,1,1,1,1],[2,2,2,2,2],[],[],[],[1,1,1],[],[1,1,1,1,1],[],[],[],[],[2,2]]
        self.PositionListOff = [0,0]
        self.PositionListBar = []
        self.bearOffStatus = [False,False]
        self.pip = (167, 167)
    def updatePip(self):
        darkPip = 0
        lightPip = 0
        for listNum in range(len(self.PositionListPoints)):
            list = self.PositionListPoints[listNum]
            listNum = listNum + 1
            if len(list) > 0:
                if list[0] == 1:
                    darkPip = darkPip + (len(list)*(25-listNum))
                if list[0] == 2:
                    lightPip = lightPip + (len(list)*listNum)
        for piece in self.PositionListBar:
            if piece == 1:
                darkPip = darkPip + 25
            if piece == 2:
                lightPip = lightPip + 25
        self.pip = (darkPip,lightPip)
    def findLastOccupiedPoint(self,player):
        if player == 1:
            for index in range(0,24,1):
                if len(self.PositionListPoints[index]) > 0 and self.PositionListPoints[index][0] == player:
                    return index + 1
        if player == 2:
            for index in range(23,-1,-1):
                if len(self.PositionListPoints[index]) > 0 and self.PositionListPoints[index][0] == player:
                    return index + 1
    def updateBearOffStatus(self):
        self.bearOffStatus[0] = True if self.findLastOccupiedPoint(1) > 18 else False
        self.bearOffStatus[1] = True if self.findLastOccupiedPoint(2) < 7 else False
    def updateWithMove(self,move,player):
        opponent = 1 if player == 2 else 2
        if move[0] == "bar":
            endPointIndex = move[1] - 1
            self.PositionListBar.remove(player)
            if len(self.PositionListPoints[endPointIndex]) > 0 and self.PositionListPoints[endPointIndex][0] == opponent:
                self.PositionListPoints[endPointIndex].remove(opponent)
                self.PositionListBar.append(opponent)
            self.PositionListPoints[endPointIndex].append(player)
        elif move[1] == "off":
            startPointIndex = move[0] - 1
            self.PositionListPoints[startPointIndex].remove(player)
            self.PositionListOff[player - 1] += 1 
            # above: [player -1] changes the player number to the respective list index
        else:
            endPointIndex = move[1] - 1
            startPointIndex = move[0] - 1
            self.PositionListPoints[startPointIndex].remove(player)
            if len(self.PositionListPoints[endPointIndex]) > 0 and self.PositionListPoints[endPointIndex][0] == opponent:
                self.PositionListPoints[endPointIndex].remove(opponent)
                self.PositionListBar.append(opponent)
            self.PositionListPoints[endPointIndex].append(player)
        self.updatePip()
    def calcMovesForDie(self,roll,player,isBiggestDie,secondMove):
        self.updateBearOffStatus()
        moveList = []
        def canMoveTo(point,player):
            if point > 24 or point < 1:
                return False
            pointList = self.PositionListPoints[point-1]
            opp = 1 if player == 2 else 2
            if len(pointList) == 0:
                return True
            if len(pointList) > 0 and pointList[0] == player:
                return True
            if len(pointList) == 1 and pointList[0] == opp:
                return True
        
        if player == 1:
            if 1 in self.PositionListBar:
                if canMoveTo(roll,1) == True:
                    moveList.append(("bar",[roll]))
            else:
                for point in range(24):
                    pointList = self.PositionListPoints[point]
                    if len(pointList) > 0 and pointList[0] == 1:
                        if canMoveTo(point+roll+1,1) == True:
                            moveList.append((point+1,[point+roll+1]))
                if self.bearOffStatus[0] == True:
                    if len(self.PositionListPoints[24-roll]) > 0 and self.PositionListPoints[24-roll][0] == 1:
                        moveList.append((25-roll,["off"]))
                    if (isBiggestDie == True or secondMove == True) and self.findLastOccupiedPoint(1) > 25-roll:
                        moveList.append((self.findLastOccupiedPoint(1),["off"]))

        if player == 2:
            if 2 in self.PositionListBar:
                if canMoveTo(25-roll,2) == True:
                    moveList.append(("bar",[25-roll]))
            else:
                for point in range(24):
                    pointList = self.PositionListPoints[point]
                    if len(pointList) > 0 and pointList[0] == 2:
                        if canMoveTo(point-roll+1,2) == True:
                            moveList.append((point+1,[point-roll+1]))
                if self.bearOffStatus[1] == True:
                    if len(self.PositionListPoints[roll-1]) > 0 and self.PositionListPoints[roll-1][0] == 2: 
                        moveList.append((roll,["off"]))
                    if (isBiggestDie == True or secondMove == True) and self.findLastOccupiedPoint(2) < roll:
                        moveList.append((self.findLastOccupiedPoint(2),["off"]))

        return moveList


class Turn:
    def __init__(self,player,playerType,settings,First=False,roll=None) -> None:
        self.roll = roll if roll != None else rollDice()
        self.doubles_turn = True if self.roll[0] == self.roll[1] else False
        self.unused_dice = []
        self.player = player
        self.player_type = playerType

        self.current_possible_moves = []

        self.sprites_move_start = []
        self.sprites_move_end = []
        self.sprite_active = []

        #prevents Doubles on first Roll
        if First == True and self.doubles_turn == True: 
            while (self.roll[0] == self.roll[1]) == True:
                self.roll = rollDice()
            self.doubles_turn = False

        #Sets up unused_dice
        if self.doubles_turn == True:
            self.unused_dice = [self.roll[0]] * 4
        else:
            self.unused_dice = copy.deepcopy(self.roll)
        
        print(f"New Turn Created // Roll = {self.roll} , Unused Dice = {self.unused_dice}") #DEBUG
    def updatePossibleMoves(self,Board):
        print("Running UpdatePossibleMoves") #Debug
        self.current_possible_moves = []
        if self.player_type == "Human":
            if self.doubles_turn == True and len(self.unused_dice) > 0:
                self.current_possible_moves = Board.calcMovesForDie(self.roll[0],self.player, True, True)
            else:
                biggerDie = self.roll[0] if self.roll[0] > self.roll[1] else self.roll[1]
                for roll in self.unused_dice:
                    self.current_possible_moves.append(Board.calcMovesForDie(roll,self.player,(roll == biggerDie),(len(self.unused_dice) == 1)))
                if len(self.unused_dice) > 1:
                    self.current_possible_moves = self.current_possible_moves[0] + self.current_possible_moves[1]
                    workingMovesList = self.current_possible_moves
                    self.current_possible_moves = []
                    startPoints = []
                    for move in workingMovesList:
                        startPoints.append(move[0]) 
                    for startPoint in startPoints:
                        numFin = []
                        for move in workingMovesList:
                            if startPoint == move[0]:
                                numFin.append(move[1][0])
                        finalList = ((startPoint),(numFin))
                        if finalList in self.current_possible_moves:
                            pass
                        else:
                            self.current_possible_moves.append(finalList)
                else:
                    self.current_possible_moves = self.current_possible_moves[0]
        if self.player_type == "AI":
            if self.doubles_turn == True:
                pass
    def formSpriteList(self,board):
        self.sprites_move_start = createMoveStartSprites(self.current_possible_moves,board,self.player)
        print(f"New Move Start Sprites Created with move list: {self.current_possible_moves}") #DEBUG
    def fromMoveToRoll(self,start,end,rolls,player):
        if start == "bar":
            roll = end if player == 1 else (25 - end)
        elif end == "off":
            roll = start if start in rolls else (25 - start)
        else:
            diff = end - start
            roll = diff if diff > 0 else (diff * -1)
        return roll



#Calculating Moves Logic

#For AI Turn Output => List of possible move combinations ex: [ ((1,3),(2,6)) , ((2,5),(5,9)) , ect.. ]
#   Format = [ ((move1),(move2)) , (moveCombination2) , ect ]
#For Human Turn Output => List of Possible first Moves ex: [ (1,[3,6]) , (2,[4,7]) , ect... ] 
#   Format = [ (startPoint,(endpoint1, endpoint2))]
#   Recalculated for second (possibly third and forth move)

#In Board => Calculate all moves for a particular dice
#In Turn ==> Calculate correct Lists for turn