import copy, random, sqlite3, time, csv, ast, torch
import numpy as np
import pandas as pd
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import matplotlib.pyplot as plt

try:
    from Main_Files import AI as AI
    from Main_Files.Logic import Board, Turn
    from AI_Agents.Network_Type2 import BackgammonNN, BackgammonNN_v3
    from Manual import RunGames
except ModuleNotFoundError:
    from willse_backgammon.Main_Files.Logic import Board, Turn
    from willse_backgammon.Main_Files import AI as AI
    from willse_backgammon.AI_Agents.Network_Type2 import BackgammonNN, BackgammonNN_v3
    from willse_backgammon.Manual import RunGames

# Code:
def print_backgammon_board(positions):

    a1 = "  O " if positions[0] > 0 else "  X " if positions[0] < 0 else "    "
    a2 = "  O " if positions[1] > 0 else "  X " if positions[1] < 0 else "    "
    a3 = "  O " if positions[2] > 0 else "  X " if positions[2] < 0 else "    "
    a4 = "  O " if positions[3] > 0 else "  X " if positions[3] < 0 else "    "
    a5 = "  O " if positions[4] > 0 else "  X " if positions[4] < 0 else "    "
    a6 = "  O " if positions[5] > 0 else "  X " if positions[5] < 0 else "    "
    a7 = "  O " if positions[6] > 0 else "  X " if positions[6] < 0 else "    "
    a8 = "  O " if positions[7] > 0 else "  X " if positions[7] < 0 else "    "
    a9 = "  O " if positions[8] > 0 else "  X " if positions[8] < 0 else "    "
    aa = "  O " if positions[9] > 0 else "  X " if positions[9] < 0 else "    "
    ab = "  O " if positions[10]> 0 else "  X " if positions[10]< 0 else "    "
    ac = "  O " if positions[11]> 0 else "  X " if positions[11]< 0 else "    "
    b1 = "  O " if positions[0] > 1 else "  X " if positions[0] < -1 else "    "
    b2 = "  O " if positions[1] > 1 else "  X " if positions[1] < -1 else "    "
    b3 = "  O " if positions[2] > 1 else "  X " if positions[2] < -1 else "    "
    b4 = "  O " if positions[3] > 1 else "  X " if positions[3] < -1 else "    "
    b5 = "  O " if positions[4] > 1 else "  X " if positions[4] < -1 else "    "
    b6 = "  O " if positions[5] > 1 else "  X " if positions[5] < -1 else "    "
    b7 = "  O " if positions[6] > 1 else "  X " if positions[6] < -1 else "    "
    b8 = "  O " if positions[7] > 1 else "  X " if positions[7] < -1 else "    "
    b9 = "  O " if positions[8] > 1 else "  X " if positions[8] < -1 else "    "
    ba = "  O " if positions[9] > 1 else "  X " if positions[9] < -1 else "    "
    bb = "  O " if positions[10]> 1 else "  X " if positions[10]< -1 else "    "
    bc = "  O " if positions[11]> 1 else "  X " if positions[11]< -1 else "    "
    c1 = "  O " if positions[0] > 2 else "  X " if positions[0] < -2 else "    "
    c2 = "  O " if positions[1] > 2 else "  X " if positions[1] < -2 else "    "
    c3 = "  O " if positions[2] > 2 else "  X " if positions[2] < -2 else "    "
    c4 = "  O " if positions[3] > 2 else "  X " if positions[3] < -2 else "    "
    c5 = "  O " if positions[4] > 2 else "  X " if positions[4] < -2 else "    "
    c6 = "  O " if positions[5] > 2 else "  X " if positions[5] < -2 else "    "
    c7 = "  O " if positions[6] > 2 else "  X " if positions[6] < -2 else "    "
    c8 = "  O " if positions[7] > 2 else "  X " if positions[7] < -2 else "    "
    c9 = "  O " if positions[8] > 2 else "  X " if positions[8] < -2 else "    "
    ca = "  O " if positions[9] > 2 else "  X " if positions[9] < -2 else "    "
    cb = "  O " if positions[10]> 2 else "  X " if positions[10]< -2 else "    "
    cc = "  O " if positions[11]> 2 else "  X " if positions[11]< -2 else "    "
    d1 = "  O " if positions[0] > 3 else "  X " if positions[0] < -3 else "    "
    d2 = "  O " if positions[1] > 3 else "  X " if positions[1] < -3 else "    "
    d3 = "  O " if positions[2] > 3 else "  X " if positions[2] < -3 else "    "
    d4 = "  O " if positions[3] > 3 else "  X " if positions[3] < -3 else "    "
    d5 = "  O " if positions[4] > 3 else "  X " if positions[4] < -3 else "    "
    d6 = "  O " if positions[5] > 3 else "  X " if positions[5] < -3 else "    "
    d7 = "  O " if positions[6] > 3 else "  X " if positions[6] < -3 else "    "
    d8 = "  O " if positions[7] > 3 else "  X " if positions[7] < -3 else "    "
    d9 = "  O " if positions[8] > 3 else "  X " if positions[8] < -3 else "    "
    da = "  O " if positions[9] > 3 else "  X " if positions[9] < -3 else "    "
    db = "  O " if positions[10]> 3 else "  X " if positions[10]< -3 else "    "
    dc = "  O " if positions[11]> 3 else "  X " if positions[11]< -3 else "    "
    e1 = "  O " if positions[0] > 4 else "  X " if positions[0] < -4 else "    "
    e2 = "  O " if positions[1] > 4 else "  X " if positions[1] < -4 else "    "
    e3 = "  O " if positions[2] > 4 else "  X " if positions[2] < -4 else "    "
    e4 = "  O " if positions[3] > 4 else "  X " if positions[3] < -4 else "    "
    e5 = "  O " if positions[4] > 4 else "  X " if positions[4] < -4 else "    "
    e6 = "  O " if positions[5] > 4 else "  X " if positions[5] < -4 else "    "
    e7 = "  O " if positions[6] > 4 else "  X " if positions[6] < -4 else "    "
    e8 = "  O " if positions[7] > 4 else "  X " if positions[7] < -4 else "    "
    e9 = "  O " if positions[8] > 4 else "  X " if positions[8] < -4 else "    "
    ea = "  O " if positions[9] > 4 else "  X " if positions[9] < -4 else "    "
    eb = "  O " if positions[10]> 4 else "  X " if positions[10]< -4 else "    "
    ec = "  O " if positions[11]> 4 else "  X " if positions[11]< -4 else "    "
    f1 = "  + " if positions[0] > 5 else "  + " if positions[0] < -5 else "    "
    f2 = "  + " if positions[1] > 5 else "  + " if positions[1] < -5 else "    "
    f3 = "  + " if positions[2] > 5 else "  + " if positions[2] < -5 else "    "
    f4 = "  + " if positions[3] > 5 else "  + " if positions[3] < -5 else "    "
    f5 = "  + " if positions[4] > 5 else "  + " if positions[4] < -5 else "    "
    f6 = "  + " if positions[5] > 5 else "  + " if positions[5] < -5 else "    "
    f7 = "  + " if positions[6] > 5 else "  + " if positions[6] < -5 else "    "
    f8 = "  + " if positions[7] > 5 else "  + " if positions[7] < -5 else "    "
    f9 = "  + " if positions[8] > 5 else "  + " if positions[8] < -5 else "    "
    fa = "  + " if positions[9] > 5 else "  + " if positions[9] < -5 else "    "
    fb = "  + " if positions[10]> 5 else "  + " if positions[10]< -5 else "    "
    fc = "  + " if positions[11]> 5 else "  + " if positions[11]< -5 else "    "

    g1 = "  + " if positions[23] > 5 else "  + " if positions[23] < -5 else "    "
    g2 = "  + " if positions[22] > 5 else "  + " if positions[22] < -5 else "    "
    g3 = "  + " if positions[21] > 5 else "  + " if positions[21] < -5 else "    "
    g4 = "  + " if positions[20] > 5 else "  + " if positions[20] < -5 else "    "
    g5 = "  + " if positions[19] > 5 else "  + " if positions[19] < -5 else "    "
    g6 = "  + " if positions[18] > 5 else "  + " if positions[18] < -5 else "    "
    g7 = "  + " if positions[17] > 5 else "  + " if positions[17] < -5 else "    "
    g8 = "  + " if positions[16] > 5 else "  + " if positions[16] < -5 else "    "
    g9 = "  + " if positions[15] > 5 else "  + " if positions[15] < -5 else "    "
    ga = "  + " if positions[14] > 5 else "  + " if positions[14] < -5 else "    "
    gb = "  + " if positions[13] > 5 else "  + " if positions[13] < -5 else "    "
    gc = "  + " if positions[12] > 5 else "  + " if positions[12] < -5 else "    "
    h1 = "  O " if positions[23] > 4 else "  X " if positions[23] < -4 else "    "
    h2 = "  O " if positions[22] > 4 else "  X " if positions[22] < -4 else "    "
    h3 = "  O " if positions[21] > 4 else "  X " if positions[21] < -4 else "    "
    h4 = "  O " if positions[20] > 4 else "  X " if positions[20] < -4 else "    "
    h5 = "  O " if positions[19] > 4 else "  X " if positions[19] < -4 else "    "
    h6 = "  O " if positions[18] > 4 else "  X " if positions[18] < -4 else "    "
    h7 = "  O " if positions[17] > 4 else "  X " if positions[17] < -4 else "    "
    h8 = "  O " if positions[16] > 4 else "  X " if positions[16] < -4 else "    "
    h9 = "  O " if positions[15] > 4 else "  X " if positions[15] < -4 else "    "
    ha = "  O " if positions[14] > 4 else "  X " if positions[14] < -4 else "    "
    hb = "  O " if positions[13] > 4 else "  X " if positions[13] < -4 else "    "
    hc = "  O " if positions[12] > 4 else "  X " if positions[12] < -4 else "    "
    i1 = "  O " if positions[23] > 3 else "  X " if positions[23] < -3 else "    "
    i2 = "  O " if positions[22] > 3 else "  X " if positions[22] < -3 else "    "
    i3 = "  O " if positions[21] > 3 else "  X " if positions[21] < -3 else "    "
    i4 = "  O " if positions[20] > 3 else "  X " if positions[20] < -3 else "    "
    i5 = "  O " if positions[19] > 3 else "  X " if positions[19] < -3 else "    "
    i6 = "  O " if positions[18] > 3 else "  X " if positions[18] < -3 else "    "
    i7 = "  O " if positions[17] > 3 else "  X " if positions[17] < -3 else "    "
    i8 = "  O " if positions[16] > 3 else "  X " if positions[16] < -3 else "    "
    i9 = "  O " if positions[15] > 3 else "  X " if positions[15] < -3 else "    "
    ia = "  O " if positions[14] > 3 else "  X " if positions[14] < -3 else "    "
    ib = "  O " if positions[13] > 3 else "  X " if positions[13] < -3 else "    "
    ic = "  O " if positions[12] > 3 else "  X " if positions[12] < -3 else "    "
    j1 = "  O " if positions[23] > 2 else "  X " if positions[23] < -2 else "    "
    j2 = "  O " if positions[22] > 2 else "  X " if positions[22] < -2 else "    "
    j3 = "  O " if positions[21] > 2 else "  X " if positions[21] < -2 else "    "
    j4 = "  O " if positions[20] > 2 else "  X " if positions[20] < -2 else "    "
    j5 = "  O " if positions[19] > 2 else "  X " if positions[19] < -2 else "    "
    j6 = "  O " if positions[18] > 2 else "  X " if positions[18] < -2 else "    "
    j7 = "  O " if positions[17] > 2 else "  X " if positions[17] < -2 else "    "
    j8 = "  O " if positions[16] > 2 else "  X " if positions[16] < -2 else "    "
    j9 = "  O " if positions[15] > 2 else "  X " if positions[15] < -2 else "    "
    ja = "  O " if positions[14] > 2 else "  X " if positions[14] < -2 else "    "
    jb = "  O " if positions[13] > 2 else "  X " if positions[13] < -2 else "    "
    jc = "  O " if positions[12] > 2 else "  X " if positions[12] < -2 else "    "
    k1 = "  O " if positions[23] > 1 else "  X " if positions[23] < -1 else "    "
    k2 = "  O " if positions[22] > 1 else "  X " if positions[22] < -1 else "    "
    k3 = "  O " if positions[21] > 1 else "  X " if positions[21] < -1 else "    "
    k4 = "  O " if positions[20] > 1 else "  X " if positions[20] < -1 else "    "
    k5 = "  O " if positions[19] > 1 else "  X " if positions[19] < -1 else "    "
    k6 = "  O " if positions[18] > 1 else "  X " if positions[18] < -1 else "    "
    k7 = "  O " if positions[17] > 1 else "  X " if positions[17] < -1 else "    "
    k8 = "  O " if positions[16] > 1 else "  X " if positions[16] < -1 else "    "
    k9 = "  O " if positions[15] > 1 else "  X " if positions[15] < -1 else "    "
    ka = "  O " if positions[14] > 1 else "  X " if positions[14] < -1 else "    "
    kb = "  O " if positions[13] > 1 else "  X " if positions[13] < -1 else "    "
    kc = "  O " if positions[12] > 1 else "  X " if positions[12] < -1 else "    "
    l1 = "  O " if positions[23] > 0 else "  X " if positions[23] < 0 else "    "
    l2 = "  O " if positions[22] > 0 else "  X " if positions[22] < 0 else "    "
    l3 = "  O " if positions[21] > 0 else "  X " if positions[21] < 0 else "    "
    l4 = "  O " if positions[20] > 0 else "  X " if positions[20] < 0 else "    "
    l5 = "  O " if positions[19] > 0 else "  X " if positions[19] < 0 else "    "
    l6 = "  O " if positions[18] > 0 else "  X " if positions[18] < 0 else "    "
    l7 = "  O " if positions[17] > 0 else "  X " if positions[17] < 0 else "    "
    l8 = "  O " if positions[16] > 0 else "  X " if positions[16] < 0 else "    "
    l9 = "  O " if positions[15] > 0 else "  X " if positions[15] < 0 else "    "
    la = "  O " if positions[14] > 0 else "  X " if positions[14] < 0 else "    "
    lb = "  O " if positions[13] > 0 else "  X " if positions[13] < 0 else "    "
    lc = "  O " if positions[12] > 0 else "  X " if positions[12] < 0 else "    "

    z1 = f"{positions[24] : 03d} "
    z2 = f"{positions[25] : 03d} "
    z3 = f"{positions[26] : 03d} "
    z4 = f"{positions[27] : 03d} "


    print(f"|    | 01   02   03   04   05   06 |    | 07   08   09   10   11   12 |    |")
    print(f"|----|----+----+----+----+----+----|----|----+----+----+----+----+----|----|")
    print(f"|{z4}|{a1} {a2} {a3} {a4} {a5} {a6}|    |{a7} {a8} {a9} {aa} {ab} {ac}|    |")
    print(f"|    |{b1} {b2} {b3} {b4} {b5} {b6}|    |{b7} {b8} {b9} {ba} {bb} {bc}|    |")
    print(f"|    |{c1} {c2} {c3} {c4} {c5} {c6}|    |{c7} {c8} {c9} {ca} {cb} {cc}|    |")
    print(f"|    |{d1} {d2} {d3} {d4} {d5} {d6}| O  |{d7} {d8} {d9} {da} {db} {dc}|    |")
    print(f"|    |{e1} {e2} {e3} {e4} {e5} {e6}|{z2}|{e7} {e8} {e9} {ea} {eb} {ec}|    |")
    print(f"|    |{f1} {f2} {f3} {f4} {f5} {f6}|    |{f7} {f8} {f9} {fa} {fb} {fc}|    |")
    print(f"|----|                             |    |                             |----|")
    print(f"|    |{g1} {g2} {g3} {g4} {g5} {g6}|    |{g7} {g8} {g9} {ga} {gb} {gc}|    |")
    print(f"|    |{h1} {h2} {h3} {h4} {h5} {h6}|{z1}|{h7} {h8} {h9} {ha} {hb} {hc}|    |")
    print(f"|    |{i1} {i2} {i3} {i4} {i5} {i6}| X  |{i7} {i8} {i9} {ia} {ib} {ic}|    |")
    print(f"|    |{j1} {j2} {j3} {j4} {j5} {j6}|    |{j7} {j8} {j9} {ja} {jb} {jc}|    |")
    print(f"|    |{k1} {k2} {k3} {k4} {k5} {k6}|    |{k7} {k8} {k9} {ka} {kb} {kc}|    |")
    print(f"|{z3}|{l1} {l2} {l3} {l4} {l5} {l6}|    |{l7} {l8} {l9} {la} {lb} {lc}|    |")
    print(f"|----|----+----+----+----+----+----|----|----+----+----+----+----+----|----|")
    print(f"|    | 24   23   22   21   20   19 |    | 18   17   16   15   14   13 |    |")

