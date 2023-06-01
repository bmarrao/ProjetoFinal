import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls 

# In this page we create graphs to visualise the effects of each ECOG score on the survivability of the patient
# We used the noNA dataframe because the model doesn't accept null values

# "importing" the data
df = st.session_state['dic_noNa']

# We created 2 auxiliary variables to later use them to create the graphs

dataf = {}

ecogs = []

# We iterate on the values and add it into the variable if it's not present
for index, row in df.iterrows():
    if row['ph.ecog'] not in ecogs and row['ph.ecog']!= 3:
        ecogs.append(row['ph.ecog'])
# Then we create dictionaries for each ECOG evaluation to then add values into them to be able to plot the later
for a in ecogs:
    Ta = {'time':[]}
    Ea = {'status':[]}
    dataf[a] = [Ta,Ea]
# We add each ECOG score into it's own corresponding dictionary
for index, row in df.iterrows():
    if row["ph.ecog"] != 3:
        dataf[row['ph.ecog']][0]['time'].append(row['time'])
        dataf[row['ph.ecog']][1]['status'].append(row['status'])
# Then we create the kaplanmeierfilter
ax = plt.subplot()
# Plotting the graph
kmf = KaplanMeierFitter()


# Finnaly for each ECOG score we create the graph accordingly
for a in ecogs:
    
    dataf[a][0] = pd.DataFrame(dataf[a][0])
    dataf[a][1] = pd.DataFrame(dataf[a][1])

    
    kmf.fit(durations = dataf[a][0], event_observed = dataf[a][1],label = "ecog" + str(a))
    kmf.survival_function_.plot(ax = ax)
# We also created the baseline to give a comparison for each ECOG score
T = df["time"]
E = df["status"]
ax = plt.subplot(111)
kmf.fit(durations = T, event_observed =E,label=f"Baseline")
kmf.survival_function_.plot(ax = ax)

#Receiving data from the figure
figaux = plt.gcf()

st.subheader("Kaplan-Maier Graph")

#Turning that data into a plotly graph so that we can add interactivity 
py_fig = tls.mpl_to_plotly(figaux,resize = True)
py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )
# Plotting the graph
st.plotly_chart(py_fig)

st.subheader("Cox Model Graph")


# We also used the Cox Proportional Hazard Model to show the impacts of the score on the survivability chance
cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')


fig, ax = plt.subplots()

# Here we plot the partial effects on outcome
cph.plot_partial_effects_on_outcome(covariates = 'ph.ecog',
                                    values = [0,1,2,3],
                                    cmap = 'coolwarm')

figaux = plt.gcf()
# Change the axis names and finnaly show the graph
py_fig = tls.mpl_to_plotly(figaux,resize = True)
py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )
# Plotting the graph
st.plotly_chart(py_fig)