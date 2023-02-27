import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls
import plotly.express as px

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


for index, row in df.iterrows():
    print(row['wt.loss'])
st.title("Survivor Analysis for lung cancer data")

##########################################################################################################################################

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

st.caption("Efeito da idade com ocontrole de outros fatores relevantes, como sexo, pontuação dedesempenho ECOG e pontuação de desempenho de Karnofsky?")

##########################################################################################################################################

st.subheader("2 -Qual é o efeito da perda de peso nos últimos seis meses no tempo de sobrevivência em pacientes com cancro de pulmão?")


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
    if row['wt.loss'] <= -10 :
        Ta1['time'].append(row['time'])
        Ea1['status'].append(row['status'])
    elif row['wt.loss'] >= -10 and row['wt.loss'] <= 0:
        Ta2['time'].append(row['time'])
        Ea2['status'].append(row['status'])
    elif row['wt.loss'] >= 0 and row['wt.loss'] <= 10:
        Ta3['time'].append(row['time'])
        Ea3['status'].append(row['status'])
    elif row['wt.loss'] >= 10 and row['wt.loss'] <= 20:
        Ta4['time'].append(row['time'])
        Ea4['status'].append(row['status'])
    elif row['wt.loss'] >= 20 :
        Ta5['time'].append(row['time'])
        Ea5['status'].append(row['status'])   



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


fig, a = plt.subplots()
kmf = KaplanMeierFitter()
kmf.fit(durations = Ta1, event_observed = Ea1,label="-10")
kmf.survival_function_.plot(ax = a)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta2, event_observed = Ea2,label="-10-0")
kmf.survival_function_.plot(ax = a)


kmf.fit(durations = Ta3, event_observed = Ea3,label="0-10")
kmf.survival_function_.plot(ax = a)

#kmf.survival_function_plot(ax = ax)

kmf.fit(durations = Ta3, event_observed = Ea3,label="(-10)-0")
kmf.survival_function_.plot(ax = a)

#kmf.plot_survival_function(ax = ax)

kmf.fit(durations = Ta4, event_observed = Ea4,label="10-0")
kmf.survival_function_.plot(ax = a)

kmf.fit(durations = Ta5, event_observed = Ea5,label="20+")
kmf.survival_function_.plot(ax = a)


kmf2 = plt.gcf()

py_fig = tls.mpl_to_plotly(kmf2, resize=True)

#kmf.plot_survival_function(ax = ax,at_risk_counts = True)

st.plotly_chart(py_fig)

##########################################################################################################################################

st.subheader("3 -A pontuação de desempenho de Karnofsky, avaliada pelo médico, prediz o tempo desobrevivência em pacientes com cancro do pulmão?")

