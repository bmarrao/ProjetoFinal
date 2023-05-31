''' Does calorie consumption affect the survival time in lung cancer patients?'''

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls


#print(df)
#ADICIONAR BAR CHART COM CONSUMO CALORIAS E O TEMPO MEDIO DE SOBREVIVẼNCIA DE CADA UM
#print(df.isnull().sum())

dic = {}
st.header("Analysis of calories impact in the time that a person survives")
st.sidebar.title('Navigation')
df = st.session_state['dic']
df_na = st.session_state['dic_noNa']

num1 = st.sidebar.number_input('Calorias inferior') 
num2 = st.sidebar.number_input('Calorias superior')
array = (num1,num2)
arr = st.session_state['pergunta5']

# tem uns comportamentos estranhos ao testar valores
if st.sidebar.button('Add to graph'):
    arr.append(array)
    st.session_state['pergunta5']= arr
    kmf = KaplanMeierFitter()

    print(arr)


    for (n1,n2) in arr:
        dic[f'({n1},{n2})']= {}
        dic[f'({n1},{n2})']['status'] = []
        dic[f'({n1},{n2})']['time'] = []

    for index, row in df.iterrows():
        for (n1,n2) in arr:
            if row['meal.cal'] >= n1 and row['meal.cal']<= n2:
                dic[f'({n1},{n2})']['time'].append(row['time'])
                dic[f'({n1},{n2})']['status'].append(row['status'])
        

    for (n1,n2) in arr:
        ax = plt.subplot(111)
        if dic[f'({n1},{n2})']['time']:
            kmf.fit(durations = pd.DataFrame(dic[f'({n1},{n2})']['time']), event_observed = pd.DataFrame(dic[f'({n1},{n2})']['status']),label=f"{n1}-{n2}")
            kmf.survival_function_.plot(ax = ax)
        else :
            st.info(f"There is no data for input {n1} - {n2}")
            arr.remove((n1,n2))
            st.session_state['pergunta5']= arr

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

if st.button('Show calories relation in cph model in a graph'):


    cph = CoxPHFitter()
    cph.fit(df_na, duration_col = 'time', event_col = 'status')

    mpl_fig = plt.figure()

    plt.subplots(figsize = (10, 6))

    cph.plot_partial_effects_on_outcome(covariates = 'meal.cal',
                                        values = [0,200,500,1000,1500,2000,2500],
                                        cmap = 'coolwarm')

    cph2 = plt.gcf()

    py_fig = tls.mpl_to_plotly(cph2, resize=True)

    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )

    st.plotly_chart(py_fig)