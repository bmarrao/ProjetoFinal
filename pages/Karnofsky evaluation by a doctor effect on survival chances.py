import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls   
import plotly.express as px
from pylab import rcParams

#in this page we created graphs to show the inffluence of the doctors karnofsky evaluation on the survival chances

#we used the noNa dictionary to not have na values for the cph model
df_na = st.session_state['dic_noNa']

# and the normal dictionary with all values for the simple plotting
df = st.session_state['dic']



dic = {}


st.header("Effect of Karnofsky evaluation by a doctor in survival time : ")
st.sidebar.title('Navigation')

# here we created the button to receive the user inputs for the desired graph
num1 = st.sidebar.number_input('Lower Bound ph karno (min 0)')
num2 = st.sidebar.number_input('Upper Bound ph karno (max 3)')
array = (num1,num2)
# using the per
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
            kmf.fit(durations = pd.DataFrame(dic[f'({n1},{n2})']['time']), event_observed = pd.DataFrame(dic[f'({n1},{n2})']['status']),label=f"{n1}-{n2}")
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


    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )
    #kmf.plot_survival_function(ax = ax,at_risk_counts = True)


    st.plotly_chart(py_fig)



    st.plotly_chart(py_fig)    
    



    #kmf.plot_survival_function(ax = ax
   


if st.button('Effect of Karnofsky evaluation on CPH model '):

    cph = CoxPHFitter()
    cph.fit(df_na, duration_col = 'time', event_col = 'status',formula= "ph.karno")

    mpl_fig = plt.figure()

    cph.plot_partial_effects_on_outcome(covariates = 'ph.karno',
                                        values = [0,10,20,30,40,50,60,70,80,90,100],
                                        cmap = 'coolwarm')



    cph2 = plt.gcf()

    py_fig = tls.mpl_to_plotly(cph2, resize=True)

    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )

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

    ''' Graph where x-axis is the Karnofsky coefficient and the y-axis how many the days in average a person survived '''
    st.bar_chart(graph1)

    ''' Graph where x-axis is the Karnofsky coefficient and the y-axis the percentage of people that were alive by the end of the experiment '''
    st.bar_chart(graph2)


