'''Estimar o tempo de sobrevivência em pacientes com cancro do pulmão com base na
sua idade, sexo, classificação ECOG e pontuação de Karnofsky'''

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter

from sksurv.linear_model import CoxPHSurvivalAnalysis

df_na = st.session_state['dic_noNa']

num1 = st.sidebar.number_input("Idade")
num2 = st.sidebar.number_input("Sexo")
num3 = st.sidebar.number_input("Pontuação de Karnofsky")
num4 = st.sidebar.number_input("Classificação ECOG")

if st.sidebar.button('Add to graph'):
    array = {'age' : num1  ,'sex': num2 ,'ph.ecog' : num4 , 'ph.karno' : num3}

    train_x = pd.DataFrame.from_dict(array)

    st.dataframe(train_x)

    estimator = CoxPHSurvivalAnalysis().fit(train_x, df_na['status'])

    surv_funcs = estimator.predict_survival_function(df_na['time'].iloc[:10])

    for fn in surv_funcs:
        plt.step(fn.x, fn(fn.x), where="post")

    plt.ylim(0, 1)
    st.pyplot(plt)