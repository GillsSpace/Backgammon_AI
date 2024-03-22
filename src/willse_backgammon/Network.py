### Imports ###
import copy
import random
import sqlite3
import time

import numpy as np

import Code.Main_Files.AI as AI
import Code.Main_Files.Logic as Logic


### Initialize Database ###
# Network_Type1.initialize_data_set()

### Tournament ###

def runTournament(rounds, matchLength, runNumber, reInitialize=False):
    print(f"Beginning Tournament... ")
    st = time.time()

    PATH = "Code\AI_Agents\\Network_Type1_Data_v3.sqlite3"
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    if reInitialize:
        try:
            cursor.execute("DROP TABLE Network_Values_Tournament")
        except:
            pass

        cursor.execute("CREATE TABLE Network_Values_Tournament (id TEXT, data TEXT)")

        cursor.execute("INSERT INTO Network_Values_Tournament VALUES (?, ?)", ("Rounds", "0"))

        for i in range(64):
            id = f"W{i + 1}"
            dataSet1 = []
            for i in range(2017):
                num = round(random.random(), 4)
                num = -1 * num if random.randint(1, 2) == 1 else num
                dataSet1.append(num)
            values = " ".join(str(num) for num in dataSet1)
            cursor.execute("INSERT INTO Network_Values_Tournament VALUES (?, ?)", (id, values,), )
            i = i + 1

        connection.commit()
        print("Data Set Initialized")

    result = cursor.execute("SELECT data FROM Network_Values_Tournament WHERE id = ?", ("Rounds",), )
    totalRounds = int(str(result.fetchall()[0][0]))

    if totalRounds >= rounds:
        print(f"This data has already completed {rounds} rounds. It has currently trained {totalRounds} rounds.")
        return

    roundsToGo = rounds - totalRounds

    for roundIteration in range(roundsToGo):
        stR = time.time()

        # Finding Current Round:
        result = cursor.execute("SELECT data FROM Network_Values_Tournament WHERE id = ?", ("Rounds",), )
        netRounds = int(str(result.fetchall()[0][0]))
        thisRound = netRounds + 1
        roundLearningRate = learningRate(thisRound)
        cursor.execute("UPDATE Network_Values_Tournament SET data = ? WHERE id = ?", (thisRound, "Rounds"))
        print(f"Starting Round {thisRound}.")

        roundIn = [i for i in range(1, 65)]
        roundOut = []

        semifinalist = []
        finalists = []

        # Running Bracket Games:
        while len(roundIn) > 1:
            i = 0
            while i < len(roundIn):
                NetworkIdent1 = f"V1.0-NVT-W{roundIn[i]}"
                NetworkIdent2 = f"V1.0-NVT-W{roundIn[i + 1]}"
                matchWinner, matchLooser = runMatch(NetworkIdent1, NetworkIdent2, matchLength)
                roundOut.append(roundIn[i] if matchLooser == 1 else roundIn[i + 1])
                i = i + 2

            for outNetwork in roundOut:
                roundIn.remove(outNetwork)
            if len(roundIn) == 2:
                finalists = copy.deepcopy(roundIn)
                semifinalist = copy.deepcopy(roundOut)
            roundOut = []
            print(f"    Stage Ended. Current Competitors = {roundIn}")

        # Gets 1st, 2nd, and 3rd place idents:
        roundWinnerIdent = f"V1.0-W{roundIn[0]}"
        finalists.remove(roundIn[0])
        roundSecondIdent = f"V1.0-W{finalists[0]}"
        roundThird1Ident = f"V1.0-W{semifinalist[0]}"
        roundThird2Ident = f"V1.0-W{semifinalist[1]}"

        # Print Tournament Results
        print(
            f"Round {thisRound} Complete. Network {roundWinnerIdent} Finished First. 2nd = {roundSecondIdent}. 3rd = {roundThird1Ident} & {roundThird2Ident}. Current Learning Rate = {roundLearningRate}")
        print("    Updated = ", end="")

        # Retrieving winning networks' data
        result = cursor.execute("SELECT data FROM Network_Values_Tournament WHERE id = ?", (roundWinnerIdent[5:],), )
        data1 = str(result.fetchall()[0][0])

        result = cursor.execute("SELECT data FROM Network_Values_Tournament WHERE id = ?", (roundSecondIdent[5:],), )
        data2 = str(result.fetchall()[0][0])
        data2 = data2.rsplit()
        data2 = [float(num) for num in data2]

        result = cursor.execute("SELECT data FROM Network_Values_Tournament WHERE id = ?", (roundThird1Ident[5:],), )
        data31 = str(result.fetchall()[0][0])
        data31 = data31.rsplit()
        data31 = [float(num) for num in data31]

        result = cursor.execute("SELECT data FROM Network_Values_Tournament WHERE id = ?", (roundThird2Ident[5:],), )
        data32 = str(result.fetchall()[0][0])
        data32 = data32.rsplit()
        data32 = [float(num) for num in data32]

        # Archiving every 100th network:
        if (thisRound) % 100 == 0 or thisRound == 1:
            ident = f"A{runNumber}-{thisRound}"
            cursor.execute("INSERT INTO Network_Values_Tournament VALUES (?, ?)", (ident, data1))

        data1 = data1.rsplit()
        data1 = [float(num) for num in data1]

        # Updating Networks Data

        for network in range(1, 65):

            values = None
            ident = f"W{network}"

            if network == 1 or network == 2:
                dataSet = []
                for i in range(2017):
                    num = round(random.random(), 4)
                    num = -1 * num if random.randint(1, 2) == 1 else num
                    dataSet.append(num)
                values = " ".join(str(num) for num in dataSet)

            elif network == 3:
                values = " ".join(str(num) for num in data1)

            elif network <= 32:
                newData = []
                for num in data1:
                    diff = ((random.random() * 2) - 1) * roundLearningRate
                    endNum = round(num + diff, 4)
                    newData.append(endNum)
                values = " ".join(str(num) for num in newData)

            elif network == 33:
                values = " ".join(str(num) for num in data2)

            elif network <= 48:
                newData = []
                for num in data2:
                    diff = ((random.random() * 2) - 1) * roundLearningRate
                    endNum = round(num + diff, 4)
                    newData.append(endNum)
                values = " ".join(str(num) for num in newData)

            elif network == 49:
                values = " ".join(str(num) for num in data31)

            elif network <= 56:
                newData = []
                for num in data31:
                    diff = ((random.random() * 2) - 1) * roundLearningRate
                    endNum = round(num + diff, 4)
                    newData.append(endNum)
                values = " ".join(str(num) for num in newData)

            elif network == 57:
                values = " ".join(str(num) for num in data32)

            elif network <= 64:
                newData = []
                for num in data32:
                    diff = ((random.random() * 2) - 1) * roundLearningRate
                    endNum = round(num + diff, 4)
                    newData.append(endNum)
                values = " ".join(str(num) for num in newData)

            cursor.execute("UPDATE Network_Values_Tournament SET data = ? WHERE id = ?", (values, ident))
            connection.commit()
            print(f"{network}", end=" ", flush=True)

        connection.commit()

        etR = time.time()
        print()
        print(f"Round {thisRound} Updates Complete. Round Time = {etR - stR}")

    et = time.time()
    print(f"Tournament Complete: Duration = {et - st}")


