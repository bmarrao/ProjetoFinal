import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls 

'''
filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
#df["ph.ecog"] = df["ph.ecog"].astype("int64")
df["ph.ecog"].fillna(df["ph.ecog"].mean(), inplace = True)
'''
df = st.session_state['dic']

dataf = {}

ecogs = []

for index, row in df.iterrows():
    if row['ph.ecog'] not in ecogs:
        ecogs.append(row['ph.ecog'])

for a in ecogs:
    Ta = {'time':[]}
    Ea = {'status':[]}
    dataf[a] = [Ta,Ea]

for index, row in df.iterrows():
    dataf[row['ph.ecog']][0]['time'].append(row['time'])
    dataf[row['ph.ecog']][1]['status'].append(row['status'])

ax = plt.subplot()
kmf = KaplanMeierFitter()


for a in ecogs:
    
    dataf[a][0] = pd.DataFrame(dataf[a][0])
    dataf[a][1] = pd.DataFrame(dataf[a][1])

    
    kmf.fit(durations = dataf[a][0], event_observed = dataf[a][1],label = "ecog" + str(a))
    kmf.survival_function_.plot(ax = ax)

T = df["time"]
E = df["status"]
ax = plt.subplot(111)
kmf.fit(durations = T, event_observed =E,label=f"Baseline")
kmf.survival_function_.plot(ax = ax)

figaux = plt.gcf()

py_fig = tls.mpl_to_plotly(figaux,resize = True)

st.plotly_chart(py_fig)




if st.button('Show ecog score relation in cph model graph'):
    cph = CoxPHFitter()
    cph.fit(df, duration_col = 'time', event_col = 'status',formula = "ph.ecog")

    #plt.subplots(figsize = (10, 6))

    fig, ax = plt.subplots()

    cph.plot_partial_effects_on_outcome(covariates = 'ph.ecog',
                                        values = [0,1,2,3,4],
                                        cmap = 'coolwarm')

    figaux = plt.gcf()

    py_fig = tls.mpl_to_plotly(figaux,resize = True)

    st.plotly_chart(py_fig)