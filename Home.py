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

# Inicialization of the streamlit page, with its title
st.set_page_config(page_title = "Lung cancer trial data analysis" )

st.title("Lung cancer trial data analysis.")


filename = './lung-cancer-data.csv'
# Reading the data from the csv file using the pandas dataframe , we use the pandas dataframe
# to make it easier to make the graphs and operations such as grouping data by the age group
df = pd.read_csv(filename)

# Changing status from 2 - dead , 1 - censored to 1 - dead and 0 - censored 
df['status'] = df["status"]-1
# Changing sex from 2 - Woman , 1 - Man to 1 - Woman and 0 - Man
df['sex'] = df["sex"]-1
# Changing weight loss from pounds to kilograms
df['wt.loss'] = df['wt.loss'] * 0.45359237

# In here we will be replacing the values so that we can create prettier graphs
df['sex'] = df['sex'].replace(0, 'Men')
df['sex'] = df['sex'].replace(1, 'Women')
df['status'] = df['status'].replace(0, 'Alive by the end of the experiment')
df['status'] = df['status'].replace(1, 'Dead by the end of the experiment')

# In here we create a copy of the original dataframe without any type of absent data
df_na = df.copy()
df_na.dropna(inplace=True)
df_na = df_na.reset_index() 
df_na["ph.ecog"] = df_na["ph.ecog"].astype("int64")
df_na.pop("index")
grouped_na=df_na.groupby(df_na.status)
dfna_alive = grouped_na.get_group('Alive by the end of the experiment')
dfna_dead = grouped_na.get_group('Dead by the end of the experiment')


'''
Project made by : Breno Fernando Guerra Marrão - A97768 , Tiago Passos Rodrigues - A96414 , Tales André Rovaris Machado - A96314\n
In this project we will be analyzing data from a study of patients with advanced lung cancer in a clinical trial of a new treatment , the Data has the following atributtes:\n
inst: code of the instituion\n 
Time: time of survival in day \n
status: censured = 0 and  dead = 1\n
Age : In years \n 
sex : Male = 0, Female = 1\n
ph.ecog: ECOG performance score as assessed by physician. 0 = asymptomatic, 1 = symptomatic but fully ambulatory, 2 = bedridden <50% of the day, 3 = bedridden >50% of the day but not bedridden, 4 = bedridden\n
ph.karno: Karnofsky performance score (poor = 0-good = 100) as assessed by physician\n
pat.karno: Karnofsky Performance Score as rated by the patient\n
meal.cal: Calories per meal\n
wt.loss: Weight loss in  (kg)
'''


# Creation of dataframes to compare data from people that stayed alive at the end of the experiment and for those who didn't
grouped=df.groupby(df.status)

df_alive = grouped.get_group('Alive by the end of the experiment')
df_dead = grouped.get_group('Dead by the end of the experiment')
df_alive = grouped.get_group('Alive by the end of the experiment')
df_dead = grouped.get_group('Dead by the end of the experiment')
# Here we create a template that we have to use in plotly in order to show data when we hover with the mouse .


# In here we create variables in session_state, that means that this data will be acessible for all the pages, now we can store all the data the 
# user inputs from all of the pages and we can also initiate and treat the data only one time

st.session_state['pergunta1'] = []
st.session_state['pergunta2'] = []
st.session_state['pergunta3'] = []
st.session_state['pergunta5'] = []
st.session_state['pergunta9'] = []
st.session_state['random_forest']= []
st.session_state['dic1'] = df 
st.session_state['dicalive'] = df_alive
st.session_state['dicdead'] = df_dead


st.header("Tables ")

st.subheader("All the data")
st.dataframe(df)

# Here we create the download button to save the information that was used in this project, using the previous dataframe that was created
# as well as the alive and dead people

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

# In this section we start to show some graphs that are important to the understanding of the variables used in other pages

st.header("Graphs")

st.subheader("Censored data")

# Here we create a histogram with the amount of people dead and alive by the end the experiment
fig = px.histogram(df, x="status",color="status")
st.plotly_chart(fig)

fig = go.Figure()

# This section of the code creates a simple histogram showing the amount of man and woman that participated in the experiment
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

# Defing what values to use on the distribrution plot and converting to numpy 
hist_data = [df['age'].to_numpy(), df_dead['age'].to_numpy(), df_alive['age'].to_numpy()]

# Definining the name for each element on hist_data 
group_labels = ['All data', 'Dead by the end of the experiment', 'Alive by the end of the experiment']
# Picking the colors of each label
colors = ['#393E46', '#2BCDC1', '#F66095']

# Creating distribution plot with bin_size of 5 , so that we can group data and create a better looking graph
fig = ff.create_distplot(hist_data, group_labels,colors=colors,bin_size=5,show_rug = False)
# In here we update ou graph so that we can label the y and x axis .
fig.update_layout(
    yaxis_title='Density',
    xaxis_title = 'Age',
)
# Ploting the graph
st.plotly_chart(fig)

