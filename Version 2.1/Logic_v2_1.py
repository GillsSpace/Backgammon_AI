import random
import copy
from Graphics_v2_1 import createMoveStartSprites, GenerateMoveLineData
import collections

def rollDice():
    num1 = random.randint(1,6)
    num2 = random.randint(1,6)
    return [num1,num2]

def byDict(k):
    s = collections.OrderedDict()
    for i in k:
        s[tuple(sorted(i))] = i
    return list(s.values())

class Board:
    def __init__(self) -> None:
        self.PositionListPoints = [[]] * 24
        self.PositionListOff = [0,0]
        self.PositionListBar = []
        self.bearOffStatus = [False,False]
        self.pip = (0,0)
        self.lastPoints = [0,0]
    def setStartPositions(self):
        self.PositionListPoints = [[1,1],[],[],[],[],[2,2,2,2,2],[],[2,2,2],[],[],[],[1,1,1,1,1],[2,2,2,2,2],[],[],[],[1,1,1],[],[1,1,1,1,1],[],[],[],[],[2,2]]
        # self.PositionListPoints = [[],[],[],[],[],[2,2,2,2,2],[],[],[],[],[],[],[],[],[],[],[],[],[1,1,1,1,1],[],[],[],[],[]] #DEBUG
        self.PositionListOff = [0,0]
        self.PositionListBar = []
        self.bearOffStatus = [False,False]
        self.lastPoints = [1,24]
        self.pip = (167, 167)
        self.TurnNumber = 0
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
    def updateLastOccupiedPoint(self,player):
        if player == 1:
            for index in range(0,24,1):
                if len(self.PositionListPoints[index]) > 0 and self.PositionListPoints[index][0] == player:
                    self.lastPoints[0] = index + 1
                    return
        if player == 2:
            for index in range(23,-1,-1):
                if len(self.PositionListPoints[index]) > 0 and self.PositionListPoints[index][0] == player:
                    self.lastPoints[1] = index + 1
                    return
    def updateBearOffStatus(self):
        self.bearOffStatus[0] = True if self.lastPoints[0] > 18 else False
        self.bearOffStatus[1] = True if self.lastPoints[1] < 7 else False
    def updateWithMove(self,move,player):
        opponent = 1 if player == 2 else 2
        if move[0] == 1001:
            endPointIndex = move[1] - 1
            self.PositionListBar.remove(player)
            if len(self.PositionListPoints[endPointIndex]) > 0 and self.PositionListPoints[endPointIndex][0] == opponent:
                self.PositionListPoints[endPointIndex].remove(opponent)
                self.PositionListBar.append(opponent)
            self.PositionListPoints[endPointIndex].append(player)
        elif move[1] == 2002:
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
        self.updateLastOccupiedPoint(player)
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
                    moveList.append((1001,[roll]))
            else:
                for point in range(24):
                    pointList = self.PositionListPoints[point]
                    if len(pointList) > 0 and pointList[0] == 1:
                        if canMoveTo(point+roll+1,1) == True:
                            moveList.append((point+1,[point+roll+1]))
                if self.bearOffStatus[0] == True:
                    if len(self.PositionListPoints[24-roll]) > 0 and self.PositionListPoints[24-roll][0] == 1:
                        moveList.append((25-roll,[2002]))
                    if (isBiggestDie == True or secondMove == True) and self.lastPoints[0] > 25-roll:
                        moveList.append((self.lastPoints[0],[2002]))

        if player == 2:
            if 2 in self.PositionListBar:
                if canMoveTo(25-roll,2) == True:
                    moveList.append((1001,[25-roll]))
            else:
                for point in range(24):
                    pointList = self.PositionListPoints[point]
                    if len(pointList) > 0 and pointList[0] == 2:
                        if canMoveTo(point-roll+1,2) == True:
                            moveList.append((point+1,[point-roll+1]))
                if self.bearOffStatus[1] == True:
                    if len(self.PositionListPoints[roll-1]) > 0 and self.PositionListPoints[roll-1][0] == 2: 
                        moveList.append((roll,[2002]))
                    if (isBiggestDie == True or secondMove == True) and self.lastPoints[1] < roll:
                        moveList.append((self.lastPoints[1],[2002]))

        return moveList
    def updateWithMoves(self,moves,player,final=False):
        moveData = []
        if len(moves) > 0 and type(moves[0]) == int:
            self.updateWithMove(moves,player)
        else:
            for move in moves:
                self.updateWithMove(move,player)
                if final == True:
                    data = GenerateMoveLineData(move,self)
                    moveData.append(data)
        self.moveData = moveData

