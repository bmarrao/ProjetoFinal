import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
from lifelines.statistics import proportional_hazard_test
import plotly.tools as tls
import plotly.express as px
from sklearn.model_selection import train_test_split
from sksurv.ensemble import RandomSurvivalForest

st.header("Models used on the creation of the graphs, their explanations and their formulas")

df_na = st.session_state['dic_noNa']
cph = CoxPHFitter()
cph.fit(df_na, duration_col = 'time', event_col = 'status')

st.subheader("Kaplan-Meier Model")
'''
The Kaplan-Meier approach, also called the product-limit approach,\n was used because it is capable of calculation the probability of survival for sets with\n missing information.
'''
st.subheader("Cox Proportional Hazard Model")
'''
The Cox Proportional Hazard Model includes covariates to calculate\n the log-hazard linear function and ,without using covariates, a population-level \nbaseline hazard
It also assumes that the probability of survival is independent\n between each patient, the hazard and predictors are multiplicative\n and that the hazard ratio is constant.
'''
st.subheader("Interpretation of Cox Model results")
'''
For example Wt.loss has a coefficent of -0.01.\n That means 1 unit of weigth loss will increase the baseline hazard by a \nfactor of exp(-0.01) which equals to 0.99 or in other terms a 1 percent decrease

We can also plot the inffluence of each variable in term of the log(HR)\n to see what are the most damaging to the patient.
'''

mpl_fig = plt.figure()
cph.plot()
st.pyplot(mpl_fig)  
'''
There is a function to see all the coefficients of each variable to get more\n in depth analysis of them.
'''

#results = proportional_hazard_test(cph,df_na,time_transform='rank')
#x = results.prisummary(decimals=3)
#st.dataframe(x)
st.subheader("Random Survival Forests")
'''
A random durvival forest is an estimator that fits a number of survival trees using samples of the dataset \n and uses averaging to predict more accurately and to prevent over-fitting
In each survival tree, the quality of a split is measured by the log-rank splitting rule that compares differents results of an event in various groups.
'''