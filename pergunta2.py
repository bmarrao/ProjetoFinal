import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from lifelines import CoxPHFitter, KaplanMeierFitter

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)


#print(df)

#print(df.isnull().sum())

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
df = df.reset_index() 
df['status'] = df["status"]-1


#print(T)
kmf = KaplanMeierFitter()
Ta1 = {'time':[]}
Ta2 = {'time':[]}
Ta3 = {'time':[]}
Ta4 = {'time':[]}
Ta5 = {'time':[]}
Ta6 = {'time':[]}
Ta7 = {'time':[]}

Ea1 = {'status':[]}
Ea2 = {'status':[]}
Ea3 = {'status':[]}
Ea4 = {'status':[]}
Ea5 = {'status':[]}
Ea6 = {'status':[]}
Ea7 = {'status':[]}

#Ta2 = pd.DataFrame()
for index, row in df.iterrows():
    if row['wt.loss'] <= -20 :
        Ta1['time'].append(row['time'])
        Ea1['status'].append(row['status'])
    elif row['wt.loss'] >= -20 and row['wt.loss'] <= -10:
        Ta2['time'].append(row['time'])
        Ea2['status'].append(row['status'])
    elif row['wt.loss'] >= -10 and row['wt.loss'] <= 0:
        Ta3['time'].append(row['time'])
        Ea3['status'].append(row['status'])
    elif row['wt.loss'] >= 0 and row['wt.loss'] <= 10:
        Ta4['time'].append(row['time'])
        Ea4['status'].append(row['status'])
    elif row['wt.loss'] >= 10 and row['wt.loss'] <= 20:
        Ta5['time'].append(row['time'])
        Ea5['status'].append(row['status'])
    elif row['wt.loss'] >= 20 and row['wt.loss'] <= 30:
        Ta6['time'].append(row['time'])
        Ea6['status'].append(row['status'])
    elif row['wt.loss'] >= 30 :
        Ta7['time'].append(row['time'])
        Ea7['status'].append(row['status'])   



       #print(row['time'], row['status'])
Ta1 = pd.DataFrame(Ta1)
Ea1 = pd.DataFrame(Ea1)
Ta2 = pd.DataFrame(Ta2)
Ea2 = pd.DataFrame(Ea2)
Ta3 = pd.DataFrame(Ta3)
Ea3 = pd.DataFrame(Ea3)
Ta4 = pd.DataFrame(Ta4)
Ea4 = pd.DataFrame(Ea4)
Ta5 = pd.DataFrame(Ta5)
Ea5 = pd.DataFrame(Ea5)
Ta6 = pd.DataFrame(Ta6)
Ea6 = pd.DataFrame(Ea6)
Ta7 = pd.DataFrame(Ta7)
Ea7 = pd.DataFrame(Ea7)


ax = plt.subplot(111)
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="-20")
kmf.survival_function_.plot(ax = ax)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta2, event_observed = Ea2,label="(-20)-(-10)")
kmf.survival_function_.plot(ax = ax)


kmf.fit(durations = Ta3, event_observed = Ea3,label="(-10)-0")
kmf.survival_function_.plot(ax = ax)

#kmf.survival_function_plot(ax = ax)

kmf.fit(durations = Ta3, event_observed = Ea3,label="(-10)-0")
kmf.survival_function_.plot(ax = ax)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta4, event_observed = Ea4,label="0-10")
kmf.survival_function_.plot(ax = ax)

kmf.fit(durations = Ta5, event_observed = Ea5,label="10-20")
kmf.survival_function_.plot(ax = ax)


kmf.fit(durations = Ta6, event_observed = Ea6,label="20-30")
kmf.survival_function_.plot(ax = ax)


kmf.fit(durations = Ta7, event_observed = Ea7,label="30+")
kmf.survival_function_.plot(ax = ax)

#kmf.plot_survival_function(ax = ax,at_risk_counts = True)

st.pyplot(plt)


'''
cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula= "age + sex + ph.ecog + ph.karno - wt.loss")

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'wt.loss',
                                    values = [-40,-30,-20,-10,0,10,20,30,40,50,60,70],
                                    cmap = 'coolwarm')
st.pyplot(plt)
'''