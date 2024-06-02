def single_training_game_subprocess_v2(model:BackgammonNN, lambda_=0.8, alpha=0.01):

    # Resets trace and previous prediction variables:
    model.episode_reset()
    
    # Initialize board and game variables:
    board = Board()
    board.setStartPositions()
    current_player = random.randint(1,2)
    game_over = False

    first_turn = True
    # Initialize first turn

    # Generate and make moves
    #chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player)
    #board.makeMoves(chosen_moves,current_player)

    # Transitions to next state and player:
    #current_player = 2 if current_player == 1 else 1
    #model.last_prediction = current_prediction

    while not game_over:
        # Initialize turn
        if first_turn:
            turn = Turn(current_player,"AI",First=first_turn)
            turn.updatePossibleMovesStandardFormat(board)
        else:
            turn = Turn(current_player,"AI")
            turn.updatePossibleMovesStandardFormat(board)

        # Generates move and prediction:
        chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player)

        # Apply Best Action
        board.makeMoves(chosen_moves, current_player)
        # Is game over?
        game_over = True if board.pip[current_player-1] == 0 else False
        

        # Compute P'
        # TODO: Can we clean up the 2 if player == 1 else 1 logic? Encapsulate the behavior some way?
        next_prediction = model.forward_on_board(board, 2 if current_player == 2 else 1)

        # Calculate the derivatives of predictions with respect to model weights/bias (params)

        # Calculates error and eligibility traces:
        # torch.no_grad() has same effect as detach but we know everything below will be "detached"
        if not game_over:
            model.zero_grad()
            current_prediction.backward()
            with torch.no_grad():
                td_error = next_prediction - current_prediction

                # We do not compute gradient with respect to the TD Error!
                # td_error.backward()

                # Updates eligibility traces then updates weights (params)
                model.update_eligibility_traces(lambda_)

                for name, param in model.named_parameters():
                    trace = model.traces[name]
                    param.data += alpha * td_error * trace.data

            #TODO: Could collect TD error here for plotting?

            # Makes a move, checks if game is over, and transitions to new turn:
            current_player = 2 if current_player == 1 else 1
            model.last_prediction = current_prediction

    # Performs final update using actual reward:
    reward = torch.zeros(1).to(DEVICE) if current_player == 1 else torch.ones(1).to(DEVICE) # current_player = loser
    td_error = reward.detach() - model.last_prediction
    model.update_eligibility_traces(lambda_)

    for name, param in model.named_parameters():
        trace = model.traces[name]
        param.data += alpha * td_error * trace.data


def single_training_game_verbose_v2(model:BackgammonNN, lambda_=0.8, alpha=0.01):

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

    #print("------------------------------------------------------------------------------------------")
    #print("Starting Turn...")
    #print(f"Player: {current_player} ({player_symbols[current_player-1]})")
    print_backgammon_board(board.positions)

    # Initialize first turn
    turn = Turn(current_player,"AI",First=True)
    turn.updatePossibleMovesStandardFormat(board)

    # Generate and make moves
    #chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player,True)

    # Debug Info:
    #print(f"Roll: {turn.roll} // Move To Play: {chosen_moves}")
    #print(f"Valuation:          {current_prediction}")
    #print(f"Previous Valuation: {model.last_prediction}")

    #print("------------------------------------------------------------------------------------------")

    #board.makeMoves(chosen_moves,current_player)
    #current_player = 2 if current_player == 1 else 1
    #model.last_prediction = current_prediction

    while not game_over:

        print("------------------------------------------------------------------------------------------")
        print("Starting Turn...")
        print(f"Player: {current_player} ({player_symbols[current_player-1]})")
        print_backgammon_board(board.positions)

        # Initialize turn
        turn = Turn(current_player,"AI")
        turn.updatePossibleMovesStandardFormat(board)

        # Generates move and prediction:
        chosen_moves, current_prediction = model.chose_move(board,turn.current_possible_moves,current_player)

        # Apply Best Action
        board.makeMoves(chosen_moves, current_player)
        game_over = True if board.pip[current_player-1] == 0 else False
        

        # Compute P'
        # TODO: Can we clean up the 2 if player == 1 else 1 logic? Encapsulate the behavior some way?
        next_prediction = model.forward_on_board(board, 2 if current_player == 1 else 1)

        # Calculate the derivatives of predictions with respect to model weights/bias (params)
        model.zero_grad()
        current_prediction.backward()

        # Calculates error and eligibility traces:
        # torch.no_grad() has same effect as detach but we know everything below will be "detached"
        if not game_over:
            with torch.no_grad():
                td_error = next_prediction - current_prediction

                # We do not compute gradient with respect to the TD Error!
                # td_error.backward()
                model.update_eligibility_traces(lambda_)

                # Updates parameters:
                for name, param in model.named_parameters():
                    trace = model.traces[name]
                    param.data += alpha * td_error * trace.data


        # Debug Info:
        print(f"Roll: {turn.roll} // Move To Play: {chosen_moves}")
        print(f"Valuation:          {next_prediction}")
        print(f"Previous Valuation: {current_prediction}")
        print(f"TD_error:           {td_error}")

        print("------------------------------------------------------------------------------------------")

        current_player = 2 if current_player == 1 else 1

        model.last_prediction = current_prediction
        #model.zero_grad()

    print("------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------")
    print("Final Update:")
    print(f"Winner = {1 if current_player == 2 else 2}")
    print("Final Board:")
    print_backgammon_board(board.positions)

    reward = torch.zeros(1).to(DEVICE) if current_player == 1 else torch.ones(1).to(DEVICE) # current_player = loser
    td_error = reward.detach() - model.last_prediction
    model.update_eligibility_traces(lambda_)

    for name, param in model.named_parameters():
        trace = model.traces[name]
        param.data += alpha * td_error * trace.data

    print(f"Reward:             {reward}")
    print(f"Previous Valuation: {current_prediction}")
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


#TODO: Create a base class model, encapsulate training behavior, 
# classes that inherit will have different structure, or make one class and have structure
# passed in params

class BackgammonNN_v2(nn.Module):
    def __init__(self):
        super(BackgammonNN_v2, self).__init__()
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

    def update_eligibility_traces(self, lambda_):
    # Before calling this function, ensure that backward() has been called on the loss
        for (name, param), trace in zip(self.named_parameters(), self.traces.values()):
            trace.data = param.grad.data + lambda_ * trace.data.to(DEVICE)

        # for (name, param) in self.named_parameters():
        #     trace.data[name] = param.grad.data + lambda_ * trace.data[name].to(DEVICE)
        
    def episode_reset(self):
        self.traces = {name: torch.zeros_like(param) for name, param in self.named_parameters()}
        self.last_prediction = None
