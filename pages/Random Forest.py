import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import plotly.tools as tls   

from sklearn.model_selection import train_test_split
from sksurv.ensemble import RandomSurvivalForest

# in this page we used the survival forests model to predict the survivability chance of a patient and plot it on a graph

#we used the noNa dictionary because the random forests model doesnt accept this type of value
df_na = st.session_state['dic_noNa']


arr = st.session_state['random_forest']

#we asked the user to input the data to make a prediction based on the values the user wants
num2 = st.sidebar.number_input('Age : ')
num3 = st.sidebar.number_input('Sex(0 - homem, 1 - mulher) :')
num4 = st.sidebar.number_input('ECOG (0-4):')
num5 = st.sidebar.number_input('Karnofsky evaluation by doctor (0-100) :')
num6 = st.sidebar.number_input('Karnofsky evaluation by patient (0-100) :')
num7 = st.sidebar.number_input('Calorias per meal : ')
num8 = st.sidebar.number_input('Weight loss (kg) : ')



st.subheader("Survival Forests")

#Preparing the data for the random forest , dividing into two differente data sets the y and x
lg_y = df_na[['status','time']].copy()

lg_y["status"] = lg_y["status"].astype("bool") 

lg_y = lg_y.to_records(index=False)

lg_x = df_na.drop(["status","time"],axis=1)

random_state = 20
#we train the model using all the values that are accepted
rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           n_jobs=-1,
                           random_state=random_state)
rsf.fit(lg_x, lg_y)
train_x = pd.DataFrame.from_dict(arr)

#When we recieve a set of values added by the user we use them to predict the survival chance and the cumulative hazzard using the created model
if st.sidebar.button('Add to graph'):
    #create figure
    mpl_fig = plt.figure()
    #gettinf the inputed values and adding them to a variable
    array = {'age' : num2  ,'sex': num3 ,'ph.ecog' : num4 , 'ph.karno' : num5 , 'pat.karno': num6 ,
             'meal.cal':num7,'wt.loss':num8}
    arr.append(array)
    #adding the data to the model
    train_x = pd.DataFrame.from_dict(arr)
    #updating the local dictionary
    st.session_state['random_forest']= arr

    
    #predicting the survival chance based on the model and plotting it
    surv = rsf.predict_survival_function(train_x, return_array=True)
    mpl_fig = plt.figure()
    for i, s in enumerate(surv):
        plt.step(rsf.event_times_, s, where="post", label=str(i))
    #Receiving data from the figure

    rsf2 = plt.gcf()
    #changing the figure format
    py_fig = tls.mpl_to_plotly(rsf2, resize=True)
    #updating axis
    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )

    st.plotly_chart(py_fig)
    #creating new figure
    mpl_fig = plt.figure()

    #using the model to predict the cumulative hazzard given the values
    surv = rsf.predict_cumulative_hazard_function(train_x, return_array=True)
    
    #iterating on the value and plotting it
    for i, s in enumerate(surv):
        plt.step(rsf.event_times_, s, where="post", label=str(i))
    plt.ylabel("Cumulative hazard")
    plt.xlabel("Time in days")
    plt.legend()
    plt.grid(True)
    #Receiving data from the figure

    rsf2 = plt.gcf()
    #changing the figure format
    py_fig = tls.mpl_to_plotly(rsf2, resize=True)
    #updating axis
    py_fig.update_layout(
    yaxis_title='Cumulative hazards',
    xaxis_title='Time in days'

    )
    #plotting
    st.plotly_chart(py_fig)

    st.dataframe(train_x)

    #st.table(df)
#here we show the data used on the training and make it available to download as a csv
st.subheader("Data used to train the Survival Forest")
st.dataframe(lg_y)

#creating the download button
st.download_button(
    label="Download all the data as CSV",
    data=pd.DataFrame(lg_y).to_csv().encode('utf-8'),
    file_name='large_df.csv',
    mime='text/csv',
)

st.dataframe(lg_x)
#st.table(df)

st.download_button(
    label="Download all the data as CSV",
    data=lg_x.to_csv().encode('utf-8'),
    file_name='large_df.csv',
    mime='text/csv',
)

st.dataframe(train_x)






