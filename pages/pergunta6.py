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

    cph = CoxPHFitter()
    cph.fit(array, duration_col = 'time', event_col = 'status')
    cph.print_summary()

    plt.subplots(figsize = (10, 6))
    
    cph.predict_survival_function(X = array)

    st.pyplot(plt)