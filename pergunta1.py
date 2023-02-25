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


T = df["time"]
E = df["status"]

kmf = KaplanMeierFitter()
kmf.fit(durations = T, event_observed = E)
ax = plt.subplot(111)
a1 = (df["age"] in range(30,40))
a2 = (df["age"] in range(40,50))
a3 = (df["age"] in range(50,60))
a4 = (df["age"] in range(60,70))
a5 = (df["age"] in range(70,90))

kmf.fit(durations = T[a1], event_observed = E[a1], label = "30-40")
kmf.plot_survival_function(ax = ax)
kmf.fit(durations = T[a2], event_observed = E[a2], label = "40-50")
kmf.plot_survival_function(ax = ax)
kmf.fit(durations = T[a3], event_observed = E[a3], label = "50-60")
kmf.plot_survival_function(ax = ax)
kmf.fit(durations = T[a4], event_observed = E[a4], label = "60-70")
kmf.plot_survival_function(ax = ax)
kmf.fit(durations = T[a5], event_observed = E[a5], label = "70-90")
kmf.plot_survival_function(ax = ax)
plt.title("Survival of different ages")
st.pyplot(ax)

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

plt.subplots(figsize = (10, 6))

'''
cph.plot_partial_effects_on_outcome(covariates = 'age',
                                    values = [50, 60, 70, 80],
                                    cmap = 'coolwarm')
                      '''
st.pyplot(plt)

