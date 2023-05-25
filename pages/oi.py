
labels = ['40','50','60','70','80','90','100']

mean = df.groupby(pd.cut(df['ph.karno'],[30,40,50,60,70,80,90,100]),as_index=False).mean()
mean["ph.karn"] = labels


labels = ['40','50','60','70','80','90','100']

mean = df.groupby(pd.cut(df['ph.karno'],[30,40,50,60,70,80,90,100]),as_index=False).mean()
mean["ph.karn"] = labels

fig = px.pie(mean, values='meal.cal', names='ph.karn', title='Medic Evaluation compared to calories consumed',hole = 0.4)
fig.update_layout(legend_traceorder="normal")
st.plotly_chart(fig)

labels = ['40','50','60','70','80','90','100']

mean = df.groupby(pd.cut(df['pat.karno'],[30,40,50,60,70,80,90,100]),as_index=False).mean()
mean["ph.karn"] = labels



fig = px.pie(mean, values='meal.cal', names='ph.karn', title='Patient Evaluation compared to calories consumed',hole = 0.4)
st.plotly_chart(fig)
