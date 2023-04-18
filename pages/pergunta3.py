import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter
import plotly.tools as tls   


filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)
#print(df)

#print(df.isnull().sum())
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
dic =  {'died': {'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []},'alive':{'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []}}

for index, row in df.iterrows():
    if row['ph.karno'] >= 0 and row['ph.karno'] < 10 :
        if row['status'] == 1 :
            dic['died']['0-10'].append(row['time'])
        else :
            dic['alive']['0-10'].append(row['time'])
    elif row['ph.karno'] >= 10 and row['ph.karno'] < 20:
        if row['status'] == 1 :
            dic['died']['10-20'].append(row['time'])
        else :
            dic['alive']['10-20'].append(row['time'])
    elif row['ph.karno'] >= 20 and row['ph.karno'] <30:
        if row['status'] == 1 :
            dic['died']['20-30'].append(row['time'])
        else :
            dic['alive']['20-30'].append(row['time'])
    elif row['ph.karno'] >= 30 and row['ph.karno'] < 40:
        if row['status'] == 1 :
            dic['died'] ['30-40'].append(row['time'])
        else :
            dic['alive']['30-40'].append(row['time'])
    elif row['ph.karno'] >= 40 and row['ph.karno'] < 50:
        if row['status'] == 1 :
            dic['died'] ['40-50'].append(row['time'])
        else :
            dic['alive']['40-50'].append(row['time']) 
    elif row['ph.karno'] >= 50 and row['ph.karno'] < 60:
        if row['status'] == 1 :
            dic['died'] ['50-60'].append(row['time'])
        else :
            dic['alive']['50-60'].append(row['time'])  
    elif row['ph.karno'] >= 60 and row['ph.karno'] <70:
        if row['status'] == 1 :
            dic['died'] ['60-70'].append(row['time'])
        else :
            dic['alive']['60-70'].append(row['time'])
    elif row['ph.karno'] >= 70 and row['ph.karno'] < 80:
        if row['status'] == 1 :
            dic['died'] ['70-80'].append(row['time'])
        else :
            dic['alive']['70-80'].append(row['time']) 
    elif row['ph.karno'] >= 80 and row['ph.karno'] <= 90:
        if row['status'] == 1 :
            dic['died']['80-90'].append(row['time'])
        else :
            dic['alive']['80-90'].append(row['time']) 
    else:
        if row['status'] == 1 :
            dic['died'] ['90-100'].append(row['time'])
        else :
            dic['alive']['90-100'].append(row['time'])  

remove = []
porcentagem ={'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []}
for i in ['0-10' , '10-20', '20-30' , '30-40' , '40-50' , '50-60' , '60-70' , '70-80' , '80-90' , '90-100'] :
    x = len(dic['alive'][i]) + len(dic['died'][i])
    if x:
        porcentagem[i] = (len(dic['alive'][i])  / x) * 100
        dic['died'][i] = (sum(dic['died'][i])  / len(dic['died'][i]))
        dic['alive'][i] = (sum(dic['alive'][i])  / len(dic['alive'][i]))


    else :
        remove.append(i)

for i in remove :
     dic['died'].pop(i)
     dic['alive'].pop(i)
     porcentagem.pop(i)

graph1 = pd.DataFrame.from_dict(dic,orient='index').transpose()
graph2 = pd.DataFrame.from_dict(porcentagem,orient='index')

st.bar_chart(graph1)

st.bar_chart(graph2)




#FAZER MAIS GRÁFICOS

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula= "age + sex + ph.ecog + ph.karno")

mpl_fig = plt.figure()

cph.plot_partial_effects_on_outcome(covariates = 'ph.karno',
                                    values = [0,10,20,30,40,50,60,70,80,90,100],
                                    cmap = 'coolwarm')



cph2 = plt.gcf()

py_fig = tls.mpl_to_plotly(cph2, resize=True)

st.plotly_chart(py_fig)
