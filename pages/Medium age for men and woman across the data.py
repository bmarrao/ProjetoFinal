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

# in this page he show the boxplots relating the sex and age
st.subheader("Medium age for men and woman across the data")
#we use the dic1 dictionary created in the home page
df = st.session_state['dic1'] 
df_alive = st.session_state['dicalive']
df_dead = st.session_state['dicdead'] 

#plotting a different version of the same boxplot
fig = px.box(df, color = "sex" ,x="sex", y="age", points="all",hover_data=df.columns)
fig.update_layout(
    yaxis_title='Age',
    xaxis_title='Sex : 0 - Men , 1 - Women',
    boxmode='group' # group together boxes of the different traces for each value of x
) 
st.plotly_chart(fig)

#creating the figure
fig = go.Figure()
#adding a boxplot to the fugure of all the people
fig.add_trace(
    go.Box(x=df['sex'],y=df['age'],
    name='All data'))
     
#adding a boxplot to the fugure of the dead people
fig.add_trace(go.Box(x=df_dead['sex'],y=df_dead['age'],name='Dead by the end of the experiment'))
#adding a boxplot to the fugure of the alive people
fig.add_trace(go.Box(x=df_alive['sex'],y=df_alive['age'],name='Alive by the end of the experiment'))
#updating axis
fig.update_layout(
    yaxis_title='Age',
    xaxis_title='Sex : 0 - Men , 1 - Women',
    boxmode='group' # group together boxes of the different traces for each value of x
)

#updating graphs
fig.update_traces(legendgroup='group')

#plotting the graphs
st.plotly_chart(fig)