# Initiating a figure
fig = go.Figure()
# Adding a graph to the figure
fig.add_trace(
    go.Histogram(x=df['age'],
    name='All data'),
)
# Adding a graph to the figure
fig.add_trace(go.Histogram(x=df_dead['age'],name='Dead by the end of the experiment')
)
# Adding a graph to the figure
fig.add_trace(go.Histogram(x=df_alive['age'],name='Alive by the end of the experiment')
            
)

# In here we update our graph so that we can label the y and x axis and set the barmode to overlay 

fig.update_layout(
    yaxis_title='Count',
    xaxis_title = 'Age',
    barmode='overlay'
)

# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
# Ploting the graph
st.plotly_chart(fig)



# Similar to before this section is the histogram of the different calories consumed per day
st.subheader("Calories per meal across the data")


# Defing what values to use on the distribrution plot and converting to numpy 
hist_data = [df_na['meal.cal'].to_numpy(), dfna_dead['meal.cal'].to_numpy(), dfna_alive['meal.cal'].to_numpy()]
# Definining the name for each element on hist_data
group_labels = ['All data', 'Dead by the end of the experiment', 'Alive by the end of the experiment']
# Picking the colors of each label
colors = ['#393E46', '#2BCDC1', '#F66095']
# Creating distribution plot with bin_size of 5, so that we can group data and create a better looking graph

fig = ff.create_distplot(hist_data, group_labels,colors=colors,bin_size=150, show_rug=False)
# In here we update our graph so that we can label the y and x axis .

fig.update_layout(
    yaxis_title='Density',
    xaxis_title = 'Calories',
)
# Plotting the graph

st.plotly_chart(fig)


# Histogram of ECOG evaluations
st.subheader("Histogram of patients with different ecog evaluations")

# Initiating a figure
fig = go.Figure()
# Adding a graph to the figure

fig.add_trace( go.Histogram( x=df["ph.ecog"],name = 'All patients'))
# Adding a graph to the figure

fig.add_trace( go.Histogram( x=df_dead["ph.ecog"],name = 'Dead by the end of experiment'))
# Adding a graph to the figure

fig.add_trace( go.Histogram( x=df_alive["ph.ecog"],name = 'Alive by the end of experiment'))
# Labeling the y and x axis
fig.update_layout(
    yaxis_title='count',
    xaxis_title='Patient ecog level',
    boxmode='group')

# Plotting the graph
st.plotly_chart(fig)

# Histogram of karnofsky score

st.subheader("Histogram of patients own evaluation of Karnofsky score")
# Initiating a figure
fig = go.Figure()

# Adding a graph to the figure
fig.add_trace( go.Histogram( x=df["pat.karno"],name = 'All patients'))

# Adding a graph to the figure
fig.add_trace( go.Histogram( x=df_dead["pat.karno"],name = 'Dead by the end of experiment'))

# Adding a graph to the figure
fig.add_trace( go.Histogram( x=df_alive["pat.karno"],name = 'Alive by the end of experiment'))
                         
# Labeling the y and x axis and defining the mode of the bar graph in this instance overlay
fig.update_layout(
    yaxis_title='count',
    xaxis_title='Patient Karnofsky score',
    barmode='overlay')

fig.update_traces(opacity=0.75)

# Ploting the graph
st.plotly_chart(fig)

# Histogram of weight loss

st.subheader("Calories per meal across the data")
# Initiating a figure
fig = go.Figure()
# Adding a graph to the figure

fig.add_trace(
    go.Histogram(x=df['meal.cal'],
    name='All data'),
)
# Adding a graph to the figure

fig.add_trace(go.Histogram(x=df_dead['meal.cal'],name='Dead by the end of the experiment')
)
# Adding a graph to the figure

fig.add_trace(go.Histogram(x=df_alive['meal.cal'],name='Alive by the end of the experiment')
            
)
# Labeling the y and x axis .

fig.update_layout(
    yaxis_title='Count',
    xaxis_title = 'Calories per meal',
    barmode='overlay'
)
# Altering the opacity so that we can obtain a better looking graph
fig.update_traces(opacity=0.75)
# Plotting the graph
st.plotly_chart(fig)

# Here we replace the annotation that we previously set for easier graph comprehension to numbers so that we can apply the data to models such as 
# Cox-ph fitter and survival forests

df['sex'] = df['sex'].replace('Men', 0)
df['sex'] = df['sex'].replace('Women',1)
df['status'] = df['status'].replace('Alive by the end of the experiment',0)
df['status'] = df['status'].replace('Dead by the end of the experiment',1)

# Defining the main data for the other pages with the data in numbers
st.session_state['dic'] = df

# This section we create a variable for the other pages , this variable is for the models that didn't 
# accept absent data in certain values so we drop them  so that we can apply those models

df_na = df.copy()
df_na.dropna(inplace=True)
df_na = df_na.reset_index() 
df_na["ph.ecog"] = df_na["ph.ecog"].astype("int64")
df_na.pop("index")
df_na = df_na.drop('inst', axis=1)
st.session_state['dic_noNa'] = df_na

