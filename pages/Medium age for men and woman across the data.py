import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls
import plotly.express as px
from sklearn.model_selection import train_test_split
from sksurv.ensemble import RandomSurvivalForest
import plotly.graph_objects as go
import numpy as np
import plotly.figure_factory as ff

st.subheader("Medium age for men and woman across the data")
df = st.session_state['dic1'] 
df_alive = st.session_state['dicalive']
df_dead = st.session_state['dicdead'] 

fig = go.Figure()
fig.add_trace(
    go.Box(x=df['sex'],y=df['age'],
    name='All data'))
                         

fig.add_trace(go.Box(x=df_dead['sex'],y=df_dead['age'],name='Dead by the end of the experiment'))
fig.add_trace(go.Box(x=df_alive['sex'],y=df_alive['age'],name='Alive by the end of the experiment'))
            
fig.update_layout(
    yaxis_title='Age',
    boxmode='group' # group together boxes of the different traces for each value of x
)


fig.update_traces(legendgroup='group')


st.plotly_chart(fig)
#Falta o comparativo dos q tavam vivo no experimento
fig = px.box(df, color = "sex" ,x="sex", y="age", points="all",hover_data=df.columns)
st.plotly_chart(fig)
