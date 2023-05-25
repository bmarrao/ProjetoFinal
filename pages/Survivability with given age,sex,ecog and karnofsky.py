import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter
import plotly.tools as tls 


from sksurv.ensemble import RandomSurvivalForest

df_na = st.session_state['dic_noNa']

arr = st.session_state['random_forest']

lg_y = df_na[['status','time']].copy()

lg_y["status"] = lg_y["status"].astype("bool") 

lg_y = lg_y.to_records(index=False)

lg_x = df_na.drop(["status","time","meal.cal","pat.karno","wt.loss"],axis=1)

random_state = 20

rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           n_jobs=-1,
                           random_state=random_state)
rsf.fit(lg_x, lg_y)
train_x = pd.DataFrame.from_dict(arr)

num1 = st.sidebar.number_input("Idade")
num2 = st.sidebar.number_input("Sexo")
num3 = st.sidebar.number_input("Pontuação de Karnofsky")
num4 = st.sidebar.number_input("Classificação ECOG")

if st.sidebar.button('Add to graph'):
    array = {'age' : num1  ,'sex': num2 ,'ph.ecog' : num4 , 'ph.karno' : num3}

    arr.append(array)
    train_x = pd.DataFrame.from_dict(arr)

    surv = rsf.predict_survival_function(train_x, return_array=True)
    mpl_fig = plt.figure()
    for i, s in enumerate(surv):
        plt.step(rsf.event_times_, s, where="post", label=str(i))

    rsf2 = plt.gcf()

    py_fig = tls.mpl_to_plotly(rsf2, resize=True)

    py_fig.update_layout(
    yaxis_title='Survival Probabily',
    xaxis_title='Time in days'

    )

    st.plotly_chart(py_fig)
    st.dataframe(train_x)