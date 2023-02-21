import numpy as np
import pandas as pd
import csv

filename = './lung-cancer-data.csv'
dic = {}
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    #print(fields)
    #print(csvfile)
    #print(csvreader)
    ind = 0
    for row in csvreader:
        dict = {}
        for i in range(len(fields)):
            if i == 2:
                dict[fields[i]] = int(row [i]) - 1
            else :
                if row[i] != 'NA':
                    dict[fields[i]] = int(row[i]) - 1
                else :
                    dict[fields[i]] = row[i]
        dic [ind] = dict
        ind += 1
df = pd.read_csv(filename)
test = pd.DataFrame(dic)
print(df)
print(test)
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
print(chart_data)
