import time
import random
import copy
import collections

#Data:
Data_rollOptions = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),(5,5),(5,6),(6,6)]

#Helper Functions:
def fromMoveToDie(start,end,roll,player):
    if start == 1001:
        die = end if player == 1 else (25 - end)
    elif end == 2002:
        die = start if start in roll else (25 - start)
        if die not in roll:
            die = max(roll)
    else:
        diff = end - start
        die = diff if diff > 0 else (diff * -1)
    return die
def average(inputList):
    return sum(inputList) / len(inputList)

#Classes:
class FastTurn:
    def __init__(self,player,roll) -> None:
        self.player = player
        self.roll = roll

class FastBoard:
    def __init__(self, PositionList=None) -> None:
        self.positions = [-2,0,0,0,0,5,0,3,0,0,0,-5,5,0,0,0,-3,0,-5,0,0,0,0,2,0,0,0,0] if PositionList == None else PositionList
        # index 0  to 23 represents number of checkers on points - negative for player one, positive for player 2
        # index 24 to 25 represents number of checkers on the bar - index 24 for P1, index 25 for P2
        # index 26 to 27 represents number of checkers off - index 26 for P1, index 27 for P2
        self.pip = [167,167] 
        self.lastPoints = [1,24]
        self.bearOffStatus = [False,False]

    def updatePip(self): #Creates and updates a self.pip Value: (P1 pip, P2 pip)
        p1_pip = 0
        p2_pip = 0
        for i in range(24):
            if self.positions[i] > 0:
                p2_pip += (i + 1) * self.positions[i]
            elif self.positions[i] < 0:
                p1_pip += (24 - i) * abs(self.positions[i])
        p1_pip += 25 * self.positions[24]
        p2_pip += 25 * self.positions[25]
        self.pip = (p1_pip, p2_pip)
    def returnPip(self): #Returns a Pip Value: (P1 pip, P2 pip)
        p1_pip = 0
        p2_pip = 0
        for i in range(24):
            if self.positions[i] > 0:
                p2_pip += (i + 1) * self.positions[i]
            elif self.positions[i] < 0:
                p1_pip += (24 - i) * abs(self.positions[i])
        p1_pip += 25 * self.positions[24]
        p2_pip += 25 * self.positions[25]
        return (p1_pip, p2_pip)

    def makeMove(self,move,player): #Updates the Board with an inputted move: (start point,end point)
        if move[0] == 1001:
            endPointIndex = move[1] - 1
            self.positions[23 + player] -= 1
            if player == 1:
                if self.positions[endPointIndex] > 0:
                    self.positions[endPointIndex] = -1
                    self.positions[25] += 1
                else:
                    self.positions[endPointIndex] -= 1
            else:
                if self.positions[endPointIndex] < 0:
                    self.positions[endPointIndex] = 1
                    self.positions[24] += 1
                else:
                    self.positions[endPointIndex] += 1
        elif move[1] == 2002:
            startPointIndex = move[0] - 1
            if player == 1:
                self.positions[startPointIndex] += 1
            else:
                self.positions[startPointIndex] -= 1
            self.positions[25 + player]
        else:
            endPointIndex = move[1] - 1
            startPointIndex = move[0] - 1
            if player == 1:
                self.positions[startPointIndex] += 1
            else:
                self.positions[startPointIndex] -= 1
            if player == 1:
                if self.positions[endPointIndex] > 0:
                    self.positions[endPointIndex] = -1
                    self.positions[25] += 1
                else:
                    self.positions[endPointIndex] -= 1
            else:
                if self.positions[endPointIndex] < 0:
                    self.positions[endPointIndex] = 1
                    self.positions[24] += 1
                else:
                    self.positions[endPointIndex] += 1
        self.updatePip()
    def makeMoves(self,moves,player): #Updates the Board with a series of moves: ((move1),(move2),ect.)
        if len(moves) > 0 and type(moves[0]) == int:
            self.makeMove(moves,player)
        else:
            for move in moves:
                self.makeMove(move,player)

    def updateLastOccupiedPoint(self,player):
        if player == 1:
            for index in range(0,24,1):
                if self.positions[index] < 0:
                    self.lastPoints[0] = index + 1
                    return
        if player == 2:
            for index in range(23,-1,-1):
                if self.positions[index] > 0:
                    self.lastPoints[1] = index + 1
                    return
    def updateBearOffStatus(self):
        self.bearOffStatus[0] = True if self.lastPoints[0] > 18 else False
        self.bearOffStatus[1] = True if self.lastPoints[1] < 7 else False

    def returnMovesForDie(self,die,player,isBiggestDieOrSecondMove):
        moveList = []
        def canMoveTo(point,player):
            if point > 24 or point < 1:
                return False
            oppValue = -1 if player == 2 else 1
            if self.positions[point-1] == 0:
                return True
            if self.positions[point-1] > 0 and player == 2:
                return True
            if self.positions[point-1] < 0 and player == 1:
                return True
            if self.positions[point-1] == oppValue:
                return True
                print("Hit Move to Found")#DEBUG
        
        if player == 1:
            if self.positions[24] > 0:
                if canMoveTo(die,1) == True:
                    moveList.append((1001,die))
            else:
                for pointIndex in range(24):
                    if self.positions[pointIndex] < 0:
                        if canMoveTo(pointIndex+die+1,1) == True:
                            moveList.append((pointIndex+1,pointIndex+die+1))
                if self.bearOffStatus[0] == True:
                    if self.positions[24-die] < 0:
                        moveList.append((25-die,2002))
                    if isBiggestDieOrSecondMove and self.lastPoints[0] > 25-die:
                        moveList.append((self.lastPoints[0],2002))

        else:
            if self.positions[25] > 0:
                if canMoveTo(25-die,2) == True:
                    moveList.append((1001,25-die))
            else:
                for pointIndex in range(24):
                    if self.positions[pointIndex] > 0:
                        if canMoveTo(pointIndex-die+1,2) == True:
                            moveList.append((pointIndex+1,pointIndex-die+1))
                if self.bearOffStatus[1] == True:
                    if self.positions[die-1] > 0: 
                        moveList.append((die,2002))
                    if isBiggestDieOrSecondMove and self.lastPoints[1] < die:
                        moveList.append((self.lastPoints[1],2002))

        return moveList

    def returnMoveSet(self,player,roll):
        pass
    def returnMoveSequences(self,player,roll):
        Sequences = []
        EndBoards = []
        if roll[0] != roll[1]:
            biggerDie = roll[0] if roll[0] >= roll[1] else roll[1]
            FirstMoves = []

            #All Possible First Moves
            self.updateLastOccupiedPoint(player)
            self.updateBearOffStatus()
            for die in roll: 
                FirstMoves.append(self.returnMovesForDie(die,player,(biggerDie == die)))
            FirstMoves = FirstMoves[0] + FirstMoves[1]

            for move in FirstMoves:
                algoBoard1 = copy.deepcopy(self)
                algoBoard1.makeMove(move,player)
                self.updatePip()
                if algoBoard1.pip[player - 1] == 0:
                    Sequences = [move]
                    return Sequences
                usedDie = fromMoveToDie(move[0],move[1],roll,player)
                unusedDie = roll[0] if roll[1] == usedDie else roll[1]
                SecondMoves = algoBoard1.returnMovesForDie(unusedDie,player,True)
                if len(SecondMoves) == 0:
                    Sequences = [move]
                    return Sequences
                for secondMove in SecondMoves:
                    algoBoard2 = copy.deepcopy(self)
                    algoBoard2.makeMoves((move,secondMove),player)
                    if algoBoard2.positions not in EndBoards:
                        Sequences.append((move,secondMove))
                        EndBoards.append(algoBoard2.positions)
            return Sequences
        
        else:
            FirstMoves = self.returnMovesForDie(roll[0],player,True)
            for firstMove in FirstMoves:
                algoBoard1 = copy.deepcopy(self)
                algoBoard1.makeMove(firstMove,player)
                if algoBoard1.pip[player - 1] == 0:
                    Sequences = [firstMove]
                    return Sequences
                SecondMoves = algoBoard1.returnMovesForDie(roll[0],player,True)
                for secondMove in SecondMoves:
                    algoBoard2 = copy.deepcopy(algoBoard1)
                    algoBoard2.makeMove(secondMove,player)
                    if algoBoard2.pip[player - 1] == 0:
                        Sequences = [(firstMove,secondMove)]
                        return Sequences
                    ThirdMoves = algoBoard2.returnMovesForDie(roll[0],player,True)
                    for thirdMove in ThirdMoves:
                        algoBoard3 = copy.deepcopy(algoBoard2)
                        algoBoard3.makeMove(thirdMove,player)
                        if algoBoard2.pip[player - 1] == 0:
                            Sequences = [(firstMove,secondMove,thirdMove)]
                            return Sequences
                        ForthMoves = algoBoard3.returnMovesForDie(roll[0],player,True)
                        for forthMove in ForthMoves:
                            algoBoard4 = copy.deepcopy(self)
                            algoBoard4.makeMoves((firstMove,secondMove,thirdMove,forthMove),player)
                            if algoBoard4.positions not in EndBoards:
                                Sequences.append((firstMove,secondMove,thirdMove,forthMove))
                                EndBoards.append(algoBoard4.positions)
            return Sequences

