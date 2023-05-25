import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls
import plotly.express as px
from sklearn.model_selection import train_test_split
from sksurv.ensemble import RandomSurvivalForest

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

st.header("Models used on the creation of the graphs, their explanations and their formulas")


st.subheader("Kaplan-Meier Model")

st.text("The Kaplan-Meier approach, also called the product-limit approach,the model was used because it is capable of calculation the probability of survival for sets with missing information")

st.subheader("Cox Proportional Hazard Model")

st.text("The Cox Proportional Hazard Model includes covariates to calculate the log-hazard linear function and ,without using covariates, a population-level baseline hazard")
st.text("it also assumes that the probability of survival is independent between each patient, the hazard and predictors are multiplicative and that the hazard ratio is constant")

st.subheader("Interpretation of Cox Model results")

