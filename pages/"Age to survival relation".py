import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls  
import plotly.express as px

#from st_pages import Page, show_pages, add_page_title,show_pages_from_config


#st.set_page_config(page_title = "Relação da idade com sobrevivência" )

'''
filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)
'''
dic = {}
st.title("Survivor Analysis for lung cancer data")
st.header("Analysis of age impact in the time that a person survives")
st.sidebar.title('Navigation')
df = st.session_state['dic']

num1 = st.sidebar.number_input('Idade superior')
num2 = st.sidebar.number_input('Idade inferior')
array = (num1,num2)
#st.session_state['pergunta1'] = st.session_state['pergunta1'].append(array)
arr = st.session_state['pergunta1']


if st.sidebar.button('Add to graph'):
    arr.append(array)
    st.session_state['pergunta1']= arr
    kmf = KaplanMeierFitter()



    #Ta2 = pd.DataFrame()
    for index, row in df.iterrows():
        for (n1,n2) in arr[1:]:
            if row['age'] >= n1 and row['age']<= n2:
                if dic['({n1},{n2})']:
                    dic['({n1},{n2})']['time'].append(row['time'])
                    dic['({n1},{n2})']['status'].append(row['status'])
                else :
                    dic['({n1},{n2})']['time'] =[row['time']]
                    dic['({n1},{n2})']['status'] =[row['status']]



    print(dic)
        #print(row['time'], row['status'])

    for (n1,n2) in arr[1:]:
        ax = plt.subplot(111)
        kmf.fit(durations = pd.DataFrame(dic['({n1},{n2})']['time']), event_observed = pd.DataFrame(dic['({n1},{n2})']['status']),label="{num1}{num2}")
        kmf.survival_function_.plot(ax = ax)


    #kmf.plot_survival_function(ax = ax
    kmf2 = plt.gcf()

    py_fig = tls.mpl_to_plotly(kmf2, resize=True)

    #kmf.plot_survival_function(ax = ax,at_risk_counts = True)


    st.plotly_chart(py_fig)






cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula= "age + sex + ph.ecog + ph.karno")

mpl_fig = plt.figure()

cph.plot_partial_effects_on_outcome(covariates = 'age',
                                    values = [30,40,50, 60, 70, 80],
                                    cmap = 'coolwarm')
                    

cph2 = plt.gcf()

py_fig = tls.mpl_to_plotly(cph2, resize=True)

st.plotly_chart(py_fig)

