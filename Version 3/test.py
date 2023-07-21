from multiprocessing import Pool
import time
import arcade,tkinter,arcade.gui,copy
from Main_Files.Logic_v3 import Board, Turn

def f(x):
    return x*x

if __name__ == '__main__':

    st = time.time()

    with Pool() as pool:      

        results = pool.map(f, range(100000))
        print(f"Time = {time.time()-st}")

    print("//Completed")
    print(f"Time = {time.time()-st}")