def single_training_game_verbose(model, lambda_=0.8, alpha=0.01):

    #Debugging info:
    player_symbols = ["X","0"]
    print(f"Starting Training Run...")
    print("Initial Parameters")
    for name, param in model.named_parameters():
        print(f"Name: {name}")
        print(param)

    initial_params = {name:torch.clone(param) for name,param in model.named_parameters()}

    model.episode_reset()

    # Initialize board and game variables:
    board = Board()
    board.setStartPositions()
    current_player = random.randint(1,2)
    game_over = False

    print("------------------------------------------------------------------------------------------")
    print("Starting Turn...")
    print(f"Player: {current_player} ({player_symbols[current_player-1]})")
    print_backgammon_board(board.positions)

    # Initialize first turn
    turn = Turn(current_player,"AI",First=True)
    turn.updatePossibleMovesStandardFormat(board)

    # Generate and make moves
    chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player,True)

    # Debug Info:
    print(f"Roll: {turn.roll} // Move To Play: {chosen_moves}")
    print(f"Valuation:          {current_prediction}")
    print(f"Previous Valuation: {model.last_prediction}")

    print("------------------------------------------------------------------------------------------")

    board.makeMoves(chosen_moves,current_player)
    current_player = 2 if current_player == 1 else 1
    model.last_prediction = current_prediction

    while not game_over:

        print("------------------------------------------------------------------------------------------")
        print("Starting Turn...")
        print(f"Player: {current_player} ({player_symbols[current_player-1]})")
        print_backgammon_board(board.positions)

        # Initialize turn
        turn = Turn(current_player,"AI")
        turn.updatePossibleMovesStandardFormat(board)

        # Generate and prediction:
        chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player,True)

        td_error:torch.Tensor = (current_prediction.detach() - model.last_prediction)

        td_error.backward()
        model.update_eligibility_traces(lambda_)

        for name, param in model.named_parameters():
            trace = model.traces[name]
            param.data -= alpha * td_error * trace.data

        # Debug Info:
        print(f"Roll: {turn.roll} // Move To Play: {chosen_moves}")
        print(f"Valuation:          {current_prediction}")
        print(f"Previous Valuation: {model.last_prediction}")
        print(f"TD_error:           {td_error}")

        print("------------------------------------------------------------------------------------------")

        board.makeMoves(chosen_moves,current_player)

        # Checks if game is over and transitions to new turn
        game_over = True if board.pip[current_player-1] == 0 else False
        current_player = 2 if current_player == 1 else 1

        model.last_prediction = current_prediction
        model.zero_grad()

    print("------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------")
    print("Final Update:")
    print(f"Winner = {1 if current_player == 2 else 2}")
    print("Final Board:")
    print_backgammon_board(board.positions)

    reward = torch.zeros(1).to(DEVICE) if current_player == 1 else torch.ones(1).to(DEVICE)
    td_error:torch.Tensor = (reward.detach() - model.last_prediction)

    td_error.backward()
    model.update_eligibility_traces(lambda_)

    for name, param in model.named_parameters():
        trace = model.traces[name]
        param.data -= alpha * td_error * trace.data

    print(f"Reward:             {reward}")
    print(f"Previous Valuation: {model.last_prediction}")
    print(f"TD_error:           {td_error}")

    print("Final Parameters")
    for name, param in model.named_parameters():
        print(f"Name: {name}")
        print(param)

    delta_params = {name:initial_params.get(name) - param_i for name,param_i in model.named_parameters()}

    print("Change in Parameters")
    for name, param in delta_params.items():
        print(f"Name: {name}")
        print(param)

    print("------------------------------------------------------------------------------------------")
    
