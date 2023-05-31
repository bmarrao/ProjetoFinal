import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go

#in this page we create 2 donut graphs to show the percentage of the mean calories consumed by each karnofsky score group

st.subheader("Relation between Karnofsky evalution by a pacient or a doctor and calories consumed")
#we use the dic1 created on the home page
df = st.session_state['dic1'] 
#we create the labels to be able to gruoup each value of karnofsky score
labels = ['40','50','60','70','80','90','100']

#we use the pd.cut() and groupby() funtions to group each karnovsky score group given by the medic and calculate their means in calories consumed
mean = df.groupby(pd.cut(df['ph.karno'],[30,40,50,60,70,80,90,100]),as_index=False).mean()
mean["ph.karn"] = labels



''' The caption on the side of the donut refers to the Medic Evaluation of the Karnofsky score for each patient, and in the donnut the percentage of the sum of the mean calories consumed by each group 
'''
#we create the donut graph and add it to the figure
fig = px.pie(mean, values='meal.cal', names='ph.karn', title='Medic Evaluation compared to calories consumed',hole = 0.4)
fig.update_traces(textposition='inside', textinfo='percent+label')
#plotting the graph
st.plotly_chart(fig)


labels = ['40','50','60','70','80','90','100']
#we use the pd.cut() and groupby() funtions to group each karnovsky score group given by the patient and calculate their means in calories consumed

mean = df.groupby(pd.cut(df['pat.karno'],[30,40,50,60,70,80,90,100]),as_index=False).mean()
mean["pat.karn"] = labels

''' The caption on the side of the donut refers to the Patient Evaluation of the Karnofsky score , and in the donut
 the percentage of the sum of the mean calories consumed by each group 
'''
#we create the donut graph and add it to the figure
fig = px.pie(mean, values='meal.cal', names='pat.karn', title='Patient Evaluation compared to calories consumed',hole = 0.4)
fig.update_traces(textposition='inside', textinfo='percent+label')
#plotting the graph
st.plotly_chart(fig)
