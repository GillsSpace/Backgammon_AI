import sqlite3, copy, random, pathlib, os
import numpy as np

PATH = pathlib.Path(__file__).parent.parent.parent
os.chdir(PATH)

def relu(x):
    return np.maximum(0, x)


def d_relu(x):
    return np.where(x > 0, 1, 0)


def sigmoid(x):
    return 1 / (1 + np.exp((x / -10)))


def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


class BackgammonNeuralNetwork:
    def __init__(self, id, new=False, size=(28, 32, 32, 4)):
        self.id = id
        self.location = "willse_backgammon\AI_Agents\Data_Sets\\Network_Type2_Data.db"

        if new:
            self.data_size = sum(size[i + 1] * (size[i] + 1) for i in range(len(size) - 1))  # Total weights and biases
            self.data_raw = list(np.random.rand(self.data_size))  # Generates weights and biases
            self.commit_to_sql()  # Commits data_raw to database
        else:
            self.data_raw = self.from_sql_to_list()  # Retrieves data from database

        self.weights = []
        self.biases = []

        for layer in size:
            self.weights.append(self.data_raw[0:(size[0] * size[1])])
            self.biases.append(self.data_raw[0:(size[0] * size[1])])

        # for i in range(len(size)):

    def from_sql_to_list(self, table="Default_Table"):  # Return a list of wights and biases
        connection = sqlite3.connect(self.location)
        cursor = connection.cursor()

        result = cursor.execute("SELECT data FROM " + table + " WHERE id = ?", (self.id,), )

        data_str = str(result.fetchone()[0])
        data_list = data_str.rsplit()

        data = [float(num) for num in data_list]
        return data

    def commit_to_sql(self, table="Default_Table"):
        connection = sqlite3.connect("Network_Type2_Data.db")
        cursor = connection.cursor()

        values = " ".join(str(num) for num in self.data_raw)

        try:
            cursor.execute("UPDATE " + table + " SET data = ? WHERE id = ?", (values, self.id))
        except sqlite3.OperationalError:
            cursor.execute("INSERT INTO " + table + " VALUES (?, ?)", (self.id, values,), )

        connection.commit()


def initialize_data_set():
    connection = sqlite3.connect("willse_backgammon/AI_Agents/Data_Sets/Network_Type2_Data.db") 
    cursor = connection.cursor()

    try:
        cursor.execute("DROP TABLE Default_Table")
    except sqlite3.OperationalError:
        pass
    cursor.execute("CREATE TABLE Default_Table (id TEXT, data TEXT)")

    connection.commit()
    print("Data Set Initialized")

initialize_data_set()  # Reset Database
# test = BackgammonNeuralNetwork("test")
