import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go

st.subheader("Medium calories per meal for a ecog evaluation across the data")
df = st.session_state['dic1'] 
df_alive = st.session_state['dicalive']
df_dead = st.session_state['dicdead'] 


fig = px.box(df, x="ph.ecog", y="meal.cal",points = "all" , hover_data=df.columns)
st.plotly_chart(fig)

fig = go.Figure()
fig.add_trace(
    go.Box(x=df['ph.ecog'],y=df['meal.cal'],
    name='All data'))

fig.add_trace(go.Box(x=df_dead['ph.ecog'],
                     y=df_dead['meal.cal'],
                     text = df.values,
                     name='Dead by the end of the experiment'))
fig.add_trace(go.Box(x=df_alive['ph.ecog'],y=df_alive['meal.cal'],name='Alive by the end of the experiment'))
            
fig.update_layout(
    yaxis_title='Meal.Cal',
    xaxis_title='Ph.Ecog    ',

    boxmode='group' # group together boxes of the different traces for each value of x
)
st.plotly_chart(fig)