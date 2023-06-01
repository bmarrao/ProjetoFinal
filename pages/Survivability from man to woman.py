'''Is there a significant difference in survival time between men and women with lung cancer? 
And after controlling other covariates such as age, ECOG performance status, or Karnofsky score?'''

import pandas as pd
import matplotlib.pyplot as plt                  
import streamlit as st
from lifelines import CoxPHFitter,KaplanMeierFitter
import plotly.tools as tls   
from plotly.graph_objs import *

# in this page we compare the survival chance and time of men and women

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)
st.title("Survivability from man to woman")


df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
df = df.reset_index() 
df['status'] = df["status"]-1

#creating the kaplan meier fitter
kmf = KaplanMeierFitter()
Ta1 = {'time':[]}
Ta2 = {'time':[]}
#baseline creation
T = {'time':[]}
E = {'status':[]}

Ea1 = {'status':[]}
Ea2 = {'status':[]}
# iterating on the data and separating men and women
for index, row in df.iterrows():
    if row['sex'] == 1:
        Ta1['time'].append(row['time'])
        Ea1['status'].append(row['status'])
    elif row['sex'] == 2:
        Ta2['time'].append(row['time'])
        Ea2['status'].append(row['status'])

Ta1 = pd.DataFrame(Ta1)
Ea1 = pd.DataFrame(Ea1)
Ta2 = pd.DataFrame(Ta2)
Ea2 = pd.DataFrame(Ea2)
ax = plt.subplot(111)
# kaplan meier fitter creation for men
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="Homem")
#plotting function
kmf.survival_function_.plot(ax = ax)

ax = plt.subplot(111)
# kaplan meier fitter creation for women
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta2, event_observed = Ea2,label="Mulher")
#plotting
kmf.survival_function_.plot(ax = ax)
T = df["time"]
E = df["status"]
ax = plt.subplot(111)
kmf.fit(durations = T, event_observed =E,label=f"Baseline")
kmf.survival_function_.plot(ax = ax)
plt.title("Survival of different gender group")

st.subheader("Kaplan-Maier Graph")

kmf2 = plt.gcf()

py_fig = tls.mpl_to_plotly(kmf2, resize=True)
#updating figure
py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )
st.plotly_chart(py_fig)
# removing na values for cox model
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
df = df.reset_index()
# creating model
cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

mpl_fig = plt.figure()

cph.plot_partial_effects_on_outcome(covariates = 'sex',
                                    values = [1,2],
                                    cmap = 'coolwarm')

cph2 = plt.gcf()
#changing plot format
py_fig = tls.mpl_to_plotly(cph2, resize=True)
#updating layout
py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )
st.subheader("Cox Model Graph")


st.plotly_chart(py_fig)