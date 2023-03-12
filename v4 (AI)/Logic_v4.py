import random
import copy

def rollDice():
    num1 = random.randint(1,6)
    num2 = random.randint(1,6)
    return (num1,num2)

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
        self.takeOutStatus = [False,False]
        self.pip = [167,167]
    def updatePip(self):
        darkPip = 0
        lightPip = 0
        for listNum in range(len(self.PositionListPoints)):
            list = self.PositionListPoints[listNum]
            if len(list) > 0:
                if list[0] == 1:
                    darkPip = darkPip + (len(list)*(25-listNum))
                if list[0] == 2:
                    lightPip = lightPip + (len(list)*listNum)
            listNum = listNum + 1
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
    def calcMovesForDie(self,roll,player,isBiggestDie):
        self.updateBearOffStatus()
        moveList = []
        def canMoveTo(point,player):
            if point > 24 or point < 1:
                return False
            pointList = self.PositionListPoints[point-1]
            opp = 1 if player == 0 else 0
            if len(pointList) == 0:
                return True
            if len(pointList) > 0 and pointList[0] == player:
                return True
            if len(pointList) == 1 and pointList[0] == opp:
                return True
        
        if player == 1:
            if 1 in self.PositionListBar:
                if canMoveTo(roll,1) == True:
                    moveList.append(("hit",[roll]))
            else:
                for point in range(24):
                    pointList = self.PositionListPoints[point]
                    if len(pointList) > 0 and pointList[0] == 1:
                        if canMoveTo(point+roll+1,1) == True:
                            moveList.append((point+1,[point+roll+1]))
                if self.takeOutStatus[0] == True:
                    if len(self.PositionListPoints[24-roll]) > 0 and self.PositionListPoints[24-roll][0] == 1:
                        moveList.append((25-roll,["safe"]))
                    if isBiggestDie == True and self.findLastOccupiedPoint(1) > 25-roll:
                        moveList.append((self.findLastOccupiedPoint(1),["safe"]))

        if player == 0:
            if 0 in self.PositionListBar:
                if canMoveTo(25-roll,0) == True:
                    moveList.append(("hit",[25-roll]))
            else:
                for point in range(24):
                    pointList = self.PositionListPoints[point]
                    if len(pointList) > 0 and pointList[0] == 0:
                        if canMoveTo(point-roll+1,0) == True:
                            moveList.append((point+1,[point-roll+1]))
                if self.takeOutStatus[1] == True:
                    if len(self.PositionListPoints[roll-1]) > 0 and self.PositionListPoints[roll-1][0] == 0: 
                        moveList.append((roll,["safe"]))
                    if isBiggestDie == True and self.findLastOccupiedPoint(0) < roll:
                        moveList.append((self.findLastOccupiedPoint(0),["safe"]))

        return moveList


class Turn:
    def __init__(self,player,playerType,settings,First=False,roll=rollDice()) -> None:
        self.roll = roll
        self.doubles_turn = True if self.roll[0] == self.roll[1] else False
        self.unused_dice = []
        self.player = player
        self.player_type = playerType

        self.current_possible_moves = []

        self.sprites_move_start = []
        self.sprites_move_end = []
        self.sprite_active = []

        #prevents Doubles on first Roll
        if First == True and self.doublesTurn == True: 
            while self.roll[0] == self.roll[1]:
                self.roll = rollDice
            self.doublesTurn = False

        #Sets up availableRolls
        if self.doublesTurn == True:
            self.availableRolls = [self.roll[0]] * 4
        else:
            self.availableRolls = copy.deepcopy(self.roll)



#Calculating Moves Logic

#For AI Turn Output => List of possible move combinations ex: [ ((1,3),(2,6)) , ((2,5),(5,9)) , ect.. ]
#   Format = [ ((move1),(move2)) , (moveCombination2) , ect ]
#For Human Turn Output => List of Possible first Moves ex: [ (1,(3,6)) , (2(4,7)) , ect... ] 
#   Format = [ (startPoint,(endpoint1, endpoint2))]
#   Recalculated for second (possibly third and forth move)

#In Board => Calculate all moves for a particular dice
#In Turn ==> Calculate correct Lists for turn