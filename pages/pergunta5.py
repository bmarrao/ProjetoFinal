''' O consumo de calorias nas refeições afeta o tempo de sobrevivência em pacientes com
cancro de pulmão?'''

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)
#print(df)
#ADICIONAR BAR CHART COM CONSUMO CALORIAS E O TEMPO MEDIO DE SOBREVIVẼNCIA DE CADA UM
#print(df.isnull().sum())

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")

kmf = KaplanMeierFitter()
Ta1 = {'time':[]}
Ta2 = {'time':[]}

T = {'time':[]}
E = {'status':[]}

Ea1 = {'status':[]}
Ea2 = {'status':[]}

for index, row in df.iterrows():
    if row['meal.cal'] >= 0 and row['meal.cal'] <= 1000:
        Ta1['time'].append(row['time'])
        Ea1['status'].append(row['status'])
    elif row['meal.cal'] >= 1500 and row['meal.cal'] <= 2500:
        Ta2['time'].append(row['time'])
        Ea2['status'].append(row['status'])

Ta1 = pd.DataFrame(Ta1)
Ea1 = pd.DataFrame(Ea1)
Ta2 = pd.DataFrame(Ta2)
Ea2 = pd.DataFrame(Ea2)


ax = plt.subplot(111)
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="0-1000")
kmf.survival_function_.plot(ax = ax)
plt.title("Difference of calories consumed on people with cancer")

ax = plt.subplot(111)
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta2, event_observed = Ea2,label="1500-2500")
kmf.survival_function_.plot(ax = ax)
kmf2 = plt.gcf()

py_fig = tls.mpl_to_plotly(kmf2, resize=True)

st.plotly_chart(py_fig)

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

mpl_fig = plt.figure()

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'meal.cal',
                                    values = [0,200,500,1000,1500,2000,2500],
                                    cmap = 'coolwarm')

cph2 = plt.gcf()

py_fig = tls.mpl_to_plotly(cph2, resize=True)

st.plotly_chart(py_fig)