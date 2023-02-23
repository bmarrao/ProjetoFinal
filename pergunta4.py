'''Existe uma diferença significativa no tempo de sobrevivência entre homens e mulheres
com cancro do pulmão? E após o controle de outras covariáveis, como idade, classificação ECOG ou pontuação de Karnofsky'''

import csv
import pandas as pd
import matplotlib.pyplot as plt                     ### FEITO
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter


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
kmf.fit(T[f], event_observed = E[f], label = "Female")
kmf.plot_survival_function(ax = ax, at_risk_counts = True)
plt.title("Survival of different gender group")
'''