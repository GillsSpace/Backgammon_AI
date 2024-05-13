import random
import time

try:
    # from AI_Agents.Network_Type2 import FullRun as Network_Type2_Full_Run
    from AI_Agents.Network_Type1 import Full_Run as Network_Type1_Full_Run
    from AI_Agents.Pick_Best_Pip import Full_Run as PBP_Full_Run
    from AI_Agents.TreeSearchI import Full_Run as TreeSearchI_Full_Run
    from Main_Files.Logic import Board, Turn
except ModuleNotFoundError:
    # from willse_backgammon.AI_Agents.Network_Type2 import FullRun as Network_Type2_Full_Run
    from willse_backgammon.AI_Agents.Network_Type1 import Full_Run as Network_Type1_Full_Run
    from willse_backgammon.AI_Agents.Pick_Best_Pip import Full_Run as PBP_Full_Run
    from willse_backgammon.AI_Agents.TreeSearchI import Full_Run as TreeSearchI_Full_Run
    from willse_backgammon.Main_Files.Logic import Board, Turn

# Helper Classes:


# AI Types:
def randomMove(ActiveBoard: Board, ActiveTurn: Turn):
    ActiveTurn.updatePossibleMovesStandardFormat(ActiveBoard)
    if ActiveTurn.current_possible_moves != []:
        Moves = random.choice(ActiveTurn.current_possible_moves)
        return Moves
    else:
        return []


def pickBestPip(ActiveBoard: Board, ActiveTurn: Turn):
    return PBP_Full_Run(ActiveBoard, ActiveTurn)


def treeSearchI(ActiveBoard: Board, ActiveTurn: Turn, multiSuppression):
    return TreeSearchI_Full_Run(ActiveBoard, ActiveTurn, multiSuppression)


# Main Function - Called
def Main(Main_Board: Board, Main_Turn: Turn, aiType, networkIdent=None, multiSuppression=False):
    AI_player = aiType
    if AI_player == "Random":
        print(f"Running Random Move Selection; Roll = {Main_Turn.roll}")
        st = time.time()
        Moves = randomMove(Main_Board, Main_Turn)
        et = time.time()
        print(f"Finished Run; Elapsed Time = {et - st}; Final Move Set = {Moves}")
        return Moves
    elif AI_player in ["Tree Search I", "TS 1", "TS1"]:
        print(f"Running Tree Search I; Roll = {Main_Turn.roll}")
        st = time.time()
        Moves = treeSearchI(Main_Board, Main_Turn, multiSuppression)
        et = time.time()
        print(f"Finished Run; Elapsed Time = {et - st}; Final Move Set = {Moves}")
        return Moves
    elif AI_player == "PBP":
        print(f"Running PBP; Roll = {Main_Turn.roll}")
        st = time.time()
        Moves = pickBestPip(Main_Board, Main_Turn)
        et = time.time()
        print(f"Finished Run; Elapsed Time = {et - st}; Final Move Set = {Moves}")
        return Moves
    elif AI_player == "Network":
        print(f"Running Network Selection, ID = {networkIdent}; Roll = {Main_Turn.roll}")
        st = time.time()
        if networkIdent[0:5] == "V1.0-":
            Moves = Network_Type1_Full_Run(Main_Board, Main_Turn, networkIdent)
        elif networkIdent[0:5] == "V2.0-":
            # Moves = Network_Type2_Full_Run(Main_Board, Main_Turn, networkIdent)
            Moves = []
        else:
            print("Error: Network Ident Not Valid (Type)")
            Moves = []
        et = time.time()
        print(f"Finished Run; Elapsed Time = {et - st}; Final Move Set = {Moves}")
        return Moves


def Silent_Main(Main_Board: Board, Main_Turn: Turn, aiType, networkIdent=None, multiSuppression=False):
    AI_player = aiType
    if AI_player == "Random":
        Moves = randomMove(Main_Board, Main_Turn)
        return Moves
    elif AI_player in ["Tree Search I", "TS 1", "TS1"]:
        Moves = treeSearchI(Main_Board, Main_Turn, multiSuppression)
        return Moves
    elif AI_player == "PBP":
        Moves = pickBestPip(Main_Board, Main_Turn)
        return Moves
    elif AI_player == "Network":
        if networkIdent[0:5] == "V1.0-":
            Moves = Network_Type1_Full_Run(Main_Board, Main_Turn, networkIdent)
        elif networkIdent[0:5] == "V2.0-":
            Moves = []
        else:
            print("Error: Network Ident Not Valid (Type)")
            Moves = []
        return Moves
