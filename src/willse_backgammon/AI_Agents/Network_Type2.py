import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import random, copy

try:
    from Main_Files.Logic import Board,Turn
except:
    from willse_backgammon.Main_Files.Logic import Board,Turn

DEVICE = "cpu"
# DEVICE = ("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

#Creating Network:
class BackgammonNN(nn.Module):
    def __init__(self):
        super(BackgammonNN, self).__init__()
        # Define the layers of the network
        # Input = probability of P1(dark) winning from any given board position
        self.forward_pass = nn.Sequential(
            nn.Linear(29,64),
            nn.ReLU(),
            nn.Linear(64,64),
            nn.ReLU(),
            nn.Linear(64,1),
            nn.Sigmoid()
        )

        # Define Traces and Last Prediction:
        self.traces = {name: torch.zeros_like(param) for name, param in self.named_parameters()}
        self.last_prediction = None

    def forward(self, x):
        return self.forward_pass(x)
    
    def forward_on_board(self,input_board:Board, next_to_move_on_board:int):
        X = torch.tensor(input_board.positions[:] + [next_to_move_on_board],dtype=torch.float32).to(DEVICE)
        y = self.forward_pass(X)
        return y
    
    def chose_move(self,base_board:Board,possible_moves,player,verbose=False):
        moveValues = []
        output = None
        # Evaluate all posable moves and identify predicted odd of winning:
        for moveSet in possible_moves:
            testBoard = copy.deepcopy(base_board)
            testBoard.makeMoves(moveSet,player)
            output = self.forward_on_board(testBoard,2 if player == 1 else 1)
            moveValues.append(output)
            #moveValues.append(output if player == 1 else 1-output)



            if verbose:
                print(f"Move Option: {moveSet} ----> {output[0]}")

        # If no possible moves return empty move and valuation for current board (same as next board):
        if len(moveValues) == 0:
            return [], self.forward_on_board(base_board,2 if player == 1 else 1)

        # Select move using greedy algorithm:
        # maxValue = max(moveValues)
        # indexOfMove = moveValues.index(maxValue)
        
        if player == 2:
            val = max(moveValues)
            indexOfMove = moveValues.index(val)
        elif player == 1:
            val = min(moveValues)
            indexOfMove = moveValues.index(val)
        else:
            raise AttributeError

        finalMoveSelection = possible_moves[indexOfMove]

        return finalMoveSelection, val

    def calc_error(self,current_prediction,previous_prediction):
        td_error = (current_prediction - previous_prediction)
        td_error.backward()
        return td_error

    def update_eligibility_traces(self, lambda_):
    # Before calling this function, ensure that backward() has been called on the loss
        for (name, param), trace in zip(self.named_parameters(), self.traces.values()):
            trace.data = param.grad.data + lambda_ * trace.data.to(DEVICE)
        
    def episode_reset(self):
        self.traces = {name: torch.zeros_like(param) for name, param in self.named_parameters()}
        self.last_prediction = None


