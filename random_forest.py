import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import plotly.tools as tls   

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
arr = st.session_state['random_forest']

num1 = st.sidebar.number_input('Instituição : ')
num2 = st.sidebar.number_input('Age : ')
num3 = st.sidebar.number_input('Sex(0 - homem, 1 - mulher) :')
num4 = st.sidebar.number_input('Pontuação de desempenho ECOG - Avaliado pelo médico :')
num5 = st.sidebar.number_input('Pontuacao de desempenho Karnofsky avaliado pelo médico :')
num6 = st.sidebar.number_input('Pontuacao de desempenho Karnofsky avaliado pelo paciente :')
num7 = st.sidebar.number_input('Calorias consumidas nas ultimas refeicoes : ')
num8 = st.sidebar.number_input('Perda de peso nos ultimos seis meses (em kilogramas ) : ')
'''
Deixar instituição e desempenho Karnofsky pelo paciente ?
'''


lg_y = df[['status','time']].copy()

lg_y["status"] = lg_y["status"].astype("bool") 

lg_y = lg_y.to_records(index=False)

lg_x = df.drop(["status","time"],axis=1)

random_state = 20

X_train, X_test, y_train, y_test = train_test_split(
    lg_x, lg_y, test_size=0.05, random_state=random_state)

rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           n_jobs=-1,
                           random_state=random_state)
rsf.fit(X_train, y_train)
#print(rsf.fit)
print(rsf.score(X_test, y_test))


if st.sidebar.button('Add to graph'):
    mpl_fig = plt.figure()
    array = {'age' : num2 ,'inst': num1 ,'sex': num3 ,'ph.ecog' : num4 , 'ph.karno' : num5 , 'pat.karno': num6 ,
             'meal.cal':num7,'wt.loss':num8}
    arr.append(array)
    test_1 = pd.DataFrame(arr)
    st.session_state['random_forest']= arr
    surv = rsf.predict_survival_function(test_1, return_array=True)
    for i, s in enumerate(surv):
        plt.step(rsf.event_times_, s, where="post", label=str(i))

    

surv = rsf.predict_survival_function(X_test, return_array=True)
mpl_fig = plt.figure()

for i, s in enumerate(surv):
    plt.step(rsf.event_times_, s, where="post", label=str(i))

plt.ylabel("Survival probability")
plt.xlabel("Time in days")
plt.legend()
plt.grid(True)

rsf2 = plt.gcf()

py_fig = tls.mpl_to_plotly(rsf2, resize=True)

st.plotly_chart(py_fig)

mpl_fig = plt.figure()


surv = rsf.predict_cumulative_hazard_function(X_test, return_array=True)

for i, s in enumerate(surv):
    plt.step(rsf.event_times_, s, where="post", label=str(i))
plt.ylabel("Cumulative hazard")
plt.xlabel("Time in days")
plt.legend()
plt.grid(True)

rsf2 = plt.gcf()

py_fig = tls.mpl_to_plotly(rsf2, resize=True)

st.plotly_chart(py_fig)
