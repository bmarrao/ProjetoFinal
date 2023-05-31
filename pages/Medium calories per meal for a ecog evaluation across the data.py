import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go

#in this page we created various boxplots to show the coorelation between calories consumed and the ecog evaluation of a patient

st.subheader("Medium calories per meal for a ecog evaluation across the data")
#using the dic1 created on the home page
df = st.session_state['dic1'] 
df_alive = st.session_state['dicalive']
df_dead = st.session_state['dicdead'] 

#creating boxplot of the ecog evaluation and calories consumed
fig = px.box(df, x="ph.ecog", y="meal.cal",points = "all" , hover_data=df.columns)
#plotting the figure
st.plotly_chart(fig)

#creating alternative plot and adding it to the figure
fig = go.Figure()
fig.add_trace(
    go.Box(x=df['ph.ecog'],y=df['meal.cal'],
    name='All data'))
#adding the boxplot of dead people to the figure
fig.add_trace(go.Box(x=df_dead['ph.ecog'],
                     y=df_dead['meal.cal'],
                     text = df.values,
                     name='Dead by the end of the experiment'))
#adding boxplot of alive people to the figure
fig.add_trace(go.Box(x=df_alive['ph.ecog'],y=df_alive['meal.cal'],name='Alive by the end of the experiment'))
#updating axis
fig.update_layout(
    yaxis_title='Calories per meal',
    xaxis_title='Ecog evaluation ',

    boxmode='group' # group together boxes of the different traces for each value of x
)
#plotting the figure
st.plotly_chart(fig)