class BackgammonNN_v2(nn.Module):
    def __init__(self):
        super(BackgammonNN_v2, self).__init__()
        # Define the layers of the network
        # Output = [(prob. of p1 gammon), (prob. of p1 win), (prob. of p2 win), (prob. of p2 gammon)]
        self.forward_pass = nn.Sequential(
            nn.Linear(198,64),
            nn.ReLU(),
            nn.Linear(64,64),
            nn.ReLU(),
            nn.Linear(64,4),
            nn.Sigmoid(),
            nn.Softmax()
        )

        # Define Traces and Last Prediction:
        self.traces = {name: torch.zeros_like(param) for name, param in self.named_parameters()}
        self.last_prediction = None

    def forward(self, x):
        return self.forward_pass(x)
    
    def forward_on_board(self,input_board:Board, next_to_move_on_board:int):
        X = []

        for i in range(24):
            men = input_board.positions[i]
            if men == 0:
                j = [0,0,0,0,0,0,0,0]
            elif men == -1:
                j = [1,0,0,0,0,0,0,0]
            elif men == 1:
                j = [0,0,0,0,1,0,0,0]
            elif men == -2:
                j = [1,1,0,0,0,0,0,0]
            elif men == 2:
                j = [0,0,0,0,1,1,0,0]
            elif men <= -3:
                j = [1,1,1,((-men)-3)/2,0,0,0,0]
            elif men >= 3:
                j = [0,0,0,0,1,1,1,(men-3)/2]
            X += j
        if next_to_move_on_board == 1:
            X += [1,0]
        else:
            X += [0,1]
        X += [input_board.positions[24]/2,input_board.positions[25]/2]
        X += [input_board.positions[26],input_board.positions[27]]

        X = torch.tensor(X,dtype=torch.float32).to(DEVICE)
        y = self.forward_pass(X)
        return y
    
    def chose_move(self,base_board:Board,possible_moves,player,verbose=False):
        moveValues = []
        output = None
        # Evaluate all posable moves and identify predicted value (2 = player 1 gammon, 1 = player 1 win, -1 = player 2 win, -2 = player 2 win):
        for moveSet in possible_moves:
            testBoard = copy.deepcopy(base_board)
            testBoard.makeMoves(moveSet,player)
            output = self.forward_on_board(testBoard,2 if player == 1 else 1)
            (p1, p2, p3, p4) = (output[0],output[1],output[2],output[3])
            moveValues.append((2*p1) + p2 - p3 - (2*p4)) #Expected Return for player 1
            if verbose:
                print(f"Move Option: {moveSet} ----> {(output[0].item(),output[1].item(),output[2].item(),output[3].item())}")

        # If no possible moves return empty move and valuation for current board (same as next board):
        if len(moveValues) == 0:
            output = self.forward_on_board(base_board,2 if player == 1 else 1)
            (p1, p2, p3, p4) = (output[0],output[1],output[2],output[3])

            return [], (2*p1) + p2 - p3 - (2*p4)

        # Select move using greedy algorithm:
        # maxValue = max(moveValues)
        # indexOfMove = moveValues.index(maxValue)
        
        if player == 1:
            val = max(moveValues)
            indexOfMove = moveValues.index(val)
        elif player == 2:
            val = min(moveValues)
            indexOfMove = moveValues.index(val)
        else:
            raise AttributeError

        finalMoveSelection = possible_moves[indexOfMove]

        return finalMoveSelection, val

    def calc_error(self,current_prediction,previous_prediction):
        # print(current_prediction)
        # print(previous_prediction)
        # (p1c, p2c, p3c, p4c) = (current_prediction[0],current_prediction[1],current_prediction[2],current_prediction[3])
        # (p1p, p2p, p3p, p4p) = (previous_prediction[0],previous_prediction[1],previous_prediction[2],previous_prediction[3])
        # td_error = ((2*p1c) + p2c - p3c - (2*p4c) - (2*p1p) + p2p - p3p - (2*p4p))
        td_error = (current_prediction - previous_prediction) # New version
        td_error.backward()
        return td_error

    def update_eligibility_traces(self, lambda_):
    # Before calling this function, ensure that backward() has been called on the loss
        for (name, param), trace in zip(self.named_parameters(), self.traces.values()):
            trace.data = param.grad.data + lambda_ * trace.data.to(DEVICE)
        
    def episode_reset(self):
        self.traces = {name: torch.zeros_like(param) for name, param in self.named_parameters()}
        self.last_prediction = None


