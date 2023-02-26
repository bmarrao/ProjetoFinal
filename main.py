import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)



df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
df = df.reset_index() 
df['status'] = df["status"]-1
df['sex'] = df["sex"]-1





st.title("Survivor Analysis for lung cancer data")

st.subheader("1 - A idade afeta significativamente o tempo de sobrevivência em pacientes com cancro de pulmão? E após o controle de outros fatores relevantes, como sexo, pontuação dedesempenho ECOG e pontuação de desempenho de Karnofsky?")

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

st.caption("Efeito da idade sem o controle de outros dados")


cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula= "age + sex + ph.ecog + ph.karno")

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'age',
                                    values = [30,40,50, 60, 70, 80],
                                    cmap = 'coolwarm')
                    
st.pyplot(plt)

st.caption("Efeito da idade com ocontrole de outros fatores relevantes, como sexo, pontuação dedesempenho ECOG e pontuação de desempenho de Karnofsky?")

st.subheader("2 -Qual é o efeito da perda de peso nos últimos seis meses no tempo de sobrevivência em pacientes com cancro de pulmão?")


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


fig, a = plt.subplots()
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="-20")
kmf.survival_function_.plot(ax = a)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta2, event_observed = Ea2,label="(-20)-(-10)")
kmf.survival_function_.plot(ax = a)


kmf.fit(durations = Ta3, event_observed = Ea3,label="(-10)-0")
kmf.survival_function_.plot(ax = a)

#kmf.survival_function_plot(ax = ax)

kmf.fit(durations = Ta3, event_observed = Ea3,label="(-10)-0")
kmf.survival_function_.plot(ax = a)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta4, event_observed = Ea4,label="0-10")
kmf.survival_function_.plot(ax = a)

kmf.fit(durations = Ta5, event_observed = Ea5,label="10-20")
kmf.survival_function_.plot(ax = a)


kmf.fit(durations = Ta6, event_observed = Ea6,label="20-30")
kmf.survival_function_.plot(ax = a)


kmf.fit(durations = Ta7, event_observed = Ea7,label="30+")
kmf.survival_function_.plot(ax = a)

#kmf.plot_survival_function(ax = ax,at_risk_counts = True)

st.pyplot(fig)



st.subheader("3 -A pontuação de desempenho de Karnofsky, avaliada pelo médico, prediz o tempo desobrevivência em pacientes com cancro do pulmão?")

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula= "ph.karno")

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'ph.karno',
                                    values = [0,10,20,30,40,50,60,70,80,90,100],
                                    cmap = 'coolwarm')
st.pyplot(plt)

st.subheader("4 -Existe uma diferença significativa no tempo de sobrevivência entre homens e mulheres com cancro do pulmão? E após o controle de outras covariáveis, como idade, classificação ECOG ou pontuação de Karnofsky")

cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status')

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'sex',
                                    values = [1,2],
                                    cmap = 'coolwarm')
st.pyplot(plt)

fig, a = plt.subplots()


Ta1 = {'time':[]}
Ta2 = {'time':[]}
Ea1 = {'status':[]}
Ea2 = {'status':[]}
for index, row in df.iterrows():
    if row['sex'] == 1 :
        Ta1['time'].append(row['time'])
        Ea1['status'].append(row['status'])
    elif row['sex'] == 2:
        Ta2['time'].append(row['time'])
        Ea2['status'].append(row['status'])
Ta1 = pd.DataFrame(Ta1)
Ea1 = pd.DataFrame(Ea1)
Ta2 = pd.DataFrame(Ta2)
Ea2 = pd.DataFrame(Ea2)
ax = plt.subplot(111)
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="Homem ou mulher")
kmf.survival_function_.plot(ax = a)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta2, event_observed = Ea2,label="Homem ou mulher")
kmf.survival_function_.plot(ax = a)

st.pyplot(fig)
st.subheader("5 -O consumo de calorias nas refeições afeta o tempo de sobrevivência em pacientes com cancro de pulmão?")
cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula = "meal.cal")

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'meal.cal',
                                    values = [0,200,500,1000,1500,2000,2500],
                                    cmap = 'coolwarm')
st.pyplot(plt)


st.subheader("7- Existe diferença significativa no tempo de sobrevivência entre pacientes com diferentes classificações de desempenho do ECOG")
cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula = "ph.ecog")

#plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'ph.ecog',
                                    values = [0,1,2,3,4],
                                    cmap = 'coolwarm')
st.pyplot(plt)

st.subheader("8- Comparar a pontuação de desempenho de Karnofsky, avaliada pelo paciente, com a classificação do médico")

dic = {'Paciente' : df["ph.karno"],'Medico': df["pat.karno"]}
data = pd.DataFrame(data = dic)

st.line_chart(data)

st.subheader("10 -Existe uma diferença significativa no tempo de sobrevivência entre homens e mulheres com cancro do pulmão? E após o controle de outras covariáveis, como idade, classificação ECOG ou pontuação de Karnofsky")


x = df['meal.cal']
y = df['ph.karno']

plt.scatter(x, y)

st.pyplot(plt)