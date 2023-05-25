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
import plotly.figure_factory as ff

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

df_na = df.copy()
df_na.dropna(inplace=True)
df_na = df_na.reset_index() 
df_na["ph.ecog"] = df_na["ph.ecog"].astype("int64")
df_na.pop("index")
grouped_na=df_na.groupby(df_na.status)
dfna_alive = grouped_na.get_group('Alive by the end of the experiment')
dfna_dead = grouped_na.get_group('Dead by the end of the experiment')


'''
In this project we will be analyzing data from a study of patients with advanced lung cancer in a clinical trial of a new treatment , the Data has the following atributtes
inst: code of the instituion\n  Time: time of survival in day \nstatus: censured = 0 and  dead = 1\n Age : In years \n sex : Male = 0, Female = 1\n
ph.ecog: ECOG performance score as assessed by physician. 0 = asymptomatic, 1 = symptomatic but fully ambulatory, 2 = bedridden <50% of the day, 3 = bedridden >50% of the day but not bedridden, 4 = bedridden\n
ph.karno: Karnofsky performance score (poor = 0-good = 100) as assessed by physician\n
pat.karno:Karnofsky Performance Score as rated by the patient\n
meal.cal: Calories per meal\n
wt.loss: Weight loss in  (kg)
'''

grouped=df.groupby(df.status)
customdata = np.stack((df['age'], df['sex'],df['status'],df['wt.loss'],df['meal.cal'],df['ph.ecog'],df['ph.karno'],df['pat.karno']), axis=-1)
df_alive = grouped.get_group('Alive by the end of the experiment')
df_dead = grouped.get_group('Dead by the end of the experiment')
hovertemplate='<b>Age</b>: %{customdata[0]}<br>' + '<b>Sex</b>: %{customdata[1]}<br>' + '<b>Status</b>: %{customdata[2]}<br>' +'<b>Weight Loss</b>: %{customdata[3]}<br>'  +'<b>Calories per Meal</b>: %{customdata[4]}<br>' + '<b>ph.ecog</b>: %{customdata[5]}<br>' + '<b>ph.karno</b>: %{customdata[6]}<br>'+'<b>pat.karno</b>: %{customdata[7]}<br>' 
st.session_state['dic1'] = df 
st.session_state['dicalive'] = df_alive
st.session_state['dicdead'] = df_dead
st.session_state['customdata'] = customdata 
st.session_state['hovertemplate'] = hovertemplate






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

hovertemplate='<b>Age</b>: %{customdata[0]}<br>' + '<b>Sex</b>: %{customdata[1]}<br>' + '<b>Status</b>: %{customdata[2]}<br>' +'<b>Weight Loss</b>: %{customdata[3]}<br>'  +'<b>Calories per Meal</b>: %{customdata[4]}<br>' + '<b>ph.ecog</b>: %{customdata[5]}<br>' + '<b>ph.karno</b>: %{customdata[6]}<br>'+'<b>pat.karno</b>: %{customdata[7]}<br>' 

st.subheader("Men and women distribution in the data")
fig = go.Figure()
fig.add_trace(
    go.Histogram(x=df['sex'],
    name='All data'),
)
fig.add_trace(go.Histogram(x=df_dead['sex'],name='Dead by the end of the experiment')
)

fig.add_trace(go.Histogram(x=df_alive['sex'],name='Alive by the end of the experiment')
            
)
fig.update_layout(barmode='overlay')

fig.update_traces(opacity=0.75)

st.plotly_chart(fig)    


st.subheader("Age distribution across the data")

hist_data = [df['age'].to_numpy(), df_dead['age'].to_numpy(), df_alive['age'].to_numpy()]

group_labels = ['All data', 'Dead by the end of the experiment', 'Alive by the end of the experiment']
colors = ['#393E46', '#2BCDC1', '#F66095']

fig = ff.create_distplot(hist_data, group_labels,colors=colors,bin_size=5,show_rug = False)
fig.update_layout(
    yaxis_title='Density',
    xaxis_title = 'Age',
)
fig.update_traces(hovertemplate =hovertemplate, customdata= customdata,
                  selector=dict(type="histogram"))