class BackgammonNN_v3(nn.Module):
    def __init__(self):
        super(BackgammonNN_v3, self).__init__()
        # Define the layers of the network
        # Input = probability of P1(dark) winning from any given board position
        self.forward_pass = nn.Sequential(
            nn.Linear(198,64),
            nn.ReLU(),
            nn.Linear(64,64),
            nn.ReLU(),
            nn.Linear(64,1),
            nn.Sigmoid()
        )

        # Define Traces and Last Prediction:
        self.traces = {name: torch.zeros_like(param) for name, param in self.named_parameters()}
        self.last_prediction = None

    def forward(self, x):
        return self.forward_pass(x)
    
    def forward_on_board(self,input_board:Board, next_to_move_on_board:int):
        X = []

        for i in range(24):
            men = input_board.positions[i]
            if men == 0:
                j = [0,0,0,0,0,0,0,0]
            elif men == -1:
                j = [1,0,0,0,0,0,0,0]
            elif men == 1:
                j = [0,0,0,0,1,0,0,0]
            elif men == -2:
                j = [1,1,0,0,0,0,0,0]
            elif men == 2:
                j = [0,0,0,0,1,1,0,0]
            elif men <= -3:
                j = [1,1,1,((-men)-3)/2,0,0,0,0]
            elif men >= 3:
                j = [0,0,0,0,1,1,1,(men-3)/2]
            X += j
        if next_to_move_on_board == 1:
            X += [1,0]
        else:
            X += [0,1]
        X += [input_board.positions[24]/2,input_board.positions[25]/2]
        X += [input_board.positions[26],input_board.positions[27]]

        X = torch.tensor(X,dtype=torch.float32).to(DEVICE)
        y = self.forward_pass(X)
        return y
    
    def chose_move(self,base_board:Board,possible_moves,player,verbose=False):
        moveValues = []
        output = None
        # Evaluate all posable moves and identify predicted odd of winning:
        for moveSet in possible_moves:
            testBoard = copy.deepcopy(base_board)
            testBoard.makeMoves(moveSet,player)
            output = self.forward_on_board(testBoard,2 if player == 1 else 1)
            moveValues.append(output)
            #moveValues.append(output if player == 1 else 1-output)
            if verbose:
                print(f"Move Option: {moveSet} ----> {output[0]}")

        # If no possible moves return empty move and valuation for current board (same as next board):
        if len(moveValues) == 0:
            return [], self.forward_on_board(base_board,2 if player == 1 else 1)

        # Select move using greedy algorithm:
        # maxValue = max(moveValues)
        # indexOfMove = moveValues.index(maxValue)
        
        if player == 1:
            val = max(moveValues)
            indexOfMove = moveValues.index(val)
        elif player == 2:
            val = min(moveValues)
            indexOfMove = moveValues.index(val)
        else:
            raise AttributeError

        finalMoveSelection = possible_moves[indexOfMove]

        return finalMoveSelection, val

    def calc_error(self,current_prediction,previous_prediction):
        td_error = (current_prediction - previous_prediction)
        td_error.backward()
        return td_error

    def update_eligibility_traces(self, lambda_):
    # Before calling this function, ensure that backward() has been called on the loss
        for (name, param), trace in zip(self.named_parameters(), self.traces.values()):
            trace.data = param.grad.data + lambda_ * trace.data.to(DEVICE)
        
    def episode_reset(self):
        self.traces = {name: torch.zeros_like(param) for name, param in self.named_parameters()}
        self.last_prediction = None

def Full_Run(inputBoard: Board, inputTurn, networkIdent, silent=True):
    # Determine Table Name:
    if networkIdent[5:8] == "01-":
        model = BackgammonNN().to(DEVICE)
    elif networkIdent[5:8] == "03-":
        model = BackgammonNN_v3().to(DEVICE)
    else:
        print("Error: Network Ident Not Valid (ID)")
        return []
    
    path = "willse_backgammon/AI_Agents/Saved_NNs/" + networkIdent[5:] + ".pt"
    try: 
        model.load_state_dict(torch.load(path))
    except:
        print("Error: Unable to load model states")
        return []
    
    chosen_moves, current_prediction = model.chose_move(inputBoard,inputTurn.current_possible_moves,inputTurn.player)

    if not silent:
        print(f"Current Valuation = {current_prediction[0]*100}% Chance for player 1 to win.")

    return chosen_moves