class TurnSolution:
    def __init__(self, Board:FastBoard, MoveSequence) -> None:
        self.Board = copy.deepcopy(Board)
        self.MoveSequence = MoveSequence
        self.expectedPipDiff = 0

class SubTurn:
    #Represents a possible turn of the opponent's
    def __init__(self, Board:FastBoard, PrimaryMoveSequence, Roll, Player) -> None:
        self.Board = copy.deepcopy(Board)
        self.PrimaryMoveSequence = PrimaryMoveSequence
        self.Roll = Roll
        self.Player = Player
        self.largestPipDiff = 0 #represents the largest pip difference opponent can generate from the subTurn.

def ReturnTurnSolutions(inputBoard:FastBoard,inputTurn:FastTurn):
    turnSolutions = []
    playerTurnSequences = inputBoard.returnMoveSequences(inputTurn.player,inputTurn.roll)
    for moveSequence in playerTurnSequences:
        instanceTurnSolution = TurnSolution(inputBoard,moveSequence)
        instanceTurnSolution.Board.makeMoves(moveSequence,inputTurn.player)
        turnSolutions.append(instanceTurnSolution)
    return turnSolutions

def PipMinMaxBasic(subTurn:SubTurn,player,Max=True): 
    #From an input of a SubTurn, returns either the maximum or minimum pip difference that can be generated in the courses of the subTurn

    pipList = []
    PossibleMovesList = subTurn.Board.returnMoveSequences(player,subTurn.Roll)

    for moves in PossibleMovesList:
        algoBoard = copy.deepcopy(subTurn.Board)
        algoBoard.makeMoves(moves,player)
        algoBoard.updatePip()
        pipDiff = (algoBoard.pip[1] - algoBoard.pip[0]) if player == 1 else (algoBoard.pip[0] - algoBoard.pip[1])
        pipList.append(pipDiff)
    
    if len(pipList) == 0:
        pipDiff = (subTurn.Board.pip[1] - subTurn.Board.pip[0]) if player == 1 else (subTurn.Board.pip[0] - subTurn.Board.pip[1])
        return pipDiff
    
    maxPipDiff = max(pipList)
    minPipDiff = min(pipList)

    if Max == True:
        return maxPipDiff
    else:
        return minPipDiff

