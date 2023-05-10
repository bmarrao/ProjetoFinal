import csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from lifelines import CoxPHFitter ,KaplanMeierFitter
import plotly.tools as tls
import plotly.express as px
from sklearn.model_selection import train_test_split
from sksurv.ensemble import RandomSurvivalForest
import plotly.graph_objects as go
import numpy as np

#from st_pages import Page, show_pages, add_page_title,show_pages_from_config
st.set_page_config(page_title = "Lung cancer data analysis" )

st.title("Lung cancer data analysis.")

filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df['status'] = df["status"]-1
df['sex'] = df["sex"]-1
df['wt.loss'] = df['wt.loss'] * 0.45359237


df['sex'] = df['sex'].replace(0, 'Men')
df['sex'] = df['sex'].replace(1, 'Women')
df['status'] = df['status'].replace(0, 'Alive by the end of the experiment')
df['status'] = df['status'].replace(1, 'Dead by the end of the experiment')
'''
inst: código da instituição\n
time: Tempo de sobrevivˆencia em dias\n
status: status de censura 0 = censurado, 1 = morto\n
age: idade em anos\n
sex: Male=0 Female=1\n
ph.ecog: Pontuação de desempenho ECOG conforme avaliado pelo médico. 0 = assin-tomático, 1 = sintomático, mas completamente deambulat ́orio, 2 = acamado <50% do dia,3 = acamado >50% do dia, mas n ̃ao acamado, 4 = acamado\n
ph.karno: pontuaçãode desempenho de Karnofsky (mau = 0-bom = 100) avaliado pelo médico \n
pat.karno: Pontuação de desempenho de Karnofsky conforme avaliado pelo paciente\n
meal.cal: Calorias consumidas nas refeicões\n
wt.loss: Perda de peso nos  ́ultimos seis meses (kg)\n 
'''

grouped=df.groupby(df.status)
customdata = np.stack((df['age'], df['sex'],df['status'],df['wt.loss'],df['meal.cal'],df['ph.ecog'],df['ph.karno'],df['pat.karno']), axis=-1)
df_alive = grouped.get_group('Alive by the end of the experiment')
df_dead = grouped.get_group('Dead by the end of the experiment')
hovertemplate='<b>Age</b>: %{customdata[0]}<br>' + '<b>Sex</b>: %{customdata[1]}<br>' + '<b>Status</b>: %{customdata[2]}<br>' +'<b>Weight Loss</b>: %{customdata[3]}<br>'  +'<b>Calories per Meal</b>: %{customdata[4]}<br>' + '<b>ph.ecog</b>: %{customdata[5]}<br>' + '<b>ph.karno</b>: %{customdata[6]}<br>'+'<b>pat.karno</b>: %{customdata[7]}<br>' 



st.header("Tables ")

st.subheader("All the data")
st.dataframe(df)
#st.table(df)

st.download_button(
    label="Download all the data as CSV",
    data=df.to_csv().encode('utf-8'),
    file_name='large_df.csv',
    mime='text/csv',
)

st.subheader("Data from the people that died by the end of the experiment")

st.dataframe(df_dead)

st.download_button(
    label="Download all the data of people that died before the end of the experiment as CSV",
    data=df_dead.to_csv().encode('utf-8'),
    file_name='large_df.csv',
    mime='text/csv',
)
st.subheader("Data from the people that were alive by the end of the experiment")

st.dataframe(df_alive)

st.download_button(
    label="Download all the data of people that were alive at the end of the experiment as CSV",
    data=df_alive.to_csv().encode('utf-8'),
    file_name='large_df.csv',
    mime='text/csv',
)


st.header("Graphs")

st.subheader("Censored data")
fig = px.histogram(df, x="status",color="status")
st.plotly_chart(fig)

fig = go.Figure()


st.subheader("Men and women distribution in the data")
fig = go.Figure()
fig.add_trace(
    go.Histogram(x=df['sex'],
    name='All men and women')
)
fig.add_trace(go.Histogram(x=df_dead['sex'],name='Dead by the end of the experiment')
)

fig.add_trace(go.Histogram(x=df_alive['sex'],name='Alive by the end of the experiment')
            
)
st.plotly_chart(fig)


st.subheader("Age distribution across the data")


fig = go.Figure()
fig.add_trace(
    go.Histogram(x=df['age'],
    name='All men and women',customdata =customdata ,hovertemplate = hovertemplate ),
)
fig.add_trace(go.Histogram(x=df_dead['age'],name='Dead by the end of the experiment',customdata =customdata ,hovertemplate = hovertemplate )
)

