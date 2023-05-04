import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls 

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df = st.session_state['dic']

num1 = st.sidebar.number_input('Instituicao desejada')

array = num1

arr = st.session_state['pergunta9']

dataf = {}



insts = []




for index, row in df.iterrows():
    if row['inst'] not in insts:
        insts.append(row['inst'])

print(insts)


for a in insts:
    Ta = {'time':[]}
    Ea = {'status':[]}
    dataf[a] = [Ta,Ea]



for index, row in df.iterrows():
    dataf[row['inst']][0]['time'].append(row['time'])
    dataf[row['inst']][1]['status'].append(row['status'])

ax = plt.subplot()
kmf = KaplanMeierFitter()


for a in insts:
    dataf[a][0] = pd.DataFrame(dataf[a][0])
    dataf[a][1] = pd.DataFrame(dataf[a][1])

    
    kmf.fit(durations = dataf[a][0], event_observed = dataf[a][1],label = "inst")
    kmf.survival_function_.plot(ax = ax)


figaux = plt.gcf()

py_fig = tls.mpl_to_plotly(figaux,resize = True)

st.plotly_chart(py_fig)



if st.sidebar.button('Add to graph'):
    arr.append(array)
    st.session_state['pergunta9']= arr
    ax2 = plt.subplot()
    kmf4 = KaplanMeierFitter()

    print(arr)

    for a in arr:
        #dataf[a][0] = pd.DataFrame(dataf[a][0])
        #dataf[a][1] = pd.DataFrame(dataf[a][1])

        
        kmf4.fit(durations = dataf[a][0], event_observed = dataf[a][1],label = "inst")
        kmf4.survival_function_.plot(ax = ax2)


    figaux3 = plt.gcf()

    py_fig2 = tls.mpl_to_plotly(figaux3,resize = True)

    st.plotly_chart(py_fig2)



S