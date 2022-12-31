import random

#Helper Functions
def RollDice():
    num1 = random.randint(1,6)
    num2 = random.randint(1,6)
    return [num1,num2]

class Board:
    def __init__(self) -> None:
        self.locationList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.sideboardList = [0,0]
        self.hitPieceList = []
        self.takeOutStatus = [False,False]
    def setStartPositions(self):
        self.locationList = [[1,1],[],[],[],[],[0,0,0,0,0],[],[0,0,0],[],[],[],[1,1,1,1,1],[0,0,0,0,0],[],[],[],[1,1,1],[],[1,1,1,1,1],[],[],[],[],[0,0]]
    def calcPip(self):
        darkPIP = 0
        lightPIP = 0
        for listNum in range(len(self.locationList)):
            list = self.locationList[listNum]
            listNum = listNum + 1
            if len(list) > 0:
                if list[0] == 1:
                    darkPIP = darkPIP + (len(list)*(25-listNum))
                if list[0] == 0:
                    lightPIP = lightPIP + (len(list)*listNum)
        return [darkPIP,lightPIP]
    def findLastOccupiedPoint(self,color):
        if color == 0:
            for index in range(23,-1,-1):
                if len(self.locationList[index]) > 0 and self.locationList[index][0] == color:
                    return index + 1
        if color == 1:
            for index in range(0,24,1):
                if len(self.locationList[index]) > 0 and self.locationList[index][0] == color:
                    return index + 1
    def updateTakeOutStatus(self):
        self.takeOutStatus[0] = True if self.findLastOccupiedPoint(1) > 18 else False
        self.takeOutStatus[1] = True if self.findLastOccupiedPoint(0) < 7 else False
    def calcPossibleMoves(self,roll,player,biggestRoll):
        self.updateTakeOutStatus()
        moveList = []
        def canMoveTo(point,player):
            if point > 24 or point < 1:
                return False
            pointList = self.locationList[point-1]
            opp = 1 if player == 0 else 0
            if len(pointList) == 0:
                return True
            if len(pointList) > 0 and pointList[0] == player:
                return True
            if len(pointList) == 1 and pointList[0] == opp:
                return True
        
        if player == 1:
            if 1 in self.hitPieceList:
                if canMoveTo(roll,1) == True:
                    moveList.append(("hit",roll))
            else:
                for point in range(24):
                    pointList = self.locationList[point]
                    if len(pointList) > 0 and pointList[0] == 1:
                        if canMoveTo(point+roll+1,1) == True:
                            moveList.append((point+1,point+roll+1))
                if self.takeOutStatus[0] == True:
                    if len(self.locationList[24-roll]) > 0 and self.locationList[24-roll][0] == 1:
                        moveList.append((25-roll,"safe"))
                    if biggestRoll == True and self.findLastOccupiedPoint(1) > 25-roll:
                        moveList.append((self.findLastOccupiedPoint(1),"safe"))

        if player == 0:
            if 0 in self.hitPieceList:
                if canMoveTo(25-roll,0) == True:
                    moveList(("hit",25-roll))
            else:
                for point in range(24):
                    pointList = self.locationList[point]
                    if len(pointList) > 0 and pointList[0] == 0:
                        if canMoveTo(point-roll+1,0) == True:
                            moveList.append((point+1,point-roll+1))
                if self.takeOutLight == True:
                    if len(self.locationList[roll-1]) > 0 and self.locationList[roll-1][0] == 0: 
                        moveList.append((roll,"safe"))
                    if biggestRoll == True and self.findLastOccupiedPoint(0) < roll:
                        moveList.append((self.findLastOccupiedPoint(0),"safe"))


class Turn:
    def __init__(self,player,Board,First=False) -> None:
        self.roll = RollDice()
        self.player = player
        self.doublesTurn = True if self.roll[0] == self.roll[1] else False
        if First == True and self.doublesTurn == True:
            self.roll = [random.randint(1,3),random.randint(4,6)]
            self.doublesTurn = False
        



#Calc Possible moves in board -- called within turn.

#Turn has multiple steps:
    #step1 - calc possible moves 
    #step2 - display possible moves interactively and allow selections
    #Step3 - make necessary updates with move
    
    #If regular x2 // if double x4


#have a "usable roll list" that shows wich roll is still usable
#do the calc roll for the items in this list (unless doubles)
#when move is made, remove that roll