def single_training_game_subprocess(model, lambda_=0.8, alpha=0.01):

    # Resets trace and previous prediction variables:
    model.episode_reset()
    
    # Initialize board and game variables:
    board = Board()
    board.setStartPositions()
    current_player = random.randint(1,2)
    game_over = False

    # Initialize first turn
    turn = Turn(current_player,"AI",First=True)
    turn.updatePossibleMovesStandardFormat(board)

    # Generate and make moves
    chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player)
    board.makeMoves(chosen_moves,current_player)

    # Transitions to next state and player:
    current_player = 2 if current_player == 1 else 1
    model.last_prediction = current_prediction

    while not game_over:
        # Initialize turn
        turn = Turn(current_player,"AI")
        turn.updatePossibleMovesStandardFormat(board)

        # Generates move and prediction:
        chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player)

        # Calculates error and eligibility traces:
        td_error = (current_prediction.detach() - model.last_prediction)
        td_error.backward()
        model.update_eligibility_traces(lambda_)

        # Updates parameters:
        for name, param in model.named_parameters():
            trace = model.traces[name]
            param.data -= alpha * td_error * trace.data

        # Makes a move, checks if game is over, and transitions to new turn:
        board.makeMoves(chosen_moves,current_player)
        game_over = True if board.pip[current_player-1] == 0 else False
        current_player = 2 if current_player == 1 else 1
        model.last_prediction = current_prediction
        model.zero_grad()

    # Performs final update using actual reward:
    reward = torch.zeros(1).to(DEVICE) if current_player == 1 else torch.ones(1).to(DEVICE) # current_player = loser
    td_error = reward.detach() - model.last_prediction
    td_error.backward()
    model.update_eligibility_traces(lambda_)

    for name, param in model.named_parameters():
        trace = model.traces[name]
        param.data -= alpha * td_error * trace.data

