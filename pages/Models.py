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


st.header("Modelos usados na criação dos graficos , suas explicações e suas formulas")

st.subheader("Estimador de Kaplan-Meier")

st.text("É um modelo também conhecido como o estimador de limite de produto , usamos este modelo pois ele é capaz de calcular a probabilidade de sobrevivência para conjuntos de dados com falhas e suspensôes INFORMAÇÂO OBTIDA EM : https://support.minitab.com/pt-br/minitab/20/help-and-how-to/statistical-modeling/reliability/how-to/distribution-overview-plot-right-censoring/methods-and-formulas/nonparametric-methods-and-formulas/kaplan-meier-estimation/")
