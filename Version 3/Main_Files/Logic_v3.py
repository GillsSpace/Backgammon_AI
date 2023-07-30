import random
import copy
from Main_Files.Graphics_v3 import createMoveStartSprites, GenerateMoveLineDataFast
import collections

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
def rollDice():
    num1 = random.randint(1,6)
    num2 = random.randint(1,6)
    return [num1,num2]
def isLegalBoard(positions):
    total_light = 0
    total_dark = 0
    for position in positions[0:24]:
        if position == 0:
            pass
        elif position < 0:
            total_dark += (-1 * position)
        elif position > 0:
            total_light += position
    total_dark += positions[24]
    total_dark += positions[26]
    total_light += positions[25]
    total_light += positions[27]

    if (total_light == 15) and (total_dark == 15):
        return True
    return False
def isLegalRoll(roll):
    if roll[0] in range(1,7) and roll[1] in range(1,7):
        return True
    else:
        return False

class Board:
    def __init__(self, PositionList=None) -> None:
        self.positions = [-2,0,0,0,0,5,0,3,0,0,0,-5,5,0,0,0,-3,0,-5,0,0,0,0,2,0,0,0,0] if PositionList == None else PositionList
        # index 0  to 23 represents number of checkers on points - negative for player one(dark), positive for player 2(light)
        # index 24 to 25 represents number of checkers on the bar - index 24 for P1, index 25 for P2
        # index 26 to 27 represents number of checkers off - index 26 for P1, index 27 for P2
        self.pip = [167,167] 
        self.lastPoints = [1,24]
        self.bearOffStatus = [False,False]
        self.MoveLineData = None

    def setStartPositions(self):
        self.positions = [-2,0,0,0,0,5,0,3,0,0,0,-5,5,0,0,0,-3,0,-5,0,0,0,0,2,0,0,0,0]
        # index 0  to 23 represents number of checkers on points - negative for player one, positive for player 2
        # index 24 to 25 represents number of checkers on the bar - index 24 for P1, index 25 for P2
        # index 26 to 27 represents number of checkers off - index 26 for P1, index 27 for P2
        self.pip = [167,167] 
        self.lastPoints = [1,24]
        self.bearOffStatus = [False,False]
        self.MoveLineData = None

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

    def makeMove(self,move,player,fromMakeMoves=False): #Updates the Board with an inputted move: (start point,end point) // also updates pip, lastPoint, and BearOff
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
            self.positions[25 + player] +=1
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
        if fromMakeMoves == False:
            self.updatePip()
            self.updateLastOccupiedPoint(player)
            self.updateBearOffStatus()

    def makeMoves(self,moves,player,updateLineData=False): #Updates the Board with a series of moves: ((move1),(move2),ect.) // also updates pip, lastPoint, and BearOff
        MoveLineData = []
        if len(moves) > 0 and type(moves[0]) == int:
            self.makeMove(moves,player,True)
            if updateLineData == True:
                self.MoveLineData = GenerateMoveLineDataFast(moves,self)
        else:
            for move in moves:
                self.makeMove(move,player,True)
                if updateLineData == True:
                   MoveLineData.append(GenerateMoveLineDataFast(move,self)) 
            self.MoveLineData = MoveLineData
        self.updatePip()
        self.updateLastOccupiedPoint(player)
        self.updateBearOffStatus()

    def updateLastOccupiedPoint(self,player): #Updates the self.lastPoints value for the given player
        if player == 1:
            for index in range(0,24,1):
                if self.positions[index] < 0:
                    self.lastPoints[0] = index + 1
                    break
        else:
            for index in range(23,-1,-1):
                if self.positions[index] > 0:
                    self.lastPoints[1] = index + 1
                    break 
                
    def updateBearOffStatus(self): #Updates the self.bearOffStatus values based on current lastPoints
        self.bearOffStatus[0] = True if (self.bearOffStatus[0]) or (self.lastPoints[0] > 18) else False
        self.bearOffStatus[1] = True if (self.bearOffStatus[1]) or (self.lastPoints[1] < 7) else False

    def returnMovesForDie(self,die,player,isBiggestDieOrSecondMove): #returns all move options a die can be used for in the current board state: [(moveOption1),(moveOption2),ect.]
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

    def returnMoveSequences(self,player,roll): #for a given roll returns list of moves sequences that result in unique Board States: [((move1),(move2)),((move1),(move2)), ect.]
        Sequences = []
        EndBoards = []
        if roll[0] != roll[1]:
            biggerDie = roll[0] if roll[0] >= roll[1] else roll[1]
            FirstMoves = []

            #All Possible First Moves
            for die in roll: 
                FirstMoves.append(self.returnMovesForDie(die,player,(biggerDie == die)))
            FirstMoves = FirstMoves[0] + FirstMoves[1]

            for move in FirstMoves:
                algoBoard1 = copy.deepcopy(self)
                algoBoard1.makeMove(move,player)
                if algoBoard1.pip[player - 1] == 0:
                    Sequences = [move]
                    return Sequences
                usedDie = fromMoveToDie(move[0],move[1],roll,player)
                unusedDie = roll[0] if roll[1] == usedDie else roll[1]
                SecondMoves = algoBoard1.returnMovesForDie(unusedDie,player,True)
                if len(SecondMoves) == 0:
                    Sequences.append(move)
                    continue
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
                    Sequences = [(firstMove)]
                    return Sequences
                SecondMoves = algoBoard1.returnMovesForDie(roll[0],player,True)
                if len(SecondMoves) == 0:
                    Sequences.append(firstMove)
                    continue
                for secondMove in SecondMoves:
                    algoBoard2 = copy.deepcopy(algoBoard1)
                    algoBoard2.makeMove(secondMove,player)
                    if algoBoard2.pip[player - 1] == 0:
                        Sequences.append((firstMove,secondMove))
                        continue
                    ThirdMoves = algoBoard2.returnMovesForDie(roll[0],player,True)
                    if len(ThirdMoves) == 0:
                        Sequences.append([firstMove,secondMove])
                        continue
                    for thirdMove in ThirdMoves:
                        algoBoard3 = copy.deepcopy(algoBoard2)
                        algoBoard3.makeMove(thirdMove,player)
                        if algoBoard2.pip[player - 1] == 0:
                            Sequences = [(firstMove,secondMove,thirdMove)]
                            return Sequences
                        ForthMoves = algoBoard3.returnMovesForDie(roll[0],player,True)
                        if len(ForthMoves) == 0:
                            Sequences.append([firstMove,secondMove,thirdMove])
                            continue
                        for forthMove in ForthMoves:
                            algoBoard4 = copy.deepcopy(self)
                            algoBoard4.makeMoves((firstMove,secondMove,thirdMove,forthMove),player)
                            if algoBoard4.positions not in EndBoards:
                                Sequences.append((firstMove,secondMove,thirdMove,forthMove))
                                EndBoards.append(algoBoard4.positions)
            return Sequences