def single_exhibition_game_verbose(model,opponent="TS1") -> int:

    player_symbols = ["X","0"]
    print(f"Starting Exhibition Game...")

    # Initialize board and game variables:
    board = Board()
    board.setStartPositions()
    current_player = random.randint(1,2)
    game_over = False

    if current_player == 1:
        print("------------------------------------------------------------------------------------------")
        print("Starting Turn...")
        print(f"Player: {current_player} ({player_symbols[current_player-1]})")
        print_backgammon_board(board.positions)

        # Initialize first turn
        turn = Turn(current_player,"AI",First=True)
        turn.updatePossibleMovesStandardFormat(board)

        # Generate and make moves
        chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player,True)

        # Debug Info:
        print(f"Roll: {turn.roll} // Move To Play: {chosen_moves}")
        print(f"Valuation:          {current_prediction}")
        print(f"Previous Valuation: {model.last_prediction}")

        print("------------------------------------------------------------------------------------------")

        board.makeMoves(chosen_moves,current_player)
        current_player = 2 if current_player == 1 else 1
        model.last_prediction = current_prediction
    else:
        print("------------------------------------------------------------------------------------------")
        print("Starting Turn...")
        print(f"Player: {current_player} ({player_symbols[current_player-1]})")
        print_backgammon_board(board.positions)

        # Initialize first turn
        turn = Turn(current_player,"AI",First=True)
        turn.updatePossibleMovesStandardFormat(board)

        # Generate and make moves
        chosen_moves = AI.Main(board,turn,"TS1")
        _, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player,True)

        # Debug Info:
        print(f"Roll: {turn.roll} // Move To Play: {chosen_moves}")

        print("------------------------------------------------------------------------------------------")

        board.makeMoves(chosen_moves,current_player)
        current_player = 2 if current_player == 1 else 1
        model.last_prediction = current_prediction

    while not game_over:

        if current_player == 1:
            print("------------------------------------------------------------------------------------------")
            print("Starting Turn...")
            print(f"Player: {current_player} ({player_symbols[current_player-1]})")
            print_backgammon_board(board.positions)

            # Initialize turn
            turn = Turn(current_player,"AI")
            turn.updatePossibleMovesStandardFormat(board)

            # Generate and prediction:
            chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player,True)
            to_be_next_prediction = torch.clone(current_prediction)
            current_prediction.detach()

            td_error = current_prediction - model.last_prediction

            # Debug Info:
            print(f"Roll: {turn.roll} // Move To Play: {chosen_moves}")
            print(f"Valuation:          {current_prediction}")
            print(f"Previous Valuation: {model.last_prediction}")
            print(f"TD_error:           {td_error}")

            print("------------------------------------------------------------------------------------------")

            board.makeMoves(chosen_moves,current_player)

            # Checks if game is over and transitions to new turn
            game_over = True if board.pip[current_player-1] == 0 else False
            current_player = 2 if current_player == 1 else 1

            model.last_prediction = to_be_next_prediction
        
        else:
            print("------------------------------------------------------------------------------------------")
            print("Starting Turn...")
            print(f"Player: {current_player} ({player_symbols[current_player-1]})")
            print_backgammon_board(board.positions)

            # Initialize turn
            turn = Turn(current_player,"AI")
            turn.updatePossibleMovesStandardFormat(board)

            # Generate and prediction:
            chosen_moves = AI.Main(board,turn,"TS1")

            # Debug Info:
            print(f"Roll: {turn.roll} // Move To Play: {chosen_moves}")

            print("------------------------------------------------------------------------------------------")

            board.makeMoves(chosen_moves,current_player)

            # Checks if game is over and transitions to new turn
            game_over = True if board.pip[current_player-1] == 0 else False
            current_player = 2 if current_player == 1 else 1

    print("------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------")

    winner = 1 if current_player == 2 else 2

    print("Final Update:")
    print(f"Winner = {winner}")
    print("Final Board:")
    print_backgammon_board(board.positions)

    reward = torch.zeros(1).to(DEVICE) if winner == 2 else torch.ones(1).to(DEVICE)
    td_error = reward - model.last_prediction

    print(f"Reward:             {reward}")
    print(f"Previous Valuation: {model.last_prediction}")

    return winner