fig.add_trace(go.Histogram(x=df_alive['age'],name='Alive by the end of the experiment',customdata =customdata ,hovertemplate = hovertemplate )
            
)

fig.update_layout(
    yaxis_title='Count',
    xaxis_title = 'Age',
)
st.plotly_chart(fig)

st.subheader("Medium age for men and woman across the data")


fig = go.Figure()
fig.add_trace(
    go.Box(x=df['sex'],y=df['age'],
    name='All men and women'))
                         

fig.add_trace(go.Box(x=df_dead['sex'],y=df_dead['age'],name='Dead by the end of the experiment'))
fig.add_trace(go.Box(x=df_alive['sex'],y=df_alive['age'],name='Alive by the end of the experiment'))
            
fig.update_layout(
    yaxis_title='Age',
    boxmode='group' # group together boxes of the different traces for each value of x
)


fig.update_traces(legendgroup='group')


st.plotly_chart(fig)
#Falta o comparativo dos q tavam vivo no experimento
fig = px.box(df, color = "sex" ,x="sex", y="age", points="all",hover_data=df.columns)
st.plotly_chart(fig)


st.subheader("Calories per meal across the data")
fig = px.histogram(df, x="meal.cal",hover_data=df.columns)
st.plotly_chart(fig)



st.subheader("Histogram of patients with different ecog evaluations")

fig = px.histogram(df, x="ph.ecog", marginal="rug",
                         hover_data=df.columns)
st.plotly_chart(fig)

st.subheader("Histogram of patients own evaluation of Karnofsky score")

fig = go.Figure()


fig.add_trace( go.Histogram( x=df["pat.karno"],name = 'All patients', 
                         hovertemplate = hovertemplate))


fig.add_trace( go.Histogram( x=df_dead["pat.karno"],name = 'Dead by the end of experiment', 
                         hovertemplate = hovertemplate))


fig.add_trace( go.Histogram( x=df_alive["pat.karno"],name = 'Alive by the end of experiment', 
                         hovertemplate = hovertemplate))
st.plotly_chart(fig)

st.subheader("Weight loss across the patients")

fig = px.histogram(df, x="wt.loss",hover_data=df.columns)
st.plotly_chart(fig)


st.subheader("Medium calories per meal for a ecog evaluation across the data")

fig = px.box(df, x="ph.ecog", y="meal.cal",points = "all" , hover_data=df.columns)
st.plotly_chart(fig)

fig = go.Figure()
fig.add_trace(
    go.Box(x=df['ph.ecog'],y=df['meal.cal'],
    name='All men and women'))

fig.add_trace(go.Box(x=df_dead['ph.ecog'],
                     y=df_dead['meal.cal'],
                     text = df.values,
                     name='Dead by the end of the experiment'))
fig.add_trace(go.Box(x=df_alive['ph.ecog'],y=df_alive['meal.cal'],name='Alive by the end of the experiment'))
            
fig.update_layout(
    yaxis_title='Meal.Cal',
    xaxis_title='Ph.Ecog    ',

    boxmode='group' # group together boxes of the different traces for each value of x
)
st.plotly_chart(fig)
#############################################################################################

st.header("Difference of calories consumed groupped by age")

fig = px.bar(df, x = "age",y = "meal.cal" )
st.plotly_chart(fig)

fig = px.bar(df_dead, x = "age",y = "meal.cal" )
st.plotly_chart(fig)

fig = px.bar(df_alive, x = "age",y = "meal.cal" )
st.plotly_chart(fig)

#Falta o comparativo dos q tavam vivo no experimento
st.header("Box plots of each ecog evaluation and respectives weight loss")


fig = go.Figure()

fig.add_trace( go.Box(x=df["ph.ecog"], y=df["wt.loss"], name='All patients'))


fig.add_trace( go.Box(x=df_alive["ph.ecog"], y=df_alive["wt.loss"] , name='Alive by the end of the experiment'))


fig.add_trace( go.Box(x=df_dead["ph.ecog"], y=df_dead["wt.loss"] , name='Dead by the end of the experiment'))

fig.update_layout(
    yaxis_title='wt.loss',
    xaxis_title='Ph.Ecog    ',

    boxmode='group' # group together boxes of the different traces for each value of x
)
st.plotly_chart(fig)



#Falta fazer alive e dead


###########################################################################################################


st.subheader("Influence of meal.cal on weight loss")
fig = px.bar(df, x='meal.cal', y='wt.loss', hover_data=df.columns)
fig.update_layout(
    yaxis=dict( # Here
        range=[0, 60] # Here
    )
)
st.plotly_chart(fig)

