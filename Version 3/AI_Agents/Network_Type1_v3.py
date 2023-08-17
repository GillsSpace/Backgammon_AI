import numpy as np
import sqlite3, copy, random

from Main_Files.Logic_v3 import Board

class FastTurn:
    def __init__(self,player,roll) -> None:
        self.player = player
        self.roll = roll

class BackgammonNeuralNetwork:
    def __init__(self, weights_bias):
        # Initialize weights and biases from the provided list
        self.weights1 = np.array(weights_bias[    :896 ]).reshape(32, 28)
        self.bias1    = np.array(weights_bias[896 :928 ])
        self.weights2 = np.array(weights_bias[928 :1952]).reshape(32, 32)
        self.bias2    = np.array(weights_bias[1952:1984])
        self.weights3 = np.array(weights_bias[1984:2016]).reshape(1 , 32)
        self.bias3    = np.array(weights_bias[2016])
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def d_relu(self, x):
        return np.where(x > 0, 1, 0)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp((x/-10)))
    
    def d_sigmoid(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
    
    def forward(self, inputs):
        hidden_layer1_output = self.relu(np.dot(self.weights1, inputs) + self.bias1)
        hidden_layer2_output = self.relu(np.dot(self.weights2, hidden_layer1_output) + self.bias2)
        output = self.sigmoid(np.dot(self.weights3, hidden_layer2_output) + self.bias3)
        return output[0]
    
    def backpropagation(self, inputs, targets, learning_rate):
        # Forward pass
        hidden_layer1_output = self.relu(np.dot(inputs, self.weights1) + self.bias1)
        hidden_layer2_output = self.relu(np.dot(hidden_layer1_output, self.weights2) + self.bias2)
        output = self.sigmoid(np.dot(hidden_layer2_output, self.weights3) + self.bias3)
        
        # Backward pass
        output_error = output - targets
        output_delta = output_error * self.d_sigmoid(output)
        
        hidden_layer2_error = np.dot(output_delta, self.weights3.T)
        hidden_layer2_delta = hidden_layer2_error * self.d_relu(hidden_layer2_output)
        
        hidden_layer1_error = np.dot(hidden_layer2_delta, self.weights2.T)
        hidden_layer1_delta = hidden_layer1_error * self.d_relu(hidden_layer1_output)
        
        # Update weights and biases
        self.weights3 -= learning_rate * np.dot(hidden_layer2_output.T, output_delta)
        self.bias3 -= learning_rate * np.sum(output_delta, axis=0)
        
        self.weights2 -= learning_rate * np.dot(hidden_layer1_output.T, hidden_layer2_delta)
        self.bias2 -= learning_rate * np.sum(hidden_layer2_delta, axis=0)
        
        self.weights1 -= learning_rate * np.dot(inputs.T, hidden_layer1_delta)
        self.bias1 -= learning_rate * np.sum(hidden_layer1_delta, axis=0)


def fromSQLtoList(id): #Return a list of wights and biases 
    PATH = "Version 3\AI_Agents\\Network_Type1_Data_v3.sqlite3"

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    result = cursor.execute("SELECT data FROM Network_Values_1 WHERE id = ?",(id,),)
    data = str(result.fetchall()[0][0])
    data = data.rsplit()

    list = []
    for num in data:
        list.append(float(num))    

    return list

def Full_Run(inputBoard: Board, inputTurn:FastTurn,networkIdent):
    wb = fromSQLtoList(networkIdent)
    network = BackgammonNeuralNetwork(wb)

    moves = inputBoard.returnMoveSequences(inputTurn.player,inputTurn.roll)

    moveValues = []
    for moveSet in moves:
        testBoard = copy.deepcopy(inputBoard)
        testBoard.makeMoves(moveSet,inputTurn.player)
        output = network.forward(testBoard.positions)
        moveValues.append(output)

    print(moveValues) #DEBUG

    maxValue = max(moveValues)
    indexOfMove = moveValues.index(maxValue)
    finalMoveSelection = moves[indexOfMove]

    return finalMoveSelection


#Database Management Code:

def InitializeDataSet():
    PATH = "Version 3\AI_Agents\\Network_Type1_Data_v3.sqlite3"

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("DROP TABLE Network_Values_1")
    except:
        pass
    cursor.execute("CREATE TABLE Network_Values_1 (id REAL, data TEXT)")

    for i in range(64):
        id = (101 + i) / 100
        dataSet1 = []
        for i in range(2017):
            num = round(random.random(),3)
            num = -1 * num if random.randint(1,2) == 1 else num
            dataSet1.append(num)
        values = " ".join(str(num) for num in dataSet1)

        cursor.execute("INSERT INTO Network_Values_1 VALUES (?, ?)",(id,values,),)

        i = i + 1

    connection.commit()
    print("Data Set Initialized")
