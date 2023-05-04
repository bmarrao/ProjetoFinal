import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter
import plotly.tools as tls 



df = st.session_state['dic']

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls   
from plotly.graph_objs import *

from pylab import rcParams
dic = {}
df_dead = st.session_state['dic dead']
df_alive = st.session_state['dic alive']
st.header("Effect of Karnofsky evaluation by a doctor in survival time : ")
st.sidebar.title('Navigation')

df = st.session_state['dic']

num1 = st.sidebar.number_input('Ph karno inferior :')
num2 = st.sidebar.number_input('Ph karno superior : ')
array = (num1,num2)
arr = st.session_state['pergunta3']


if st.sidebar.button('Add to graph'):
    arr.append(array)
    st.session_state['pergunta3']= arr
    kmf = KaplanMeierFitter()


    for (n1,n2) in arr:
        dic[f'({n1},{n2})']= {}
        dic[f'({n1},{n2})']['status'] = []
        dic[f'({n1},{n2})']['time'] = []

    for index, row in df.iterrows():
        for (n1,n2) in arr:
            if row['ph.karno'] >= n1 and row['ph.karno']<= n2:
                dic[f'({n1},{n2})']['time'].append(row['time'])
                dic[f'({n1},{n2})']['status'].append(row['status'])
        

    for (n1,n2) in arr:
        ax = plt.subplot(111)
        if dic[f'({n1},{n2})']['time']:
            kmf.fit(durations = pd.DataFrame(dic[f'({n1},{n2})']['time']), event_observed = pd.DataFrame(dic[f'({n1},{n2})']['status']),label=f"{num1}-{num2}")
            kmf.survival_function_.plot(ax = ax)
        else :
            st.info(f"There is no data for input {n1} - {n2}")
            arr.remove((n1,n2))
            st.session_state['pergunta3']= arr

    T = df["time"]
    E = df["status"]
    ax = plt.subplot(111)
    kmf.fit(durations = T, event_observed =E,label=f"Baseline")
    kmf.survival_function_.plot(ax = ax)

    kmf2 = plt.gcf()

    py_fig = tls.mpl_to_plotly(kmf2, resize=True)

    #kmf.plot_survival_function(ax = ax,at_risk_counts = True)


    st.plotly_chart(py_fig)



    st.plotly_chart(py_fig)    
    



    #kmf.plot_survival_function(ax = ax
   


if st.button('Effect of Karnofsky evaluation on CPH model '):

    df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
    df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
    df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
    df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
    df.dropna(inplace=True)
    df["ph.ecog"] = df["ph.ecog"].astype("int64")
    df = df.reset_index() 
    cph = CoxPHFitter()
    cph.fit(df, duration_col = 'time', event_col = 'status',formula= "ph.karno")

    mpl_fig = plt.figure()

    cph.plot_partial_effects_on_outcome(covariates = 'ph.karno',
                                        values = [0,10,20,30,40,50,60,70,80,90,100],
                                        cmap = 'coolwarm')



    cph2 = plt.gcf()

    py_fig = tls.mpl_to_plotly(cph2, resize=True)

    st.plotly_chart(py_fig)

if st.button('Survival probability given a Karnofsky evaluation by a doctor '):


    dict =  {'died': {'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []},'alive':{'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []}}

    for index, row in df.iterrows():
        if row['ph.karno'] >= 0 and row['ph.karno'] < 10 :
            if row['status'] == 1 :
                dict['died']['0-10'].append(row['time'])
            else :
                dict['alive']['0-10'].append(row['time'])
        elif row['ph.karno'] >= 10 and row['ph.karno'] < 20:
            if row['status'] == 1 :
                dict['died']['10-20'].append(row['time'])
            else :
                dict['alive']['10-20'].append(row['time'])
        elif row['ph.karno'] >= 20 and row['ph.karno'] <30:
            if row['status'] == 1 :
                dict['died']['20-30'].append(row['time'])
            else :
                dict['alive']['20-30'].append(row['time'])
        elif row['ph.karno'] >= 30 and row['ph.karno'] < 40:
            if row['status'] == 1 :
                dict['died'] ['30-40'].append(row['time'])
            else :
                dict['alive']['30-40'].append(row['time'])
        elif row['ph.karno'] >= 40 and row['ph.karno'] < 50:
            if row['status'] == 1 :
                dict['died'] ['40-50'].append(row['time'])
            else :
                dict['alive']['40-50'].append(row['time']) 
        elif row['ph.karno'] >= 50 and row['ph.karno'] < 60:
            if row['status'] == 1 :
                dict['died'] ['50-60'].append(row['time'])
            else :
                dict['alive']['50-60'].append(row['time'])  
        elif row['ph.karno'] >= 60 and row['ph.karno'] <70:
            if row['status'] == 1 :
                dict['died'] ['60-70'].append(row['time'])
            else :
                dict['alive']['60-70'].append(row['time'])
        elif row['ph.karno'] >= 70 and row['ph.karno'] < 80:
            if row['status'] == 1 :
                dict['died'] ['70-80'].append(row['time'])
            else :
                dict['alive']['70-80'].append(row['time']) 
        elif row['ph.karno'] >= 80 and row['ph.karno'] <= 90:
            if row['status'] == 1 :
                dict['died']['80-90'].append(row['time'])
            else :
                dict['alive']['80-90'].append(row['time']) 
        else:
            if row['status'] == 1 :
                dict['died'] ['90-100'].append(row['time'])
            else :
                dict['alive']['90-100'].append(row['time'])  

    remove = []
    porcentagem ={'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []}
    for i in ['0-10' , '10-20', '20-30' , '30-40' , '40-50' , '50-60' , '60-70' , '70-80' , '80-90' , '90-100'] :
        x = len(dict['alive'][i]) + len(dict['died'][i])
        if x:
            porcentagem[i] = (len(dict['alive'][i])  / x) * 100
            dict['died'][i] = (sum(dict['died'][i])  / len(dict['died'][i]))
            dict['alive'][i] = (sum(dict['alive'][i])  / len(dict['alive'][i]))


        else :
            remove.append(i)

    for i in remove :
        dict['died'].pop(i)
        dict['alive'].pop(i)
        porcentagem.pop(i)

    graph1 = pd.DataFrame.from_dict(dict,orient='index').transpose()
    graph2 = pd.DataFrame.from_dict(porcentagem,orient='index')

    st.bar_chart(graph1)

    st.bar_chart(graph2)


