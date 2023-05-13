import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import plotly.tools as tls   

from sklearn.model_selection import train_test_split
from sksurv.ensemble import RandomSurvivalForest


df_na = st.session_state['dic_noNa']


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


st.subheader("Survival Forests")

lg_y = df_na[['status','time']].copy()

lg_y["status"] = lg_y["status"].astype("bool") 

lg_y = lg_y.to_records(index=False)

lg_x = df_na.drop(["status","time"],axis=1)


random_state = 20

st.text("Data used to train the Survival Forest")
st.dataframe(lg_y)
#st.table(df)

st.download_button(
    label="Download all the data as CSV",
    data=pd.DataFrame(lg_y).to_csv().encode('utf-8'),
    file_name='large_df.csv',
    mime='text/csv',
)

st.dataframe(lg_x)
#st.table(df)

st.download_button(
    label="Download all the data as CSV",
    data=lg_x.to_csv().encode('utf-8'),
    file_name='large_df.csv',
    mime='text/csv',
)
rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           n_jobs=-1,
                           random_state=random_state)
rsf.fit(lg_x, lg_y)



if st.sidebar.button('Add to graph'):
    mpl_fig = plt.figure()
    array = {'age' : num2 ,'inst': num1 ,'sex': num3 ,'ph.ecog' : num4 , 'ph.karno' : num5 , 'pat.karno': num6 ,
             'meal.cal':num7,'wt.loss':num8}
    arr.append(array)
    Train = pd.DataFrame.from_dict(arr)

    train_y = Train[['status','time']].copy()
    train_y["status"] = train_y["status"].astype("bool") 

    train_y = train_y.to_records(index=False)

    train_x = Train.drop(["status","time"],axis=1)