fig = px.bar(df_alive, x='meal.cal', y='wt.loss', hover_data=df_alive.columns)
fig.update_layout(
    yaxis=dict( # Here
        range=[0, 60] # Here
    )
)
st.plotly_chart(fig)

fig = px.bar(df_dead, x='meal.cal', y='wt.loss', hover_data=df_dead.columns)
fig.update_layout(
    yaxis=dict( # Here
        range=[0, 60] # Here
    )
)
st.plotly_chart(fig)

fig = go.Figure()
fig.add_trace(go.Bar(x=df['meal.cal'],y=df['wt.loss'],customdata =customdata ,hovertemplate = hovertemplate ,name='All data'))
fig.add_trace(go.Bar(x=df_dead['meal.cal'],y=df_dead['wt.loss'],customdata =customdata ,hovertemplate = hovertemplate ,name='Dead by the end of the experiment'))
fig.add_trace(go.Bar(x=df_alive['meal.cal'],y=df_alive['wt.loss'],customdata =customdata ,hovertemplate = hovertemplate ,name='Alive by the end of the experiment'))
fig.update_layout(
    yaxis_title='Weight Lost',
    xaxis_title='Calories Consumed',

    boxmode='group', # group together boxes of the different traces for each value of x
    yaxis=dict( # Here
        range=[0, 60] # Here
    )
)
st.plotly_chart(fig)

fig = px.scatter(df, x='meal.cal', y='wt.loss', hover_data=df.columns)
st.plotly_chart(fig)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_dead['meal.cal'], y=df_dead['wt.loss'],customdata =customdata ,hovertemplate = hovertemplate , mode = 'markers',name='Dead by the end of the experiment')
)

fig.add_trace(go.Scatter(x=df_alive['meal.cal'], y=df_alive['wt.loss'], customdata =customdata ,hovertemplate = hovertemplate ,mode = 'markers',name='Alive by the end of the experiment'))
st.plotly_chart(fig)

fig = px.pie(df, values='meal.cal', names='ph.karno', title='Medic Evaluation compared to calories consumed')
fig.update_layout(legend_traceorder="normal")
st.plotly_chart(fig)

fig = px.pie(df, values='meal.cal', names='pat.karno', title='Patient Evaluation compared to calories consumed')
st.plotly_chart(fig)

fig = px.box(df, x='ph.karno', y='pat.karno', points = "all", hover_data=df.columns, title='Difference from Patient to Medic')
st.plotly_chart(fig)

df['sex'] = df['sex'].replace('Men', 0)
df['sex'] = df['sex'].replace('Women',1)
df['status'] = df['status'].replace('Alive by the end of the experiment',0)
df['status'] = df['status'].replace('Dead by the end of the experiment',1)

df_dead['sex'] = df_dead['sex'].replace('Men', 0)
df_dead['sex'] = df_dead['sex'].replace('Women',1)
df_dead['status'] = df_dead['status'].replace('Alive by the end of the experiment',0)
df_dead['status'] = df_dead['status'].replace('Dead by the end of the experiment',1)

df_alive['sex'] = df_alive['sex'].replace('Men', 0)
df_alive['sex'] = df_alive['sex'].replace('Women',1)
df_alive['status'] = df_alive['status'].replace('Alive by the end of the experiment',0)
df_alive['status'] = df_alive['status'].replace('Dead by the end of the experiment',1)



st.session_state['pergunta1'] = []
st.session_state['pergunta2'] = []
st.session_state['pergunta3'] = []
st.session_state['pergunta5'] = []
st.session_state['pergunta9'] = []

st.session_state['random_forest']= []

df_na = df.copy()
df_na.dropna(inplace=True)
df_na = df_na.reset_index() 
df_na["ph.ecog"] = df_na["ph.ecog"].astype("int64")

st.session_state['dic_noNa'] = df_na
st.session_state['dic'] = df
st.title("Survivor Analysis for lung cancer data")
#st.sidebar.sucess("Select a page above")
st.subheader("Survival Forests")
lg_y = df_na[['status','time']].copy()

lg_y["status"] = lg_y["status"].astype("bool") 

lg_y = lg_y.to_records(index=False)

lg_x = df_na.drop(["status","time"],axis=1)

random_state = 20

X_train, X_test, y_train, y_test = train_test_split(
    lg_x, lg_y, test_size=0.05, random_state=random_state)

rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           n_jobs=-1,
                           random_state=random_state)
rsf.fit(X_train, y_train)
print(rsf.score(X_test, y_test))



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