def train_vs_ts1(model, lambda_=0.8, alpha=0.01):
    pass

def main(model_id, trace_decay_rate=0.7, learning_rate=0.001, seed_num=143728):

    torch.manual_seed(seed_num)
    random.seed(seed_num)
    torch.autograd.set_detect_anomaly(True)

    # Creates a temporary log file for debugging
    import sys
    out_path = 'willse_backgammon/AI_Agents/Data_Sets/Logs/output_' + model_id + '.txt'
    sys.stdout = open(out_path,'wt')

    # Model Id: 00-0000-0000 (Network Version, Flags, Id)
    model = BackgammonNN_v3().to(DEVICE)
    path = ""
    net_id = model_id[0:2]

    if net_id == "01":
        path = "willse_backgammon/AI_Agents/Saved_NNs/" + model_id + ".pt"
        try: 
            model.load_state_dict(torch.load(path))
        except:
            try:
                open(path,"r")
            except:
                open(path,"x")
    if net_id == "03":
        path = "willse_backgammon/AI_Agents/Saved_NNs/" + model_id + ".pt"
        try: 
            model.load_state_dict(torch.load(path))
        except:
            try:
                open(path,"r")
            except:
                open(path,"x")


    st = time.time()

    print("#############################################")
    print("#")
    print(f"#   Simulation Run 001: Testing new board representation")
    print(f"#   Model: {model_id} (Seed = {seed_num})")
    print(f"#   Trace Decay Rate: {trace_decay_rate}, Learning Rate: {learning_rate}")
    print(f"#   Notes: trying lower decay rate with higher learning rate")
    print("#")
    print("#############################################")

    single_training_game_verbose(model,trace_decay_rate,learning_rate)

    for k in range(10):

        for i in range(10):
            print(f"Starting Game {(k*100)+(i+1)}...")
            single_training_game_subprocess(model,trace_decay_rate,learning_rate)

        print("#############################################")
        print("#")
        print(f"#   Test Game: {k+1}")
        print("#")
        print("#############################################")
        single_training_game_verbose(model,trace_decay_rate,learning_rate)

        print("#############################################")
        print("#")
        print(f"#   Match Game (vs. TS1): {k+1}")
        print("#")
        print("#############################################")
        single_exhibition_game_verbose(model)

        torch.save(model.state_dict(),path)


    et = time.time()

    print(f"Total elapsed time: {et-st}")

if __name__ == "__main__":
    DEVICE = "cpu"
    # DEVICE = ("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    main("03-0000-0001",0.9,0.01)