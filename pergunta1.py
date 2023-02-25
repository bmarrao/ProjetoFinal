import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)


st.title("Survivor Analysis for lung cancer data")
st.header("Analysis of age impact in the time that a person survives")
'''
df = pd.read_csv(filename)
age_time = {}
age = df['age']
time = df['time']
for i in range(0,len(df)):
    if age[i] not in age_time:
        age_time[age[i]] = [time[i]]
    else:
        age_time[age[i]].append(time[i])
for i in age_time:
    x = age_time[i]
    age_time[i] = sum(x)/len(x)
graph1 = pd.DataFrame.from_dict(age_time,orient='index')

st.line_chart(graph1)
'''

df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")


#print(T)
kmf = KaplanMeierFitter()
Ta1 = {'time':[]}
Ta2 = {'time':[]}
Ta3 = {'time':[]}
Ta4 = {'time':[]}

Ea1 = {'status':[]}
Ea2 = {'status':[]}
Ea3 = {'status':[]}
Ea4 = {'status':[]}

#Ta2 = pd.DataFrame()
for index, row in df.iterrows():
    if row['age'] >= 30 and row['age'] <= 50:
        Ta1['time'].append(row['time'])
        Ea1['status'].append(row['status'])
    elif row['age'] >= 50 and row['age'] <= 60:
        Ta2['time'].append(row['time'])
        Ea2['status'].append(row['status'])
    elif row['age'] >= 60 and row['age'] <= 70:
        Ta3['time'].append(row['time'])
        Ea3['status'].append(row['status'])
    elif row['age'] >= 70 and row['age'] <= 100:
        Ta4['time'].append(row['time'])
        Ea4['status'].append(row['status'])



       #print(row['time'], row['status'])
Ta1 = pd.DataFrame(Ta1)
Ea1 = pd.DataFrame(Ea1)
Ta2 = pd.DataFrame(Ta2)
Ea2 = pd.DataFrame(Ea2)
Ta3 = pd.DataFrame(Ta3)
Ea3 = pd.DataFrame(Ea3)
Ta4 = pd.DataFrame(Ta4)
Ea4 = pd.DataFrame(Ea4)


ax = plt.subplot(111)
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="30-50")
kmf.survival_function_.plot(ax = ax)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta2, event_observed = Ea2,label="50-60")
kmf.survival_function_.plot(ax = ax)


#kmf.survival_function_plot(ax = ax)

kmf.fit(durations = Ta3, event_observed = Ea3,label="60-70")
kmf.survival_function_.plot(ax = ax)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta4, event_observed = Ea4,label="70+")
kmf.survival_function_.plot(ax = ax)

#kmf.plot_survival_function(ax = ax,at_risk_counts = True)
st.pyplot(plt)




cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula= "age + sex + ph.ecog + ph.karno")

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'age',
                                    values = [30,40,50, 60, 70, 80],
                                    cmap = 'coolwarm')
                    
st.pyplot(plt)

