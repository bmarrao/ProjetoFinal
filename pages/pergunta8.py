import pandas as pd
import streamlit as st
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.express as px

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)
'''
st.subheader("8- Comparar a pontuação de desempenho de Karnofsky, 
             avaliada pelo paciente, com a classificação do médico")
'''
'''
df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
#df["ph.ecog"] = df["ph.ecog"].astype("int64")
df["ph.ecog"].fillna(df["ph.ecog"].mean(), inplace = True)
'''
df = st.session_state['dic']

dic = {'Paciente' : df["ph.karno"],'Medico': df["pat.karno"]}
data = pd.DataFrame(data = dic)

z = px.scatter(data,x = "Paciente", y ="Medico",trendline="ols")


st.plotly_chart(z)