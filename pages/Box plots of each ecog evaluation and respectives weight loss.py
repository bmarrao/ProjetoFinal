import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go

# in this page we display a few boxplots to show the coorelation between patients ecog evaluation 

df = st.session_state['dic1'] 
df_alive = st.session_state['dicalive']
df_dead = st.session_state['dicdead'] 

st.header("Box plots of each ecog evaluation and respectives weight loss")



fig = go.Figure()

# we created 3 boxplots groups to easier visualise the variyng coorelations between those who 
# stayed alive by the end of the experiment and for those who didn't

fig.add_trace( go.Box(x=df["ph.ecog"], y=df["wt.loss"], name='All patients'))


fig.add_trace( go.Box(x=df_alive["ph.ecog"], y=df_alive["wt.loss"] , name='Alive by the end of the experiment'))


fig.add_trace( go.Box(x=df_dead["ph.ecog"], y=df_dead["wt.loss"] , name='Dead by the end of the experiment'))

fig.update_layout(
    yaxis_title='wt.loss',
    xaxis_title='Ph.Ecog    ',

    boxmode='group' # group together boxes of the different traces for each value of x
)
st.plotly_chart(fig)