st.plotly_chart(fig)


fig = go.Figure()
fig.add_trace(
    go.Histogram(x=df['age'],
    name='All data',customdata =customdata ,hovertemplate = hovertemplate),
)
fig.add_trace(go.Histogram(x=df_dead['age'],name='Dead by the end of the experiment',customdata =customdata ,hovertemplate = hovertemplate )
)

fig.add_trace(go.Histogram(x=df_alive['age'],name='Alive by the end of the experiment',customdata =customdata ,hovertemplate = hovertemplate )
            
)

fig.update_layout(
    yaxis_title='Count',
    xaxis_title = 'Age',
    barmode='overlay'
)
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
st.plotly_chart(fig)




st.subheader("Calories per meal across the data")


hist_data = [df_na['meal.cal'].to_numpy(), dfna_dead['meal.cal'].to_numpy(), dfna_alive['meal.cal'].to_numpy()]

group_labels = ['All data', 'Dead by the end of the experiment', 'Alive by the end of the experiment']
colors = ['#393E46', '#2BCDC1', '#F66095']

fig = ff.create_distplot(hist_data, group_labels,colors=colors,bin_size=150, show_rug=False)
fig.update_layout(
    yaxis_title='Density',
    xaxis_title = 'Calories',
)
st.plotly_chart(fig)



st.subheader("Histogram of patients with different ecog evaluations")

fig = go.Figure()

fig.add_trace( go.Histogram( x=df["ph.ecog"],name = 'All patients',  customdata =customdata,
                         hovertemplate = hovertemplate))

fig.add_trace( go.Histogram( x=df_dead["ph.ecog"],name = 'Dead by the end of experiment',  customdata =customdata,
                         hovertemplate = hovertemplate))

fig.add_trace( go.Histogram( x=df_alive["ph.ecog"],name = 'Alive by the end of experiment',  customdata =customdata,
                         hovertemplate = hovertemplate))

fig.update_layout(
    yaxis_title='count',
    xaxis_title='Patient ecog level',
    boxmode='group')

st.plotly_chart(fig)

st.subheader("Histogram of patients own evaluation of Karnofsky score")

fig = go.Figure()


fig.add_trace( go.Histogram( x=df["pat.karno"],name = 'All patients', customdata =customdata,
                         hovertemplate = hovertemplate))


fig.add_trace( go.Histogram( x=df_dead["pat.karno"],name = 'Dead by the end of experiment', customdata =customdata,
                         hovertemplate = hovertemplate))


fig.add_trace( go.Histogram( x=df_alive["pat.karno"],name = 'Alive by the end of experiment', customdata =customdata, 
                         hovertemplate = hovertemplate))
fig.update_layout(
    yaxis_title='count',
    xaxis_title='Patient karno score',
    barmode='overlay')

fig.update_traces(opacity=0.75)


st.plotly_chart(fig)

st.subheader("Weight loss across the patients")

fig = go.Figure()
fig.add_trace(
    go.Histogram(x=df['meal.cal'],
    name='All data',customdata =customdata ,hovertemplate = hovertemplate),
)
fig.add_trace(go.Histogram(x=df_dead['meal.cal'],name='Dead by the end of the experiment',customdata =customdata ,hovertemplate = hovertemplate )
)

fig.add_trace(go.Histogram(x=df_alive['meal.cal'],name='Alive by the end of the experiment',customdata =customdata ,hovertemplate = hovertemplate )
            
)

fig.update_layout(
    yaxis_title='Count',
    xaxis_title = 'Calories',
    barmode='overlay'
)
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
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

st.session_state['dic'] = df

df_na = df.copy()
df_na.dropna(inplace=True)
df_na = df_na.reset_index() 
df_na["ph.ecog"] = df_na["ph.ecog"].astype("int64")
df_na.pop("index")
df_na = df_na.drop('inst', axis=1)
print(df_na)
st.session_state['dic_noNa'] = df_na

