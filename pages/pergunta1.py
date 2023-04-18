import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls   

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)
dic = {}
array = [(0,0)]
st.title("Survivor Analysis for lung cancer data")
st.header("Analysis of age impact in the time that a person survives")
st.sidebar.title('Navigation')
num1 = st.sidebar.number_input('Idade superior')
num2 = st.sidebar.number_input('Idade inferior')
array.append((num1, num2))
print("OI")
print(array)




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
Ta5 = {'time':[]}

Ea1 = {'status':[]}
Ea2 = {'status':[]}
Ea3 = {'status':[]}
Ea4 = {'status':[]}
Ea5 = {'status':[]}


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

    if row['age'] >= num1 and row['age'] <= num2:
        Ta1['time'].append(row['time'])
        Ea1['status'].append(row['status'])



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

ax = plt.subplot(111)
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="{num1}{num2}")
kmf.survival_function_.plot(ax = ax)
kmf2 = plt.gcf()

py_fig = tls.mpl_to_plotly(kmf2, resize=True)

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
kmf2 = plt.gcf()

py_fig = tls.mpl_to_plotly(kmf2, resize=True)

#kmf.plot_survival_function(ax = ax,at_risk_counts = True)


st.plotly_chart(py_fig)




cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula= "age + sex + ph.ecog + ph.karno")

mpl_fig = plt.figure()

cph.plot_partial_effects_on_outcome(covariates = 'age',
                                    values = [30,40,50, 60, 70, 80],
                                    cmap = 'coolwarm')
                    

cph2 = plt.gcf()

py_fig = tls.mpl_to_plotly(cph2, resize=True)

st.plotly_chart(py_fig)

