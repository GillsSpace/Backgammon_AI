### Imports ###
import arcade, time, copy, sqlite3, random
import numpy as np

import Main_Files.Logic_v3 as Logic
import Main_Files.AI_v3 as AI
import Main_Files.Graphics_v3 as Graphics

import AI_Agents.Network_Type1_v3 as Network_Type1

### Initialize Database ###
# Network_Type1.InitializeDataSet()

### Tournament ###

def runTournament(rounds,learningRate=0.01,matchLength=1,reInitialize=True):
    print(f"Beginning Tournament... ")
    st = time.time()

    PATH = "Version 3\AI_Agents\\Network_Type1_Data_v3.sqlite3"
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    if reInitialize:
        try:
            cursor.execute("DROP TABLE Network_Values_Tournament")
        except:
            pass

        cursor.execute("CREATE TABLE Network_Values_Tournament (id TEXT, data TEXT)")

        cursor.execute("INSERT INTO Network_Values_Tournament VALUES (?, ?)",("Rounds","0"))

        for i in range(64):
            id = f"W{i+1}"
            dataSet1 = []
            for i in range(2017):
                num = round(random.random(),4)
                num = -1 * num if random.randint(1,2) == 1 else num
                dataSet1.append(num)
            values = " ".join(str(num) for num in dataSet1)
            cursor.execute("INSERT INTO Network_Values_Tournament VALUES (?, ?)",(id,values,),)
            i = i + 1

        connection.commit()
        print("Data Set Initialized")

    for roundT in range(rounds):
        stR = time.time()
        print(f"Starting Round {roundT + 1}.")

        roundIn = [i for i in range(1,65)]
        roundOut = []

        while len(roundIn) > 1:
            i = 0
            while i < len(roundIn):
                NetworkIdent1 = f"V1.0-W{roundIn[i]}"
                NetworkIdent2 = f"V1.0-W{roundIn[i+1]}"
                matchWinner, matchLooser = runMatch(NetworkIdent1,NetworkIdent2,matchLength)
                roundOut.append(roundIn[i] if matchLooser == 1 else roundIn[i+1])
                i = i + 2

            for outNetwork in roundOut:
                roundIn.remove(outNetwork)
            roundOut = []
            print(f"    Stage Ended. Current Competitors = {roundIn}")

        roundWinnerIdent = f"V1.0-W{roundIn[0]}"
        print(f"Round {roundT+1} Complete. Network {roundWinnerIdent} Finished First.")

        result = cursor.execute("SELECT data FROM Network_Values_Tournament WHERE id = ?",(roundWinnerIdent[5:],),)
        data = str(result.fetchall()[0][0])
        
        if (roundT+1) % 100 == 0:
            ident = f"A{roundT+1}"
            cursor.execute("INSERT INTO Network_Values_Tournament VALUES (?, ?)",(ident,data))

        data = data.rsplit()
        data = [float(num) for num in data]

        for network in range(64):
            ident = f"W{network+1}"
            if ident == roundWinnerIdent[5:]:
                continue

            newData = []
            for num in data:
                diff = ((random.random() * 2) - 1) * learningRate
                endNum = round(num + diff, 4)
                newData.append(endNum)
                values = " ".join(str(num) for num in newData)
            cursor.execute("UPDATE Network_Values_Tournament SET data = ? WHERE id = ?",(values,ident))
            connection.commit()
        
        etR = time.time()
        print(f"Round {roundT+1} Updates Complete. Round Time = {etR - stR}")

    et = time.time()
    print(f"Tournament Complete: Duration = {et - st}")

def runMatch(ident1,ident2,length):
    """Helper Function for runTournament. returns winner, looser of a match of length "length" between networks "ident1" and "ident2"."""
    ident1Wins = 0
    ident2Wins = 0
    for game in range(length):
        winner, looser = runGame(ident1,ident2)
        ident1Wins = ident1Wins + 1 if winner == 1 else ident1Wins
        ident2Wins = ident2Wins + 1 if winner == 2 else ident2Wins
        if ident1Wins > (length / 2):
            return 1,2
        elif ident2Wins > (length / 2):
            return 2,1
    
    #If tied after "length" games, play tie-breaker:
    return runGame(ident1,ident2)


def runGame(ident1,ident2):
    """Helper Function for runTournament. returns winner, looser of a singe game between networks "ident1" and "ident2". """
    Board = Logic.Board()
    Board.setStartPositions()

    startingPlayer = random.randint(1,2)
    gameOver = False

    Turn = Logic.Turn(startingPlayer,"AI",None,First=True)
    Moves = AI.Silent_Main(Board,Turn,"Network",ident2 if Turn.player == 2 else ident1,"Network_Values_Tournament")
    Board.makeMoves(Moves,Turn.player)

    while not gameOver:
        Turn = Logic.Turn(1 if Turn.player == 2 else 2,"AI",None)
        Moves = AI.Silent_Main(Board,Turn,"Network",ident2 if Turn.player == 2 else ident1,"Network_Values_Tournament")
        Board.makeMoves(Moves,Turn.player)

        if Board.pip[1 if Turn.player == 2 else 0] == 0:
            gameOver = True
            looser = 1 if Turn.player == 2 else 1
            winner = Turn.player
    
    return winner, looser

runTournament(2000,0.05,7,True)