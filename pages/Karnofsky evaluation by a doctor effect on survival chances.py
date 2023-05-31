import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter, KaplanMeierFitter
import plotly.tools as tls   
import plotly.express as px
from pylab import rcParams

# In this page we created graphs to show the influence of the doctors Karnofsky evaluation on the survival chances

# We used the noNa dictionary to not have na values for the cph model
df_na = st.session_state['dic_noNa']

# And the normal dictionary with all values for the simple plotting
df = st.session_state['dic']



dic = {}

# Setting the page header
st.header("Effect of Karnofsky evaluation by a doctor in survival time  ")
st.sidebar.title('Navigation')

# Here we created the button to receive the user inputs for the desired graph
num1 = st.sidebar.number_input("Lower Bound of a doctor's Karnofsky evaluation (min 0)")
num2 = st.sidebar.number_input("Upper Bound of a doctor's Karnofsky evaluation (max 100)")
array = (num1,num2)
# Using the pergunta3 dictionary created in the home page
arr = st.session_state['pergunta3']

# When the add to graph button is pressed we plot the data based on the values that were given to the program

if st.sidebar.button('Add to graph'):
    #Here we add the data given by the user do the session state variable

    arr.append(array)
    st.session_state['pergunta3']= arr
    kmf = KaplanMeierFitter()

    # We needed to created auxiliary variables to store the desired age group and to prevent mixups in the data
    for (n1,n2) in arr:
        dic[f'({n1},{n2})']= {}
        dic[f'({n1},{n2})']['status'] = []
        dic[f'({n1},{n2})']['time'] = []
        
    # Here we store the desired ph karno and their data
    for index, row in df.iterrows():
        for (n1,n2) in arr:
            if row['ph.karno'] >= n1 and row['ph.karno']<= n2:
                dic[f'({n1},{n2})']['time'].append(row['time'])
                dic[f'({n1},{n2})']['status'].append(row['status'])
        
    # Finnaly we plot the data and the survival probabilities of that karnofsky group
    for (n1,n2) in arr:
        ax = plt.subplot(111)
        if dic[f'({n1},{n2})']['time']:
            #fitting the data given by the user to the Kaplam Meier model

            kmf.fit(durations = pd.DataFrame(dic[f'({n1},{n2})']['time']), event_observed = pd.DataFrame(dic[f'({n1},{n2})']['status']),label=f"{n1}-{n2}")
            #Ploting
            kmf.survival_function_.plot(ax = ax)
        else :
            st.info(f"There is no data for input {n1} - {n2}")
            arr.remove((n1,n2))
            st.session_state['pergunta3']= arr

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

    # In here we update our graph so that we can label the y and x axis .

    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )

    #plotting
    st.plotly_chart(py_fig)
 
    
   
#in this second part we use the cph model to create a graph of the survival probability by karnofsky score for aech day passed

if st.button('Effect of Karnofsky evaluation on CPH model '):
    #creating the model
    cph = CoxPHFitter()
    cph.fit(df_na, duration_col = 'time', event_col = 'status',formula= "ph.karno")
    #creating the figure
    mpl_fig = plt.figure()
    #plotting the partial effects on outcome for each karnofsky score
    cph.plot_partial_effects_on_outcome(covariates = 'ph.karno',
                                        values = [0,10,20,30,40,50,60,70,80,90,100],
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

#here we 
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

    ''' Graph where x-axis is the Karnofsky evaluation score and the y-axis how many the days in average a person survived '''
    st.bar_chart(graph1)

    ''' Graph where x-axis is the Karnofsky evaluation score and the y-axis the percentage of people that were alive by the end of the experiment '''
    st.bar_chart(graph2)


