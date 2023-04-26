'''Existe relação entre a pontuação de desempenho de Karnofsky e o número de calorias
consumidas nas refeições?'''

import pandas as pd
import matplotlib.pyplot as plt             ### FEITO
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter
import plotly.express as px


'''
filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
print(df.to_dict())
'''
df = st.session_state['dic']

x = df['meal.cal']
y = df['ph.karno']

z = px.scatter(x = x, y =y,opacity = .2)
st.plotly_chart(z)

st.write(round(x. corr(y), 2))


'''
fig = px.scatter(
    df,
    x="sepal_width",
    y="sepal_length",
    color="sepal_length",
    color_continuous_scale="reds",
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    st.plotly_chart(fig, theme=None, use_container_width=True)'''