import numpy as np

class BackgammonNeuralNetwork:
    def __init__(self, weights_biases):
        self.weights_biases = weights_biases
        self.num_input = 28
        self.num_hidden = 20
        self.num_output = 1
        
        # Extract weights and biases from the provided list
        self.weights1 = np.array(weights_biases[:self.num_input*self.num_hidden]).reshape(self.num_input, self.num_hidden)
        self.biases1 = np.array(weights_biases[self.num_input*self.num_hidden:self.num_input*self.num_hidden+self.num_hidden])
        self.weights2 = np.array(weights_biases[self.num_input*self.num_hidden+self.num_hidden:self.num_input*self.num_hidden+self.num_hidden+self.num_hidden*self.num_output]).reshape(self.num_hidden, self.num_output)
        self.bias2 = np.array(weights_biases[self.num_input*self.num_hidden+self.num_hidden+self.num_hidden*self.num_output:])
        
    def forward_propagate(self, inputs):
        hidden_layer = np.dot(inputs, self.weights1) + self.biases1
        hidden_layer = self.sigmoid(hidden_layer)
        output_layer = np.dot(hidden_layer, self.weights2) + self.bias2
        output_layer = self.sigmoid(output_layer)
        return output_layer
    
    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

import random

def create_next_generation(network1, network2, network3, network4, learning_rate):
    offspring_counts = [32, 16, 8, 8]  # Offspring counts for first, second, third, and fourth place

    # Initialize a list to store the next generation of networks
    next_generation = []

    # Create offspring for the first-place network
    for _ in range(offspring_counts[0]):
        offspring = create_offspring(network1, learning_rate)
        next_generation.append(offspring)

    # Create offspring for the second-place network
    for _ in range(offspring_counts[1]):
        offspring = create_offspring(network2, learning_rate)
        next_generation.append(offspring)

    # Create offspring for the third-place network
    for _ in range(offspring_counts[2]):
        offspring = create_offspring(network3, learning_rate)
        next_generation.append(offspring)

    # Create offspring for the fourth-place network
    for _ in range(offspring_counts[3]):
        offspring = create_offspring(network4, learning_rate)
        next_generation.append(offspring)

    # Randomly select and add additional networks to reach a total of 64 networks
    while len(next_generation) < 64:
        random_network = random.choice([network1, network2, network3, network4])
        offspring = create_offspring(random_network, learning_rate)
        next_generation.append(offspring)

    return next_generation


def create_offspring(network, learning_rate):
    # Extract the weights and biases from the parent network
    weights_biases = network.weights_biases.copy()

    # Mutate the weights and biases by adding random noise
    for i in range(len(weights_biases)):
        weights_biases[i] += random.uniform(-learning_rate, learning_rate)

    # Create a new instance of the network class with the mutated weights and biases
    offspring = BackgammonNeuralNetwork(weights_biases)

    return offspring

def evolve_networks(num_iterations, initial_learning_rate):
    num_networks = 64
    networks = [BackgammonNeuralNetwork(generate_random_weights_biases()) for _ in range(num_networks)]
    learning_rate = initial_learning_rate

    for iteration in range(num_iterations):
        print(f"Iteration {iteration + 1}")
        print("Tournament Results:")
        winners = play_tournament(networks)

        # Calculate new learning rate
        learning_rate = initial_learning_rate / (iteration + 1)

        # Create next generation of networks
        next_generation = create_next_generation(winners[0], winners[1], winners[2], winners[3], learning_rate)

        networks = next_generation

    return networks


def play_tournament(networks):
    winners_bracket = []
    losers_bracket = []
    eliminated = []
    num_networks = len(networks)

    # First round of winners bracket
    for i in range(0, num_networks, 2):
        network1 = networks[i]
        network2 = networks[i + 1]
        winner = runGame(network1, network2)
        if winner == network1:
            winners_bracket.append(network1)
            eliminated.append(network2)
        else:
            winners_bracket.append(network2)
            eliminated.append(network1)

    # Remaining rounds of winners bracket
    while len(winners_bracket) > 1:
        new_round = []
        for i in range(0, len(winners_bracket), 2):
            network1 = winners_bracket[i]
            network2 = winners_bracket[i + 1]
            winner = runGame(network1, network2)
            if winner == network1:
                new_round.append(network1)
                eliminated.append(network2)
            else:
                new_round.append(network2)
                eliminated.append(network1)
        winners_bracket = new_round

    # First round of losers bracket
    losers_bracket.extend(eliminated)

    # Remaining rounds of losers bracket
    while len(losers_bracket) > 1:
        new_round = []
        for i in range(0, len(losers_bracket), 2):
            network1 = losers_bracket[i]
            network2 = losers_bracket[i + 1]
            winner = runGame(network1, network2)
            if winner == network1:
                new_round.append(network1)
                eliminated.append(network2)
            else:
                new_round.append(network2)
                eliminated.append(network1)
        losers_bracket = new_round

    # Final match between winners bracket winner and losers bracket winner
    network1 = winners_bracket[0]
    network2 = losers_bracket[0]
    final_winner = runGame(network1, network2)

    # Determine top four winners
    top_four_winners = [final_winner]
    top_four_winners.extend(winners_bracket[1:3])
    top_four_winners.append(losers_bracket[0])

    return top_four_winners


def generate_random_weights_biases():
    num_weights_biases = 1441
    return [random.uniform(-1, 1) for _ in range(num_weights_biases)]


def runGame(network1, network2):
    # Replace with your implementation of the game

    #Code Here imported from v2.2

    import importlib.util       
 
    # passing the file name and path as argument
    spec = importlib.util.spec_from_file_location(
    "mod", "W:\(W) - Code\(W) Backgammon\Version 2.2\Manual_v2_2.py")   
    
    # importing the module as foo
    Manual = importlib.util.module_from_spec(spec)       
    spec.loader.exec_module(Manual)

    winner = Manual.RunGame(network1,network2)

    # Return the winning network

    return winner

evolve_networks(1000,1)
