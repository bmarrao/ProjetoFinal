'''Estimar o tempo de sobrevivência em pacientes com cancro do pulmão com base na
sua idade, sexo, classificação ECOG e pontuação de Karnofsky'''

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter


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
cph.fit(df, duration_col = 'time', event_col = 'status', formula = "age + sex + ph.ecog + ph.karno")
cph.print_summary()

plt.subplots(figsize = (10, 6))

#Exemplo para idade
    
cph.predict_survival_function(X = df)


st.pyplot(plt)
