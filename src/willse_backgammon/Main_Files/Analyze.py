import sys
try:
    from Main_Files import AI as AI
    from AI_Agents import Network_Type2 as T2
    from Main_Files import Logic as Logic
    from NN_Tests import print_backgammon_board
except ModuleNotFoundError:
    from willse_backgammon.Main_Files import AI as AI
    from willse_backgammon.AI_Agents import Network_Type2 as T2
    from willse_backgammon.Main_Files import Logic as Logic
    from willse_backgammon.NN_Tests import print_backgammon_board

ROLLS = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),(5,5),(5,6),(6,6)]

def analyze(board:Logic.Board, turn:Logic.Turn, settings, nextPlayer):
    out_path = 'willse_backgammon/Logs/Active_Analyze.log'
    sys.stdout = open(out_path,'at')

    print("#############################################################")
    print("Analyze Results")
    print("")
    print("Input Board:")
    print_backgammon_board(board.positions)
    print("")
    print("")
    print("Current Analyze:")

    if nextPlayer == 1:
        if settings["Agent1"] == "Network":
            netID = settings["Network1 ID"]
            roll_results = []

            print(f"Valuation = {T2.Full_Run(board,turn,netID,analyse=True,noRoll=True)[0]}")
            print("")
            print("")
            print("Possible Roll Options:")

            for roll in ROLLS:
                print(f"Roll = {roll}")
                turn_sub = Logic.Turn(nextPlayer, "Network", roll=roll)
                turn_sub.updatePossibleMovesStandardFormat(board)
                chosen_moves, current_prediction, possible_moves = T2.Full_Run(board, turn_sub, netID, analyse=True)
                roll_results.append((roll, chosen_moves, current_prediction))
                for move in possible_moves:
                    print(f"Move Option: {move[0]} ----> {move[1]}")
                print("")

            print("Roll Summary:")
            for roll in roll_results:
                print(f"Roll: {roll[0]} ----> {roll[2].item()} (From {roll[1]})")

        else:
            print("Could not run analyze because no player 1 is not a neural network")
    if nextPlayer == 2:
        if settings["Agent2"] == "Network":
            netID = settings["Network2 ID"]
            roll_results = []

            print(f"Valuation = {T2.Full_Run(board,turn,netID,analyse=True,noRoll=True)[0]}")
            print("")
            print("")
            print("Possible Roll Options:")

            for roll in ROLLS:
                print(f"Roll = {roll}")
                turn_sub = Logic.Turn(nextPlayer, "Network", roll=roll)
                turn_sub.updatePossibleMovesStandardFormat(board)
                chosen_moves, current_prediction, possible_moves = T2.Full_Run(board, turn_sub, netID, analyse=True)
                roll_results.append((roll, chosen_moves, current_prediction))
                for move in possible_moves:
                    print(f"Move Option: {move[0]} ----> {move[1]}")
                print("")

            print("Roll Summary:")
            for roll in roll_results:
                print(f"Roll: {roll[0]} ----> {roll[2].item()} (From {roll[1]})")

        else:
            print("Could not run analyze because no player 2 is not a neural network")
    else:
        print("Could not run analyze because no player is set to move next.")

    print_backgammon_board(board.positions)

    print("#############################################################")
    sys.stdout = sys.__stdout__
