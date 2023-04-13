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

df['status'] = df["status"]-1
df['sex'] = df["sex"]-1
df['wt.loss'] = df['wt.loss'] * 0.45359237

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
df = df.reset_index() 

st.title("Survivor Analysis for lung cancer data")

st.subheader("Survival Forests")

lg_y = df[['status','time']].copy()

lg_y["status"] = lg_y["status"].astype("bool") 

lg_y = lg_y.to_records(index=False)

lg_x = df.drop(["status","time"],axis=1)

st.header("Modelos usados na criação dos graficos , suas explicações e suas formulas")

st.subheader("Estimador de Kaplan-Meier")

st.text("É um modelo também conhecido como o estimador de limite de produto , usamos este modelo pois ele é capaz de calcular a probabilidade de sobrevivência para conjuntos de dados com falhas e suspensôes INFORMAÇÂO OBTIDA EM : https://support.minitab.com/pt-br/minitab/20/help-and-how-to/statistical-modeling/reliability/how-to/distribution-overview-plot-right-censoring/methods-and-formulas/nonparametric-methods-and-formulas/kaplan-meier-estimation/")
st.la