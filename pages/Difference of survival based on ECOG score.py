import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls 

#in this page we create graphs to visuaise the effects of each ecog score on the survivability of the patient
#we used the noNA dataframe because the model doesnt accept null values
df = st.session_state['dic_noNa']

#we created 2 auxiliary variables to later use them to create the graphs

dataf = {}

ecogs = []

#we iterate on the values and add it into the variable if its not present
for index, row in df.iterrows():
    if row['ph.ecog'] not in ecogs:
        ecogs.append(row['ph.ecog'])
#then we create dictionaries for each ecog evaluation to then add values into them to be able to plot the later
for a in ecogs:
    Ta = {'time':[]}
    Ea = {'status':[]}
    dataf[a] = [Ta,Ea]
#we add each ecog score into its own corresponding dictionary
for index, row in df.iterrows():
    dataf[row['ph.ecog']][0]['time'].append(row['time'])
    dataf[row['ph.ecog']][1]['status'].append(row['status'])
#then we create the kaplanmeierfilter
ax = plt.subplot()
kmf = KaplanMeierFitter()


#and finnaly for each ecog score we create the graph accordingly
for a in ecogs:
    
    dataf[a][0] = pd.DataFrame(dataf[a][0])
    dataf[a][1] = pd.DataFrame(dataf[a][1])

    
    kmf.fit(durations = dataf[a][0], event_observed = dataf[a][1],label = "ecog" + str(a))
    kmf.survival_function_.plot(ax = ax)
#we also created the baseline to give a comparison for each ecog score
T = df["time"]
E = df["status"]
ax = plt.subplot(111)
kmf.fit(durations = T, event_observed =E,label=f"Baseline")
kmf.survival_function_.plot(ax = ax)

figaux = plt.gcf()

py_fig = tls.mpl_to_plotly(figaux,resize = True)
py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )
st.plotly_chart(py_fig)


# we also used the Cox Proportional Hazard Model to show the impacts of the score on the survivability chance

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')


fig, ax = plt.subplots()

#here we plot the partial effects on outcome
cph.plot_partial_effects_on_outcome(covariates = 'ph.ecog',
                                    values = [0,1,2,3],
                                    cmap = 'coolwarm')

figaux = plt.gcf()
#change the axis names and finnaly show the graph
py_fig = tls.mpl_to_plotly(figaux,resize = True)
py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )
st.plotly_chart(py_fig)