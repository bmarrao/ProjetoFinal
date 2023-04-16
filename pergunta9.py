import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls 

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df["inst"].fillna(100.00, inplace = True)
df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
#df["ph.ecog"] = df["ph.ecog"].astype("int64")
df["ph.ecog"].fillna(df["ph.ecog"].mean(), inplace = True)

dataf = {}

insts = []




for index, row in df.iterrows():
    if row['inst'] not in insts:
        insts.append(row['inst'])



for a in insts:
    Ta = {'time':[]}
    Ea = {'status':[]}
    dataf[a] = [Ta,Ea]



for index, row in df.iterrows():
    dataf[row['inst']][0]['time'].append(row['time'])
    dataf[row['inst']][1]['status'].append(row['status'])

ax = plt.subplot()
kmf = KaplanMeierFitter()


for a in insts:
    dataf[a][0] = pd.DataFrame(dataf[a][0])
    dataf[a][1] = pd.DataFrame(dataf[a][1])

    
    kmf.fit(durations = dataf[a][0], event_observed = dataf[a][1],label = "inst")
    kmf.survival_function_.plot(ax = ax)

figaux = plt.gcf()

py_fig = tls.mpl_to_plotly(figaux,resize = True)

st.plotly_chart(py_fig)











cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

fig, ax = plt.subplots()

cph.plot_partial_effects_on_outcome(covariates = 'inst',
                                    values = [a for a in insts],
                                    cmap = 'coolwarm')





st.pyplot(plt)

