''' O consumo de calorias nas refeições afeta o tempo de sobrevivência em pacientes com
cancro de pulmão?'''

import csv
import pandas as pd
import matplotlib.pyplot as plt
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

cph.plot_partial_effects_on_outcome(covariates = 'meal.cal',
                                    values = [0,200,500,1000,1500,2000,2500],
                                    cmap = 'coolwarm')
st.pyplot(plt)