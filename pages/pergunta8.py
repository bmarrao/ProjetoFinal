import pandas as pd
import streamlit as st
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.express as px

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df = st.session_state['dic']

dic = {'Paciente' : df["ph.karno"],'Medico': df["pat.karno"]}
data = pd.DataFrame(data = dic)

z = px.scatter(data,x = "Paciente", y ="Medico",trendline="ols")


st.plotly_chart(z)