class Turn: 
    def __init__(self,player,playerType,roll=None,First=False):
        self.player = player #Either 1 or 2
        self.playerType = playerType #Either "AI" or "Human"

        self.roll = roll if roll != None else rollDice()
        self.doubles_turn = True if self.roll[0] == self.roll[1] else False
        self.unused_dice = []

        self.current_possible_moves = []

        if self.playerType == "Human":
            self.sprites_move_start = []
            self.sprites_move_end = []
            self.sprite_active = []

        #prevents Doubles on first Roll
        if First and self.doubles_turn: 
            while (self.roll[0] == self.roll[1]):
                self.roll = rollDice()
            self.doubles_turn = False

        #Sets up unused_dice
        if self.doubles_turn == True:
            self.unused_dice = [self.roll[0]] * 4
        else:
            self.unused_dice = copy.deepcopy(self.roll)

    def updatePossibleMovesHumanFormat(self,Board: Board): #updates self.currentPossibleMoves in Human playerType Format for use by Main Game Loop
        # Human Format: [(startPoint,[possibleFirstEndPoint, possibleSecondEndPoint]), (1, [3, 5]), (12, [14]), (17, [19]), (19, [21, 23])]
        self.current_possible_moves = []
        if self.doubles_turn == True and len(self.unused_dice) > 0:
            self.current_possible_moves = Board.returnMovesForDie(self.roll[0],self.player, True)
            self.current_possible_moves = [(move[0],[move[1]]) for move in self.current_possible_moves]
        else:
            biggerDie = self.roll[0] if self.roll[0] > self.roll[1] else self.roll[1]
            for roll in self.unused_dice:
                self.current_possible_moves.append(Board.returnMovesForDie(roll,self.player,(roll == biggerDie) or (len(self.unused_dice) == 1)))
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
                            numFin.append(move[1])
                    finalList = ((startPoint),(numFin)) 
                    if finalList in self.current_possible_moves:
                        pass
                    else:
                        self.current_possible_moves.append(finalList)
            else:
                workingMovesList = []
                for possibleMove in self.current_possible_moves[0]:
                    move = (possibleMove[0],[possibleMove[1]])
                    workingMovesList.append(move)
                self.current_possible_moves = workingMovesList
    
    def updatePossibleMovesStandardFormat(self,Board: Board): #updates self.currentPossibleMoves to full set of unique move sequences for use by AI programs
        self.current_possible_moves = Board.returnMoveSequences(self.player,self.roll)

    def formSpriteList(self,Board): #creates and updates a sprit list for use by Main Game Loop
        #Needs Human Format for self.current_possible_moves 
        self.sprites_move_start = createMoveStartSprites(self.current_possible_moves,Board,self.player)


#Calculating Moves Logic

#For AI Turn Output => List of possible move combinations ex: [ ((1,3),(2,6)) , ((2,5),(5,9)) , ect.. ]
#   Format = [ ((move1),(move2)) , (moveCombination2) , ect ]
#For Human Turn Output => List of Possible first Moves ex: [ (1,[3,6]) , (2,[4,7]) , ect... ] 
#   Format = [ (startPoint,(endpoint1, endpoint2))]
#   Recalculated for second (possibly third and forth move)

#In Board => Calculate all moves for a particular dice
#In Turn ==> Calculate correct Lists for turn