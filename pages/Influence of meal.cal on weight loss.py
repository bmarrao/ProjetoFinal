import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

#in this page we make a scatterplot to show the inffluence on the meal calories and the patients weight loss


# we used the first dictionary created in the home page 
df_na = st.session_state['dic1']
grouped_na=df_na.groupby(df_na.status)
dfna_alive = grouped_na.get_group(0)
dfna_dead = grouped_na.get_group(1)


st.header("Influence of meal.cal on weight loss")

#create the figure
fig = go.Figure()
#adding the graph to the figgure
fig.add_trace(go.Scatter(x=df_na['meal.cal'], y=df_na['wt.loss'], mode = 'markers',name='All Data')
)
fig.add_trace(go.Scatter(x=dfna_dead['meal.cal'], y=dfna_dead['wt.loss'], mode = 'markers',name='Dead by the end of the experiment')
)

fig.add_trace(go.Scatter(x=dfna_alive['meal.cal'], y=dfna_alive['wt.loss']   ,mode = 'markers',name='Alive by the end of the experiment'))
#updating axis
fig.update_layout(
    yaxis_title='Wt.Loss',
    xaxis_title='Meal.Cal',
)
#showing th graph
st.plotly_chart(fig)
#
fig = px.scatter(df_na, x="meal.cal", y="wt.loss", hover_data=df_na.columns)
fig.update_layout(
    yaxis_title='Wt.Loss',
    xaxis_title='Meal.Cal',
)
st.plotly_chart(fig)