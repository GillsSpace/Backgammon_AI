import copy, random, sqlite3, time, csv, ast
import numpy as np
import pandas as pd

try:
    from Main_Files import AI as AI
    from Main_Files import Logic as Logic
    from AI_Agents import Network_Type2
except ModuleNotFoundError:
    from willse_backgammon.Main_Files import Logic as Logic
    from willse_backgammon.Main_Files import AI as AI
    from willse_backgammon.AI_Agents import Network_Type2

# Code:
Network_Type2.main()

