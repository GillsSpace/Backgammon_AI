import random
import copy

class Board:
    def __init__(self) -> None:
        self.PositionListPoints = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
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




