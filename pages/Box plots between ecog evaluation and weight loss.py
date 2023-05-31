import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go

# In this page we display a few boxplots to show the correlation between patients ecog evaluation 

# "importing" the data
df = st.session_state['dic1'] 
df_alive = st.session_state['dicalive']
df_dead = st.session_state['dicdead'] 
# Setting the page header
st.header("Box plots between ecog evaluation and weight loss")



fig = go.Figure()

# We created 3 boxplot groups to facilitate the visualization of the different correlations between 
# those who stayed alive by the end of the experiment and those who did not

# Adding a graph to the figure
fig.add_trace( go.Box(x=df["ph.ecog"], y=df["wt.loss"], name='All patients'))

# Adding a graph to the figure
fig.add_trace( go.Box(x=df_alive["ph.ecog"], y=df_alive["wt.loss"] , name='Alive by the end of the experiment'))

# Adding a graph to the figure
fig.add_trace( go.Box(x=df_dead["ph.ecog"], y=df_dead["wt.loss"] , name='Dead by the end of the experiment'))

# Labeling the y and x axis
fig.update_layout(
    yaxis_title='Weight Loss (KG)',
    xaxis_title='Ecog evaluation ',

    boxmode='group' # group together boxes of the different traces for each value of x
)
st.plotly_chart(fig)