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

print(df.isnull().sum())

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')
cph.print_summary()

plt.subplots(figsize = (10, 6))
#cph.plot() # não consigo dar plot por erro de plugin??
'''
Exemplo para idade
cph.plot_partial_effects_on_outcome(covariates = 'age',
                                    values = [50, 60, 70, 80],
                                    cmap = 'coolwarm')
'''

                                    
'''
Exemplo para sexo
cph.plot_partial_effects_on_outcome(covariates = 'sex',
                                    values = [0,1],
                                    cmap = 'coolwarm')
'''
st.pyplot(plt)
