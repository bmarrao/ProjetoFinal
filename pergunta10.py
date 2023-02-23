'''Existe uma diferença significativa no tempo de sobrevivência entre homens e mulheres
com cancro do pulmão? E após o controle de outras covariáveis, como idade, classificação ECOG ou pontuação de Karnofsky'''

import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter


filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")

x = df['meal.cal']
y = df['ph.karno']

plt.scatter(x, y)

st.pyplot(plt)