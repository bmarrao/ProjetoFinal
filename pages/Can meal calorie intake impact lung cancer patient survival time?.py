''' O consumo de calorias nas refeições afeta o tempo de sobrevivência em pacientes com
cancro de pulmão? - 5'''

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls

'''filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)'''
#print(df)
#ADICIONAR BAR CHART COM CONSUMO CALORIAS E O TEMPO MEDIO DE SOBREVIVẼNCIA DE CADA UM
#print(df.isnull().sum())

'''
df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
'''
dic = {}
st.header("Analysis of calories impact in the time that a person survives")
st.sidebar.title('Navigation')
df = st.session_state['dic']

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


    for (n1,n2) in arr[1:]:
        dic[f'({n1},{n2})']= {}
        dic[f'({n1},{n2})']['status'] = []
        dic[f'({n1},{n2})']['time'] = []

    for index, row in df.iterrows():
        for (n1,n2) in arr[1:]:
            if row['meal.cal'] >= n1 and row['meal.cal']<= n2:
                dic[f'({n1},{n2})']['time'].append(row['time'])
                dic[f'({n1},{n2})']['status'].append(row['status'])
        

    for (n1,n2) in arr[1:]:
        ax = plt.subplot(111)
        kmf.fit(durations = pd.DataFrame(dic[f'({n1},{n2})']['time']), event_observed = pd.DataFrame(dic[f'({n1},{n2})']['status']),label=f"{num1}-{num2}")
        kmf.survival_function_.plot(ax = ax)


    #kmf.plot_survival_function(ax = ax
    kmf2 = plt.gcf()

    py_fig = tls.mpl_to_plotly(kmf2, resize=True)

    #kmf.plot_survival_function(ax = ax,at_risk_counts = True)


    st.plotly_chart(py_fig)

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

mpl_fig = plt.figure()

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'meal.cal',
                                    values = [0,200,500,1000,1500,2000,2500],
                                    cmap = 'coolwarm')

cph2 = plt.gcf()

py_fig = tls.mpl_to_plotly(cph2, resize=True)

st.plotly_chart(py_fig)