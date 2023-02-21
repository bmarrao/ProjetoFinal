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
age_time = {}
age = df['age']
time = df['time']

for i in range(0,len(df)):
    if age[i] not in age_time:
        age_time[age[i]] = [time[i]]
    else:
        age_time[age[i]].append(time[i])
for i in age_time:
    x = age_time[i]
    age_time[i] = sum(x)/len(x)
age = pd.DataFrame.from_dict(age_time,orient='index')



#print(df['age'])
#print(df['time'])

#print(test)

