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

# This page creates graphs to show the difference of average calories consumed by each age group

# "importing" the data
df = st.session_state['dic1']
df_dead = st.session_state['dicalive']
df_alive = st.session_state['dicdead']

# Setting the page header
st.header("Difference of calories consumed groupped by age")

# Here we created labels to show each age group and group them on the graphs
labels = ["39-45","45-50","50-55","55-60","60-65","65-70","70-75","75-82"]

# We used the pd.cur function to separate the people by age and then grouped them using the groupby function
# We also used the mean() function to calculate the mean of the groupped group
mean = df.groupby(pd.cut(df['age'], [39,45,50,55,60,65,70,75,82]),as_index=False).mean()
mean["AgeGroup"] = labels
mean_dead = df_dead.groupby(pd.cut(df_dead['age'],[39,45,50,55,60,65,70,75,82]),as_index=False).mean()
mean_dead["AgeGroup"] = labels
mean_alive = df_alive.groupby(pd.cut(df_alive['age'],[39,45,50,55,60,65,70,75,82]),as_index=False).mean()
mean_alive["AgeGroup"] = labels

# Then we created the bar graph using this new dataframe of groupped ages
fig = go.Figure()
# Adding a graph to the figure
fig.add_trace(go.Bar(x=mean['AgeGroup'],y=mean['meal.cal'],name='All data'))
# Adding a graph to the figure
fig.add_trace(go.Bar(x=mean_dead['AgeGroup'],y=mean_dead['meal.cal'],name='Dead by the end of the experiment'))
# Adding a graph to the figure
fig.add_trace(go.Bar(x=mean_alive['AgeGroup'],y=mean_alive['meal.cal'],name='Alive by the end of the experiment'))
# Labeling the y and x axis
fig.update_layout(
    yaxis_title='average calories per meal',
    xaxis_title='Age',

    boxmode='group' # group together boxes of the different traces for each value of x
)
# Plotting the graph
st.plotly_chart(fig)