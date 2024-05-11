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

        # Evaluate all posable moves and identify predicted odd of winning:
        for moveSet in possible_moves:
            testBoard = copy.deepcopy(base_board)
            testBoard.makeMoves(moveSet,player)
            output = self.forward_on_board(testBoard,2 if player == 1 else 1)
            moveValues.append(output if player == 1 else 1-output)

            if verbose:
                print(f"Move Option: {moveSet} ----> {output[0]}")

        # If no possible moves return empty move and valuation for current board (same as next board):
        if len(moveValues) == 0:
            return [], self.forward_on_board(base_board,2 if player == 1 else 1)

        # Select move using greedy algorithm:
        maxValue = max(moveValues)
        indexOfMove = moveValues.index(maxValue)
        finalMoveSelection = possible_moves[indexOfMove]

        return finalMoveSelection, output

    def update_eligibility_traces(self, lambda_):
    # Before calling this function, ensure that backward() has been called on the loss
        for (name, param), trace in zip(self.named_parameters(), self.traces.values()):
            trace.data = param.grad.data + lambda_ * trace.data.to(DEVICE)

        # for (name, param) in self.named_parameters():
        #     trace.data[name] = param.grad.data + lambda_ * trace.data[name].to(DEVICE)
        
    def episode_reset(self):
        self.traces = {name: torch.zeros_like(param) for name, param in self.named_parameters()}
        self.last_prediction = None