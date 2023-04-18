'''Existe uma diferença significativa no tempo de sobrevivência entre homens e mulheres
com cancro do pulmão? E após o controle de outras covariáveis, como idade, classificação ECOG ou pontuação de Karnofsky'''

import pandas as pd
import matplotlib.pyplot as plt                     ### FEITO
import streamlit as st
from lifelines import CoxPHFitter,KaplanMeierFitter
import plotly.tools as tls   
from plotly.graph_objs import *

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


kmf = KaplanMeierFitter()
Ta1 = {'time':[]}
Ta2 = {'time':[]}

T = {'time':[]}
E = {'status':[]}

Ea1 = {'status':[]}
Ea2 = {'status':[]}

for index, row in df.iterrows():
    if row['sex'] == 1:
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
kmf.fit(durations = Ta1, event_observed = Ea1,label="Homem")
kmf.survival_function_.plot(ax = ax)
plt.title("Survival of different gender group")

ax = plt.subplot(111)
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta2, event_observed = Ea2,label="Mulher")
kmf.survival_function_.plot(ax = ax)
plt.title("Survival of different gender group")
kmf2 = plt.gcf()

py_fig = tls.mpl_to_plotly(kmf2, resize=True)

st.plotly_chart(py_fig)



cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

mpl_fig = plt.figure()

cph.plot_partial_effects_on_outcome(covariates = 'sex',
                                    values = [1,2],
                                    cmap = 'coolwarm')

cph2 = plt.gcf()

py_fig = tls.mpl_to_plotly(cph2, resize=True)

st.plotly_chart(py_fig)