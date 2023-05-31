import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go

# This page shows a simple graph of the difference of the patients own karnofsky evaluation compared to the medic evaluation

# Setting the page header
st.subheader("Difference of Karnofsky evalutation from patiests to medic")
# "importing" the data
df = st.session_state['dic1'] 

# Creation of the graph
fig = px.box(df, x='ph.karno', y='pat.karno', points = "all", hover_data=df.columns)

fig.update_layout(
    yaxis_title='Patient Karnofsky evaluation',
    xaxis_title = 'Doctor Karnofsky evaluation',
)
# Plotting the graph
st.plotly_chart(fig)