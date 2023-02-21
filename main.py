import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

st.write("""
Tests
""")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(df)

'''
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
df = pd.DataFrame(data=dic) 

'''