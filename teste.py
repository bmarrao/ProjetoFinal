import csv
import pandas as pd
import matplotlib.pyplot as plt                     ### FEITO
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter,KaplanMeierFitter
import streamlit.components.v1 as components
import chart_studio as py
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

st.pyplot(plt)