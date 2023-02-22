import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter   

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)


st.title("Survivor Analysis for lung cancer data")
st.header("Analysis of age impact in the time that a person survives")

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
graph1 = pd.DataFrame.from_dict(age_time,orient='index')

st.line_chart(graph1)

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")


cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

plt.subplots(figsize = (10, 6))

'''
cph.plot_partial_effects_on_outcome(covariates = 'age',
                                    values = [50, 60, 70, 80],
                                    cmap = 'coolwarm')
                      '''
st.pyplot(plt)