def runMatch(ident1, ident2, length):
    """Helper Function for runTournament. returns winner, looser of a match of length "length" between networks "ident1" and "ident2"."""
    ident1Wins = 0
    ident2Wins = 0
    for game in range(length):
        winner, looser = runGame(ident1, ident2)
        ident1Wins = ident1Wins + 1 if winner == 1 else ident1Wins
        ident2Wins = ident2Wins + 1 if winner == 2 else ident2Wins
        if ident1Wins > (length / 2):
            return 1, 2
        elif ident2Wins > (length / 2):
            return 2, 1

    # If tied after "length" games, play tie-breaker:
    return runGame(ident1, ident2)


def runGame(ident1, ident2):
    """Helper Function for runTournament. returns winner, looser of a singe game between networks "ident1" and "ident2". """
    Board = Logic.Board()
    Board.setStartPositions()

    startingPlayer = random.randint(1, 2)
    gameOver = False

    Turn = Logic.Turn(startingPlayer, "AI", None, First=True)
    Moves = AI.Silent_Main(Board, Turn, "Network", ident2 if Turn.player == 2 else ident1)
    Board.makeMoves(Moves, Turn.player)

    while not gameOver:
        Turn = Logic.Turn(1 if Turn.player == 2 else 2, "AI", None)
        Moves = AI.Silent_Main(Board, Turn, "Network", ident2 if Turn.player == 2 else ident1)
        Board.makeMoves(Moves, Turn.player)

        if Board.pip[1 if Turn.player == 2 else 0] == 0:
            gameOver = True
            looser = 1 if Turn.player == 2 else 1
            winner = Turn.player

    return winner, looser


def learningRate(round):
    return 0.25 * ((-1 / (1 + np.e ** (-round / 2000))) + 1.05)


def create_data_set(game_number):
    import csv

    positions = []
    output = []

    # ident1 = "V1.0-NVT-A1-100"
    # ident2 = "V1.0-NVT-A1-100"

    ident1 = "TS1"
    ident2 = "TS1"

    board = Logic.Board()
    board.setStartPositions()

    starting_player = random.randint(1, 2)
    game_over = False

    turn = Logic.Turn(starting_player, "AI", None, First=True)
    moves = AI.Silent_Main(board, turn, "TS1", ident2 if turn.player == 2 else ident1,multiSuppression=True)
    board.makeMoves(moves, turn.player)

    while not game_over:
        positions.append(copy.deepcopy(board.positions))
        turn = Logic.Turn(1 if turn.player == 2 else 2, "AI", None)
        moves = AI.Silent_Main(board, turn, "TS1", ident2 if turn.player == 2 else ident1,multiSuppression=True)
        board.makeMoves(moves, turn.player)

        if board.pip[1 if turn.player == 2 else 0] == 0:
            game_over = True
            output = []
            if turn.player == 1 and board.positions[27] == 0:
                output = [1,0,0,0]
            if turn.player == 1 and board.positions[27] != 0:
                output = [0,1,0,0]
            if turn.player == 2 and board.positions[26] != 0:
                output = [0,0,1,0]
            if turn.player == 2 and board.positions[26] == 0:
                output = [0,0,0,1]

    with open('Code/AI_Agents/Data_sets/data_set_1.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        for positions in positions:
            writer.writerow([game_number,positions,output])

    return output

### Run Code ###
for i in range(1000):
    outcome = create_data_set(i+1)
    print(f"Set {i+1} Completed, Outcome = {outcome}")
# runTournament(1000, 99, 1, False)
