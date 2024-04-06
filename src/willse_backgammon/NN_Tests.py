import copy, random, sqlite3, time, csv, ast
import numpy as np
import pandas as pd

try:
    from Main_Files import AI as AI
    from Main_Files import Logic as Logic
except ModuleNotFoundError:
    from willse_backgammon.Main_Files import Logic as Logic
    from willse_backgammon.Main_Files import AI as AI

df = pd.read_csv("willse_backgammon/AI_Agents/Data_Sets/data_set_1.csv")
data = np.array(df)

print("Loading Data... \n")
print(df.head()) 

print(f"\nData Shape:     {data.shape}")

m, n = data.shape
np.random.shuffle(data)

data_dev = data[0:1000].T
Y_dev = data_dev[2]
Y_dev = [ast.literal_eval(row.strip()) for row in Y_dev]
Y_dev = np.array(Y_dev).astype(float)
print(f"Y_dev Shape:    {Y_dev.shape}")
X_dev = data_dev[1]
X_dev = [ast.literal_eval(row.strip()) for row in X_dev]
X_dev = np.array(X_dev).astype(float)
print(f"X_dev Shape:    {X_dev.shape}")
X_dev = X_dev / 255.0

data_train = data[1000:m].T
Y_train = data_train[2]
Y_train = [ast.literal_eval(row.strip()) for row in Y_train]
Y_train = np.array(Y_train).astype(float)
print(f"Y_train Shape:  {Y_train.shape}")
X_train = data_train[1]
X_train = [ast.literal_eval(row.strip()) for row in X_train]
X_train = np.array(X_train).astype(float)
print(f"X_train Shape:  {X_train.shape}")
X_train = X_train / 255.0


# with open('willse_backgammon/AI_Agents/Data_sets/data_set_1.csv', 'r', newline='') as f:
#     reader = csv.reader(f, delimiter=',')
#     print(reader)
#     for row in reader:
#         print ([ast.literal_eval(x.strip()) for x in row])

# with open('willse_backgammon/Logs/NN_Tests.log','w') as f:
#     reader = csv.reader(f, delimiter=',')
#     for row in reader:
#         print ([ast.literal_eval(x.strip()) for x in row])
#     # Define the data to be written
#     data = ['This is the first line', 'This is the second line', 'This is the third line']
#     # Use a for loop to write each line of data to the file
#     for line in data:
#         f.write(line + '\n')
#         # Optionally, print the data as it is written to the file
#         print(line)
# # The file is automatically closed when the 'with' block ends
