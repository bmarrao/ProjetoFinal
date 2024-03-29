import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls   
from plotly.graph_objs import *

from pylab import rcParams
dic = {}
st.header("Effect of weight loss in survival chances")
st.sidebar.title('Navigation')
#using the dic created on the home page
df = st.session_state['dic']
#creating input buttons
num1 = st.sidebar.number_input('Lower bound weight (Kg) ')
num2 = st.sidebar.number_input('Upper bound weight (Kg)')
array = (num1,num2)
arr = st.session_state['pergunta2']

#when added to graph button is pressed we get the desired data and plot it
if st.sidebar.button('Add to graph'):
    st.subheader("Kaplan-Maier Graph")
    arr.append(array)
    st.session_state['pergunta2']= arr
    kmf = KaplanMeierFitter()
    print(type(num1), type(num2))

    #creating new dictionaries
    for (n1,n2) in arr:
        dic[f'({n1},{n2})']= {}
        dic[f'({n1},{n2})']['status'] = []
        dic[f'({n1},{n2})']['time'] = []
    #adding data to them
    for index, row in df.iterrows():
        for (n1,n2) in arr:
            if row['wt.loss'] >= n1 and row['wt.loss']<= n2:
                dic[f'({n1},{n2})']['time'].append(row['time'])
                dic[f'({n1},{n2})']['status'].append(row['status'])
        
    #plotting the data using kaplan meier fitter
    for (n1,n2) in arr:
        ax = plt.subplot(111)
        if dic[f'({n1},{n2})']['time']:
            kmf.fit(durations = pd.DataFrame(dic[f'({n1},{n2})']['time']), event_observed = pd.DataFrame(dic[f'({n1},{n2})']['status']),label=f"{n1}-{n2}")
            kmf.survival_function_.plot(ax = ax)
        else :
            st.info(f"There is no data for input {n1} - {n2}")
            arr.remove((n1,n2))
            st.session_state['pergunta2']= arr
    #baseline
    T = df["time"]
    E = df["status"]
    ax = plt.subplot(111)
    kmf.fit(durations = T, event_observed =E,label=f"Baseline")
    kmf.survival_function_.plot(ax = ax)
    #kmf.plot_survival_function(ax = ax
    kmf2 = plt.gcf()

    py_fig = tls.mpl_to_plotly(kmf2, resize=True)

    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )
    #kmf.plot_survival_function(ax = ax,at_risk_counts = True)

    st.plotly_chart(py_fig)