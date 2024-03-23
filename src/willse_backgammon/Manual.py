import multiprocessing
import random
import time

try:
    from Main_Files import AI as AI
    from Main_Files import Logic as Logic
except ModuleNotFoundError:
    from willse_backgammon.Main_Files import Logic as Logic
    from willse_backgammon.Main_Files import AI as AI

# Testing Functions:
def RunGame(ai_type1, ai_type2, net_ident1=None, netIdent2=None, PrintData=False, Silent=False):
    Board.setStartPositions()

    starting_player = random.randint(1, 2)
    game_over = False
    winner = 0
    turn_number = 1

    turn = Logic.Turn(starting_player, "AI", None, First=True)
    if not Silent:
        moves = AI.Main(Board, turn, ai_type2 if turn.player == 2 else ai_type1,
                        netIdent2 if turn.player == 2 else net_ident1)
    else:
        moves = AI.Silent_Main(Board, turn, ai_type2 if turn.player == 2 else ai_type1,
                               netIdent2 if turn.player == 2 else net_ident1)
    Board.makeMoves(moves, turn.player)

    while not game_over:

        turn = Logic.Turn(1 if turn.player == 2 else 2, "AI", None)
        turn_number = turn_number + 1
        if not Silent:
            moves = AI.Main(Board, turn, ai_type2 if turn.player == 2 else ai_type1,
                            netIdent2 if turn.player == 2 else net_ident1)
        else:
            moves = AI.Silent_Main(Board, turn, ai_type2 if turn.player == 2 else ai_type1,
                                   netIdent2 if turn.player == 2 else net_ident1)
        Board.makeMoves(moves, turn.player)

        if Board.pip[1 if turn.player == 2 else 0] == 0:
            game_over = True
            winner = turn.player

    if PrintData:
        print("/// Results ///")
        print(f"Winner = player {winner} // Number of Turns = {turn_number}")
        print(f"Final Scores: {Board.pip[0]} to {Board.pip[1]}")
        print("///////////////")

    return turn_number, winner


def RunGameMulti(args):
    AiType1, AiType2, netIdent1, netIdent2 = args

    Board.setStartPositions()

    startingPlayer = random.randint(1, 2)
    gameOver = False

    Turn = Logic.Turn(startingPlayer, "AI", None, First=True)
    Moves = AI.Silent_Main(Board, Turn, AiType2 if Turn.player == 2 else AiType1,
                           netIdent2 if Turn.player == 2 else netIdent1, True)
    Board.makeMoves(Moves, Turn.player)

    while not gameOver:

        Turn = Logic.Turn(1 if Turn.player == 2 else 2, "AI", None)
        Moves = AI.Silent_Main(Board, Turn, AiType2 if Turn.player == 2 else AiType1,
                               netIdent2 if Turn.player == 2 else netIdent1, True)
        Board.makeMoves(Moves, Turn.player)

        if Board.pip[1 if Turn.player == 2 else 0] == 0:
            gameOver = True
            winner = Turn.player

    print(f"Game Finished. Winner = {winner}")
    return winner


def RunGames(AiType1, AiType2, iterations, netIdent1=None, netIdent2=None, Silent=True):
    i = 0
    turns = []
    wins = [0, 0]

    st = time.time()
    while i < iterations:
        turnNum, winner = RunGame(AiType1, AiType2, netIdent1, netIdent2, Silent=Silent)
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


def RunGamesMulti(AiType1, AiType2, iterations, netIdent1=None, netIdent2=None, Silent=True):
    st = time.time()

    args = [(AiType1, AiType2, netIdent1, netIdent2)] * iterations

    with multiprocessing.Pool() as pool:
        results = pool.map(RunGameMulti, args)

    player1Wins = 0
    player2Wins = 0

    for result in results:
        if result == 1:
            player1Wins = player1Wins + 1
        else:
            player2Wins = player2Wins + 1

    et = time.time()
    elapsed_time = et - st

    print()
    print("##### Games Stats #####")
    print(f"    Player 1 = {AiType1} // Player 2 = {AiType2} // Ident1 = {netIdent1} // Ident2 = {netIdent2}")
    print(f"    Games Played = {iterations} // Elapsed Time = {elapsed_time}")
    print(f"    Player 1 Wins = {player1Wins} // Player 2 Wins = {player2Wins}")
    print("#######################")
    print()


def TestAIMoveUpdates(Board: Logic.Board, player, roll):
    Turn = Logic.Turn(player, "AI", None, roll=roll)
    Turn.updatePossibleMovesAI(Board, player)
    print(f"PossibleMoves = {Turn.current_possible_moves}")


Board = Logic.Board()

##### Current Test Code #####

if __name__ == "__main__":
    pass
    # RunGamesMulti("Network", "TS1", 1000, netIdent1="V1.0-NVT-A1-100", netIdent2="V1.0-NVT-A600")
