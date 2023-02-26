'''Existe uma diferença significativa no tempo de sobrevivência entre homens e mulheres
com cancro do pulmão? E após o controle de outras covariáveis, como idade, classificação ECOG ou pontuação de Karnofsky'''

import csv
import pandas as pd
import matplotlib.pyplot as plt                     ### FEITO
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter,KaplanMeierFitter

#ADICIONAR MAIS GRÁFICOS - BARCHART SIMPLES ?
filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)
#print(df)

#print(df.isnull().sum())

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
df = df.reset_index() 
df['status'] = df["status"]-1

fig, a = plt.subplots()


Ta1 = {'time':[]}
Ta2 = {'time':[]}
Ea1 = {'status':[]}
Ea2 = {'status':[]}
for index, row in df.iterrows():
    if row['sex'] == 1 :
        Ta1['time'].append(row['time'])
        Ea1['status'].append(row['status'])
    elif row['sex'] == 2:
        Ta2['time'].append(row['time'])
        Ea2['status'].append(row['status'])
Ta1 = pd.DataFrame(Ta1)
Ea1 = pd.DataFrame(Ea1)
Ta2 = pd.DataFrame(Ta2)
Ea2 = pd.DataFrame(Ea2)
ax = plt.subplot(111)
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="Homem ou mulher")
kmf.survival_function_.plot(ax = a)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta2, event_observed = Ea2,label="Homem ou mulher")
kmf.survival_function_.plot(ax = a)

st.pyplot(fig)

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'sex',
                                    values = [1,2],
                                    cmap = 'coolwarm')
st.pyplot(plt)


'''
T = df["time"]
E = df["status"]

kmf = KaplanMeierFitter()
kmf.fit(durations = T, event_observed = E)
ax = plt.subplot(111)
m = (df["sex"] == 1)
f = (df["sex"] == 2)
kmf.fit(durations = T[m], event_observed = E[m], label = "Male")
kmf.plot_survival_function(ax = ax)
plt.title("Survival of different gender group")
kmf.fit(T[f], event_observed = E[f], label = "Female")
kmf.plot_survival_function(ax = ax, at_risk_counts = True)
'''