class Turn:
    def __init__(self,player,playerType,settings,First=False,roll=None) -> None:
        self.roll = roll if roll != None else rollDice()
        self.doubles_turn = True if self.roll[0] == self.roll[1] else False
        self.unused_dice = []
        self.player = player
        self.player_type = playerType
        self.settings = settings

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
        
        # print(f"New Turn Created // player = {self.player} // Roll = {self.roll} , Unused Dice = {self.unused_dice}") #DEBUG
    def updatePossibleMoves(self,Board):
        self.current_possible_moves = []
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
    def updatePossibleMovesAI(self,Board:Board,player=None):
        player = self.player if player == None else player
        self.current_possible_moves = []
        if self.doubles_turn == False:
            biggerDie = self.roll[0] if self.roll[0] >= self.roll[1] else self.roll[1]
            FirstMoves = []
            for roll in self.unused_dice: #All Possible First Moves
                FirstMoves.append(Board.calcMovesForDie(roll,player,(roll == biggerDie),False))
            FirstMoves = FirstMoves[0] + FirstMoves[1]
            for move in FirstMoves:
                algoBoard1 = copy.deepcopy(Board)
                algoBoard1.updateWithMove((move[0],move[1][0]),player)
                if algoBoard1.pip[player - 1] == 0:
                    self.current_possible_moves = [(move[0],move[1][0])]
                    return 
                usedRoll = self.fromMoveToRoll(move[0],move[1][0],self.roll,player)
                secondMoves = algoBoard1.calcMovesForDie((self.roll[0] if self.roll[1] == usedRoll else self.roll[1]),player,True,True)
                if len(secondMoves) == 0:
                    self.current_possible_moves = [(FirstMoves[0][0],FirstMoves[0][1][0])]
                    return
                for secondMove in secondMoves:
                    self.current_possible_moves.append(((move[0],move[1][0]),(secondMove[0],secondMove[1][0])))
            self.current_possible_moves = list(set(self.current_possible_moves))
            self.current_possible_moves = byDict(self.current_possible_moves)
        else:
            FirstMoves = Board.calcMovesForDie(self.roll[0],player,True,True)
            for move in FirstMoves:
                algoBoard1 = copy.deepcopy(Board)
                algoBoard1.updateWithMove((move[0],move[1][0]),player)
                if algoBoard1.pip[player - 1] == 0:
                    self.current_possible_moves = [(move[0],move[1][0])]
                    return
                secondMoves = algoBoard1.calcMovesForDie(self.roll[0],player,True,True)
                for secondMove in secondMoves:
                    algoBoard2 = copy.deepcopy(Board)
                    algoBoard2.updateWithMoves(((move[0],move[1][0]),(secondMove[0],secondMove[1][0])),player)
                    if algoBoard2.pip[player - 1] == 0:
                        self.current_possible_moves = [((move[0],move[1][0]),(secondMove[0],secondMove[1][0]))]
                        return 
                    thirdMoves = algoBoard2.calcMovesForDie(self.roll[0],player,True,True)
                    for thirdMove in thirdMoves:
                        algoBoard3 = copy.deepcopy(Board)
                        algoBoard3.updateWithMoves(((move[0],move[1][0]),(secondMove[0],secondMove[1][0]),(thirdMove[0],thirdMove[1][0])),player)
                        if algoBoard3.pip[player - 1] == 0:
                            self.current_possible_moves = [((move[0],move[1][0]),(secondMove[0],secondMove[1][0]),(thirdMove[0],thirdMove[1][0]))]
                            return 
                        forthMoves = algoBoard3.calcMovesForDie(self.roll[0],player,True,True)
                        for forthMove in forthMoves:
                            self.current_possible_moves.append(((move[0],move[1][0]),(secondMove[0],secondMove[1][0]),(thirdMove[0],thirdMove[1][0]),(forthMove[0],forthMove[1][0])))
            self.current_possible_moves = list(set(self.current_possible_moves))
            self.current_possible_moves = byDict(self.current_possible_moves)
    def formSpriteList(self,board):
        self.sprites_move_start = createMoveStartSprites(self.current_possible_moves,board,self.player)
    def fromMoveToRoll(self,start,end,rolls,player):
        if start == 1001:
            roll = end if player == 1 else (25 - end)
        elif end == 2002:
            roll = start if start in rolls else (25 - start)
            if roll not in rolls:
                roll = max(rolls)
        else:
            diff = end - start
            roll = diff if diff > 0 else (diff * -1)
        return roll
    def updateTurnSettings(self,settings):
        self.settings = settings


#Calculating Moves Logic

#For AI Turn Output => List of possible move combinations ex: [ ((1,3),(2,6)) , ((2,5),(5,9)) , ect.. ]
#   Format = [ ((move1),(move2)) , (moveCombination2) , ect ]
#For Human Turn Output => List of Possible first Moves ex: [ (1,[3,6]) , (2,[4,7]) , ect... ] 
#   Format = [ (startPoint,(endpoint1, endpoint2))]
#   Recalculated for second (possibly third and forth move)

#In Board => Calculate all moves for a particular dice
#In Turn ==> Calculate correct Lists for turn