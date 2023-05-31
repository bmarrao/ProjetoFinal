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



df = st.session_state['dic1']
df_dead = st.session_state['dicalive']
df_alive = st.session_state['dicdead']

st.header("Difference of calories consumed groupped by age")
bins= [0,2,4,13,20,110]
labels = ["39-45","45-50","50-55","55-60","60-65","65-70","70-75","75-82"]
#mean = df
mean = df.groupby(pd.cut(df['age'], [39,45,50,55,60,65,70,75,82]),as_index=False).mean()
mean["AgeGroup"] = labels
mean_dead = df_dead.groupby(pd.cut(df_dead['age'],[39,45,50,55,60,65,70,75,82]),as_index=False).mean()
mean_dead["AgeGroup"] = labels
mean_alive = df_alive.groupby(pd.cut(df_alive['age'],[39,45,50,55,60,65,70,75,82]),as_index=False).mean()
mean_alive["AgeGroup"] = labels

fig = go.Figure()
fig.add_trace(go.Bar(x=mean['AgeGroup'],y=mean['meal.cal'],name='All data'))
fig.add_trace(go.Bar(x=mean_dead['AgeGroup'],y=mean_dead['meal.cal'],name='Dead by the end of the experiment'))
fig.add_trace(go.Bar(x=mean_alive['AgeGroup'],y=mean_alive['meal.cal'],name='Alive by the end of the experiment'))
fig.update_layout(
    yaxis_title='average calories per meal',
    xaxis_title='Age',

    boxmode='group' # group together boxes of the different traces for each value of x
)
st.plotly_chart(fig)