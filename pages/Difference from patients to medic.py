import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go

# this page show a simple graph of the difference that the patients own karnofsky evaluation compares to the medic evaluaton

st.subheader("Difference from patiests to medic")
df = st.session_state['dic1'] 

#creation of the graph
fig = px.box(df, x='ph.karno', y='pat.karno', points = "all", hover_data=df.columns)
st.plotly_chart(fig)