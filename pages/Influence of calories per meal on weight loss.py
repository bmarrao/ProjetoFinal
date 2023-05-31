import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# In this page we make a scatter plot to show the inffluence on the meal calories and the patients weight loss


# We used the first dictionary created in the home page 
df_na = st.session_state['dic1']
grouped_na=df_na.groupby(df_na.status)
dfna_alive = grouped_na.get_group(0)
dfna_dead = grouped_na.get_group(1)

# Creating and puting a title on the sidebar
st.header("Influence of calories per meal on weight loss")

# Creating the scatter plot
fig = px.scatter(df_na, x="meal.cal", y="wt.loss", hover_data=df_na.columns)
# Labeling the y and x axis
fig.update_layout(
    yaxis_title='Weight loss (kg)',
    xaxis_title='Calories per meal',
)
# Plotting the graph
st.plotly_chart(fig)

# Create the figure
fig = go.Figure()
# Adding the graph to the figgure
fig.add_trace(go.Scatter(x=df_na['meal.cal'], y=df_na['wt.loss'], mode = 'markers',name='All Data')
)
fig.add_trace(go.Scatter(x=dfna_dead['meal.cal'], y=dfna_dead['wt.loss'], mode = 'markers',name='Dead by the end of the experiment')
)

fig.add_trace(go.Scatter(x=dfna_alive['meal.cal'], y=dfna_alive['wt.loss']   ,mode = 'markers',name='Alive by the end of the experiment'))
# Update axis
fig.update_layout(
    yaxis_title='Wt.Loss',
    xaxis_title='Meal.Cal',
)
# Show the graph
st.plotly_chart(fig)
