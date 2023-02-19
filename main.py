import csv
import pandas as pd
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

print(dic)


for i in dic :
    print (dic[i])
