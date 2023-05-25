import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

hovertemplate = st.session_state['hovertemplate']

df_na = st.session_state['dic1']
grouped_na=df_na.groupby(df_na.status)
dfna_alive = grouped_na.get_group(0)
dfna_dead = grouped_na.get_group(1)

customdata = customdata = np.stack((df_na['age'], df_na['sex'],df_na['status'],df_na['wt.loss'],df_na['meal.cal'],df_na['ph.ecog'],df_na['ph.karno'],df_na['pat.karno']), axis=-1)

st.header("Influence of meal.cal on weight loss")

'''
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_na['meal.cal'], y=df_na['wt.loss'],customdata =customdata ,hovertemplate = hovertemplate , mode = 'markers',name='All Data')
)
fig.add_trace(go.Scatter(x=dfna_dead['meal.cal'], y=dfna_dead['wt.loss'],customdata =customdata ,hovertemplate = hovertemplate , mode = 'markers',name='Dead by the end of the experiment')
)

fig.add_trace(go.Scatter(x=dfna_alive['meal.cal'], y=dfna_alive['wt.loss'], customdata =customdata ,hovertemplate = hovertemplate ,mode = 'markers',name='Alive by the end of the experiment'))
fig.update_layout(
    yaxis_title='Wt.Loss',
    xaxis_title='Meal.Cal',
)
'''

fig = px.scatter(df_na, x="meal.cal", y="wt.loss", hover_data=df_na.columns)
fig.update_layout(
    yaxis_title='Wt.Loss',
    xaxis_title='Meal.Cal',
)
st.plotly_chart(fig)