df = df.reset_index() 
dic_died = {'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []}
dic_alive =  {'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []}
dic =  {'0-10' : [], '10-20': [], '20-30' : [] , '30-40' : [] , '40-50' : [] , '50-60' : [], '60-70' : [] , '70-80' : [] , '80-90' : [] , '90-100' : []}

for index, row in df.iterrows():
    if row['ph.karno'] >= 0 and row['ph.karno'] < 10 :
        if row['status'] == 0 :
            dic_died ['0-10'].append(row['time'])
        else :
            dic_alive['0-10'].append(row['time'])
        dic['0-10'].append(row['time'])
    elif row['ph.karno'] >= 10 and row['ph.karno'] < 20:
        if row['status'] == 0 :
            dic_died ['10-20'].append(row['time'])
        else :
            dic_alive['10-20'].append(row['time'])
        dic['10-20'].append(row['time'])
    elif row['ph.karno'] >= 20 and row['ph.karno'] <30:
        if row['status'] == 0 :
            dic_died ['20-30'].append(row['time'])
        else :
            dic_alive['20-30'].append(row['time'])
        dic['20-30'].append(row['time'])
    elif row['ph.karno'] >= 30 and row['ph.karno'] < 40:
        if row['status'] == 0 :
            dic_died ['30-40'].append(row['time'])
        else :
            dic_alive['30-40'].append(row['time'])
        dic['30-40'].append(row['time'])

    elif row['ph.karno'] >= 40 and row['ph.karno'] < 50:
        if row['status'] == 0 :
            dic_died ['40-50'].append(row['time'])
        else :
            dic_alive['40-50'].append(row['time']) 
        dic['40-50'].append(row['time'])
    elif row['ph.karno'] >= 50 and row['ph.karno'] < 60:
        if row['status'] == 0 :
            dic_died ['50-60'].append(row['time'])
        else :
            dic_alive['50-60'].append(row['time'])  
        dic['50-60'].append(row['time'])
    elif row['ph.karno'] >= 60 and row['ph.karno'] <70:
        if row['status'] == 0 :
            dic_died ['60-70'].append(row['time'])
        else :
            dic_alive['60-70'].append(row['time'])
        dic['60-70'].append(row['time'])
    elif row['ph.karno'] >= 70 and row['ph.karno'] < 80:
        if row['status'] == 0 :
            dic_died ['70-80'].append(row['time'])
        else :
            dic_alive['70-80'].append(row['time']) 
        dic['70-80'].append(row['time'])
    elif row['ph.karno'] >= 80 and row['ph.karno'] <= 90:
        if row['status'] == 0 :
            dic_died ['80-90'].append(row['time'])
        else :
            dic_alive['80-90'].append(row['time']) 
        dic['80-90'].append(row['time'])
    else:
        if row['status'] == 0 :
            dic_died ['90-100'].append(row['time'])
        else :
            dic_alive['90-100'].append(row['time'])  
        dic['90-100'].append(row['time'])

remove = []
remove2 = []
for i in dic :
    if dic[i]:
        dic[i] = (len(dic_died[i])  /  len(dic[i]) ) * 100
    else :
        remove2.append(i)

for i in dic_died:
    if dic_died[i] :
        dic_died[i] = sum(dic_died[i])/len(dic_died[i]) 
    else :
        remove.append(i)
for i in dic_alive:
    if dic_alive[i] :
        dic_alive[i] =  len(dic_alive[i])
    else :
        dic_alive[i] = 0
    
for i in remove:
    dic_died.pop(i)
for i in remove2:
    dic.pop(i)

graph1 = pd.DataFrame.from_dict(dic,orient='index')
graph2 = pd.DataFrame.from_dict(dic_died,orient='index')
graph3 = pd.DataFrame.from_dict(dic_alive,orient='index')

print(dic_died)
print(dic_alive)
print(dic)

st.bar_chart(graph1)
st.bar_chart(graph2)
st.bar_chart(graph3)



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



##########################################################################################################################################

st.subheader("5 -O consumo de calorias nas refeições afeta o tempo de sobrevivência em pacientes com cancro de pulmão?")
cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula = "meal.cal")

mpl_fig = plt.figure()

plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'meal.cal',
                                    values = [0,200,500,1000,1500,2000,2500],
                                    cmap = 'coolwarm')

cph2 = plt.gcf()

py_fig = tls.mpl_to_plotly(cph2, resize=True)

st.plotly_chart(py_fig)

##########################################################################################################################################

st.subheader("7- Existe diferença significativa no tempo de sobrevivência entre pacientes com diferentes classificações de desempenho do ECOG")
cph = CoxPHFitter()
cph.fit(df, duration_col = 'time', event_col = 'status',formula = "ph.ecog")

#plt.subplots(figsize = (10, 6))

cph.plot_partial_effects_on_outcome(covariates = 'ph.ecog',
                                    values = [0,1,2,3,4],
                                    cmap = 'coolwarm')
st.pyplot(plt)

##########################################################################################################################################

st.subheader("8- Comparar a pontuação de desempenho de Karnofsky, avaliada pelo paciente, com a classificação do médico")

dic = {'Paciente' : df["ph.karno"],'Medico': df["pat.karno"]}
data = pd.DataFrame(data = dic)

st.line_chart(data)

##########################################################################################################################################

st.subheader("10 -Existe uma diferença significativa no tempo de sobrevivência entre homens e mulheres com cancro do pulmão? E após o controle de outras covariáveis, como idade, classificação ECOG ou pontuação de Karnofsky")


x = df['meal.cal']
y = df['ph.karno']

z = px.scatter(x = x, y =y,opacity = .2)
st.plotly_chart(z)

##########################################################################################################################################

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
