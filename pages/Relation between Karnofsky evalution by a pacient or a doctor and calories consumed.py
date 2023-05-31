import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px
import plotly.graph_objects as go

st.subheader("Relation between Karnofsky evalution by a pacient or a doctor and calories consumed")
df = st.session_state['dic1'] 

labels = ['40','50','60','70','80','90','100']

mean = df.groupby(pd.cut(df['ph.karno'],[30,40,50,60,70,80,90,100]),as_index=False).mean()
mean["ph.karn"] = labels


labels = ['40','50','60','70','80','90','100']

mean = df.groupby(pd.cut(df['ph.karno'],[30,40,50,60,70,80,90,100]),as_index=False).mean()
mean["ph.karn"] = labels

''' The caption on the side of the donut refers to the Medic Evaluation on a patient and we have the percentage of people 
with the given evaluation and the mean of calories consumed'''

fig = px.pie(mean, values='meal.cal', names='ph.karn', title='Medic Evaluation compared to calories consumed',hole = 0.4)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)

labels = ['40','50','60','70','80','90','100']

mean = df.groupby(pd.cut(df['pat.karno'],[30,40,50,60,70,80,90,100]),as_index=False).mean()
mean["pat.karn"] = labels

''' The caption on the side of the donut refers to the Patient Evaluation that the patient itself gave and we have the percentage of people 
with the given evaluation and the mean of calories consumed'''

fig = px.pie(mean, values='meal.cal', names='pat.karn', title='Patient Evaluation compared to calories consumed',hole = 0.4)
fig.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig)
