'''Estimar o tempo de sobrevivência em pacientes com cancro do pulmão com base na
sua idade, sexo, classificação ECOG e pontuação de Karnofsky'''

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter

from sksurv.linear_model import CoxPHSurvivalAnalysis


# Usar random_forest

df_na = st.session_state['dic_noNa']

cph = CoxPHFitter()
cph.fit(df_na, duration_col = 'time', event_col = 'status', formula = "age + sex + ph.ecog + ph.karno")
cph.print_summary()

plt.subplots(figsize = (10, 6))

#Exemplo para idade
    
cph.predict_survival_function(X = df_na)


st.pyplot(plt)
