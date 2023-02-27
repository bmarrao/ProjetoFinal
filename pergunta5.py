''' O consumo de calorias nas refeições afeta o tempo de sobrevivência em pacientes com
cancro de pulmão?'''

import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter
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

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula = "meal.cal")

mpl_fig = plt.figure()

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'meal.cal',
                                    values = [0,200,500,1000,1500,2000,2500],
                                    cmap = 'coolwarm')

cph2 = plt.gcf()

py_fig = tls.mpl_to_plotly(cph2, resize=True)

st.plotly_chart(py_fig)