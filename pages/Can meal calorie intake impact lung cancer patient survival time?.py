''' Does calorie consumption affect the survival time in lung cancer patients?'''

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls

# In this page we made graphs to illustrate the impact that age has on the survivability of the patients
dic = {}
# Setting the page header
st.header("Analysis of calories impact in the time that a person survives")
# Creating and puting a title on the sidebar
st.sidebar.title('Navigation')
# "importing" the data
df = st.session_state['dic']
df_na = st.session_state['dic_noNa']

# We created the input to let the user create and visualise different values based on his choice
num1 = st.sidebar.number_input('Calorias inferior') 
num2 = st.sidebar.number_input('Calorias superior')
array = (num1,num2)
# Reading the data previously given by the user
arr = st.session_state['pergunta5']

# When the add to graph button is pressed we plot the data based on the values that were given to the program
if st.sidebar.button('Add to graph'):
    #Here we add the data given by the user do the session state variable
    arr.append(array)
    st.session_state['pergunta5']= arr
    #Initializing the Kaplan Meier model Fitter 
    kmf = KaplanMeierFitter()

    # We needed to created auxiliary variables to store the desired age group and to prevent mixups in the data
    for (n1,n2) in arr:
        dic[f'({n1},{n2})']= {}
        dic[f'({n1},{n2})']['status'] = []
        dic[f'({n1},{n2})']['time'] = []

    # Here we store the desired age groups and their data
    for index, row in df.iterrows():
        for (n1,n2) in arr:
            if row['meal.cal'] >= n1 and row['meal.cal']<= n2:
                dic[f'({n1},{n2})']['time'].append(row['time'])
                dic[f'({n1},{n2})']['status'].append(row['status'])
        
    # Finnaly we plot the data and the survival probabilities of that age group
    for (n1,n2) in arr:
        ax = plt.subplot(111)
        if dic[f'({n1},{n2})']['time']:
            # Fitting the data given by the user to the Kaplam Meier model
            kmf.fit(durations = pd.DataFrame(dic[f'({n1},{n2})']['time']), event_observed = pd.DataFrame(dic[f'({n1},{n2})']['status']),label=f"{n1}-{n2}")
            # Plotting
            kmf.survival_function_.plot(ax = ax)
        else :
            st.info(f"There is no data for input {n1} - {n2}")
            arr.remove((n1,n2))
            st.session_state['pergunta5']= arr

    #Creating the baseline
    T = df["time"]
    E = df["status"]
    ax = plt.subplot(111)
    kmf.fit(durations = T, event_observed =E,label=f"Baseline")
    kmf.survival_function_.plot(ax = ax)

    #Receiving data from the figure
    kmf2 = plt.gcf()

    #Turning that data into a plotly graph so that we can add interactivity
    py_fig = tls.mpl_to_plotly(kmf2, resize=True)

    # In here we update our graph so that we can label the y and x axis
    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )


    st.plotly_chart(py_fig)

# In this second part we use the cph model to create a graph of the survival probability by age group for each day passed
if st.button('Show calories relation in cph model in a graph'):


    cph = CoxPHFitter()
    cph.fit(df_na, duration_col = 'time', event_col = 'status')

    mpl_fig = plt.figure()

    plt.subplots(figsize = (10, 6))

    cph.plot_partial_effects_on_outcome(covariates = 'meal.cal',
                                        values = [0,200,500,1000,1500,2000,2500],
                                        cmap = 'coolwarm')

    #Receiving data from the figure
    cph2 = plt.gcf()
    #Turning that data into a plotly graph so that we can add interactivity 
    py_fig = tls.mpl_to_plotly(cph2, resize=True)
    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )

    st.plotly_chart(py_fig)