#Running:
def Full_Run(inputBoard:FastBoard,inputTurn:FastTurn):
    #Takes a input of a FastBoard and a FastTurn and returns the optimal move for the current player to make. 
    initialTurnSolutions = ReturnTurnSolutions(inputBoard,inputTurn)
    possiblePipDiffs = []
    for turnSolution in initialTurnSolutions:
        subTurnsList = []
        for roll in Data_rollOptions:
            instanceSubTurn = SubTurn(turnSolution.Board,turnSolution.MoveSequence,roll,(1 if inputTurn.player == 2 else 2))
            subTurnsList.append(instanceSubTurn)
        MaxPipDiffs = []
        for subTurn in subTurnsList:
            subTurn.largestPipDiff = PipMinMaxBasic(subTurn,subTurn.Player)
            MaxPipDiffs.append(subTurn.largestPipDiff)
            if subTurn.Roll[0] != subTurn.Roll[1]:
                #accounts fot weighted average of non-double rolls, appends the value twice:
                MaxPipDiffs.append(subTurn.largestPipDiff)
        turnSolution.expectedPipDiff = average(MaxPipDiffs)
        possiblePipDiffs.append(turnSolution.expectedPipDiff)

    if len(possiblePipDiffs) != 0:
        maxPipDiff = min(possiblePipDiffs)
        #Using min function because possible pip differences are calculated for opponents. 
        indexOfTurn = possiblePipDiffs.index(maxPipDiff)
        return initialTurnSolutions[indexOfTurn].MoveSequence 
    else:
        return None  
