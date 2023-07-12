import random
import sqlite3
import json

PATH = "Version 3\Data\TestData1.sqlite3"

connection = sqlite3.connect(PATH)
cursor = connection.cursor()

def InitializeDataSet():
    try:
        cursor.execute("DROP TABLE Network_Values_1")
    except:
        pass
    cursor.execute("CREATE TABLE Network_Values_1 (id REAL, data TEXT)")

    for i in range(64):
        id = (101 + i) / 100
        dataSet1 = []
        for i in range(1441):
            num = random.randint(-10,10)
            dataSet1.append(num)
        values = " ".join(str(num) for num in dataSet1)

        cursor.execute("INSERT INTO Network_Values_1 VALUES (?, ?)",(id,values,),)

        i = i + 1

    connection.commit()
    print("Data Set Initialized")

def UpdateDataSet(firstID,lastID,range):

    """
    Update each Value in data by some random float constrained by range. FirstID value will not be altered.
    """

    Id = firstID + 0.01

    while Id <= lastID:
        print(Id)
        result = cursor.execute("SELECT data FROM Network_Values_1 WHERE id = ?",(Id,),)
        data = str(result.fetchall()[0][0])
        data = data.rsplit()
        newData = []
        for num in data:
            startNum = float(num)
            diff = (random.random() * range * 2) - 1
            endNum = round(startNum + diff, 4)
            newData.append(endNum)
            values = " ".join(str(num) for num in newData)
        cursor.execute("UPDATE Network_Values_1 SET data = ? WHERE id = ?",(values,Id))
        Id = round((Id + 0.01),2)

    connection.commit()


#RUN CODE:

# InitializeDataSet()
# UpdateDataSet(1,1.64,1)
