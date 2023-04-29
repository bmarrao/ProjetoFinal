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

#from st_pages import Page, show_pages, add_page_title,show_pages_from_config
st.set_page_config(page_title = "Lung cancer data analysis" )



filename = './lung-cancer-data.csv'
df = pd.read_csv(filename)

df['status'] = df["status"]-1
df['sex'] = df["sex"]-1
df['wt.loss'] = df['wt.loss'] * 0.45359237


df['sex'] = df['sex'].replace(0, 'Men')
df['sex'] = df['sex'].replace(1, 'Women')
df['status'] = df['status'].replace(0, 'Alive by the end of the experiment')
df['status'] = df['status'].replace(1, 'Dead by the end of the experiment')
grouped=df.groupby(df.status)

df_vivo = grouped.get_group('Alive by the end of the experiment')
df_dead = grouped.get_group('Dead by the end of the experiment')
#Falta o comparativo dos q tavam vivo no experimento
fig = px.histogram(df, x="status",color="status")
st.plotly_chart(fig)

fig = go.Figure()

'''
fig.add_trace(go.Histogram(df,x='sex'))
fig.add_trace(go.Histogram(df_vivo, x='sex'))
fig.add_trace(go.Histogram(df_dead, x='sex'))
st.plotly_chart(fig)
'''

'''Men and women data'''
fig = go.Figure()
fig.add_trace(
    go.Histogram(x=df['sex'],
    name='All men and women')
)
fig.add_trace(go.Histogram(x=df_dead['sex'],name='Dead by the end of the experiment')
)

fig.add_trace(go.Histogram(x=df_vivo['sex'],name='Alive by the end of the experiment')
            
)
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.75)
st.plotly_chart(fig)


fig = px.histogram(df, x="sex", color="sex",hover_data=df.columns)
st.plotly_chart(fig)
st.caption("All men and women on the experiment")

fig = px.histogram(df_dead,color = 'sex', x="sex")
st.plotly_chart(fig)
st.caption("Women and men dead by the end of the experiment")

fig = px.histogram(df_vivo,color='sex', x="sex")
st.plotly_chart(fig)
st.caption("Women and men alive by the end of the experiment")


'''Age data'''
fig = go.Figure()
fig.add_trace(
    go.Histogram(x=df['age'],
    name='All men and women')
)
fig.add_trace(go.Histogram(x=df_dead['age'],name='Dead by the end of the experiment')
)

fig.add_trace(go.Histogram(x=df_vivo['age'],name='Alive by the end of the experiment')
            
)
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.75)
st.plotly_chart(fig)

fig = px.histogram(df, x="age")
st.plotly_chart(fig)
st.caption("All people on the experiment")


fig = px.histogram(df_vivo, x="age")
st.plotly_chart(fig)
st.caption("Alive by the end of the experiment")

fig = px.histogram(df_dead, x="age")
st.plotly_chart(fig)
st.caption("Dead by the end of the experiment")

fig = go.Figure()
fig.add_trace(
    go.Box(x=df['sex'],y=df['age'],
    name='All men and women'))

fig.add_trace(go.Box(x=df_dead['sex'],y=df_dead['age'],name='Dead by the end of the experiment'))

fig.add_trace(go.Box(x=df_vivo['sex'],y=df_vivo['age'],name='Alive by the end of the experiment')
            
)
fig.update_layout(
    yaxis_title='Age',
    boxmode='group' # group together boxes of the different traces for each value of x
)

st.plotly_chart(fig)
#Falta o comparativo dos q tavam vivo no experimento
fig = px.box(df, color = "sex" ,x="sex", y="age", points="all")
st.plotly_chart(fig)

#Falta o comparativo dos q tavam vivo no experimento
fig = px.bar(df, x='sex', y='meal.cal')
st.plotly_chart(fig)


#Falta o comparativo dos q tavam vivo no experimento
fig = px.box(df, x="ph.ecog", y="meal.cal")
st.plotly_chart(fig)


df["ph.karno"].fillna(df["ph.karno"].mean(), inplace = True)
df["pat.karno"].fillna(df["pat.karno"].mean(), inplace = True)
df["meal.cal"].fillna(df["meal.cal"].mean(), inplace = True)
df["wt.loss"].fillna(df["wt.loss"].mean(), inplace = True)
df.dropna(inplace=True)
df["ph.ecog"] = df["ph.ecog"].astype("int64")
df = df.reset_index() 

st.session_state['pergunta1'] = []
st.session_state['pergunta2'] = []
st.session_state['pergunta3'] = []
st.session_state['pergunta5'] = []
st.session_state['pergunta9'] = []

st.session_state['random_forest']= []

st.session_state['dic'] = df
st.title("Survivor Analysis for lung cancer data")
#st.sidebar.sucess("Select a page above")
st.subheader("Survival Forests")
lg_y = df[['status','time']].copy()

lg_y["status"] = lg_y["status"].astype("bool") 

lg_y = lg_y.to_records(index=False)

lg_x = df.drop(["status","time"],axis=1)

random_state = 20

X_train, X_test, y_train, y_test = train_test_split(
    lg_x, lg_y, test_size=0.05, random_state=random_state)

rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           n_jobs=-1,
                           random_state=random_state)
rsf.fit(X_train, y_train)
#print(rsf.fit)
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

