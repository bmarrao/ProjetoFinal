import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls
import plotly.express as px
from sklearn.model_selection import train_test_split
from sksurv.ensemble import RandomSurvivalForest

st.header("Models used on the creation of the graphs, their explanations and their formulas")


st.subheader("Kaplan-Meier Model")

st.text("The Kaplan-Meier approach, also called the product-limit approach,the model was used because it is capable of calculation the probability of survival for sets with missing information")

st.subheader("Cox Proportional Hazard Model")

st.text("The Cox Proportional Hazard Model includes covariates to calculate the log-hazard linear function and ,without using covariates, a population-level baseline hazard")
st.text("it also assumes that the probability of survival is independent between each patient, the hazard and predictors are multiplicative and that the hazard ratio is constant")

st.subheader("Interpretation of Cox Model results")

st.text("For example Wt.loss has a coefficent of -0.01. That means 1 unit of weigth loss will increase the baseline hazard by a factor of exp(-0.01) which equals to 0.99 or in other terms a 1 percent decrease")

st.text("We can also plot the inffluence of each variable in term of the log(HR) to see what are the most damaging to the patient")

st.text("There is a function to see all the coefficients of each variable to get more in depth analysis of them.")