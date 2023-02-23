import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
#df["ph.ecog"] = df["ph.ecog"].astype("int64")
df["ph.ecog"].fillna(df["ph.ecog"].mean(), inplace = True)

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

#plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'inst',
                                    values = [0,1,2,3,4],
                                    cmap = 'coolwarm')
st.pyplot(plt)