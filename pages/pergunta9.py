import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls 

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)
'''
df["inst"].fillna(100.00, inplace = True)
df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
#df["ph.ecog"] = df["ph.ecog"].astype("int64")
df["ph.ecog"].fillna(df["ph.ecog"].mean(), inplace = True)
'''


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






if st.button('Show difference of institution to survival rate using cph model'):
    cph = CoxPHFitter()
    cph.fit(df, duration_col = 'time', event_col = 'status')

    fig, ax = plt.subplots()

    cph.plot_partial_effects_on_outcome(covariates = 'inst',
                                        values = [a for a in insts],
                                        cmap = 'coolwarm')





    figaux = plt.gcf()

    py_fig = tls.mpl_to_plotly(figaux,resize = True)

    st.plotly_chart(py_fig)

