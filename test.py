import streamlit as st
import pandas as pd
import datetime 
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title="Sales Dashboard",layout="wide")
with open('style.css') as s:
    st.markdown(f'<style>{s.read()}<style>',unsafe_allow_html=True)
st.title("Sales Dashboard")
df= pd.read_csv("Order Details.csv")
#df["date"]=pd.to_datetime(df['date'])
df['value']=pd.to_numeric(df['value'])
list = pd.read_csv(r'C:\Users\Rishi\Desktop\Dashboard\List.csv')
#df=pd.merge(df,list[['Date','SKU Codes','Type','PP for Pack Size']],how='left',left_on=['sku_erp_code','date'], right_on=['SKU Codes','Date'])
#df['PP for Pack Size']=df['PP for Pack Size'].astype(float)
#df['Total PP']=0
#for i in df.index:
#    df['Total PP'][i]=df['suom_quantity'][i]*df['PP for Pack Size'][i]

#df=df.groupby(by="order_id").sum()
st.sidebar.header("Please Filter Here:")
Date = st.sidebar.multiselect(
   "Select a Date:",
    options=df['date'].unique(),
    default=df['date'][0]
)
df=df.query(
    "date == @Date"
)

RM = st.sidebar.multiselect(
   "Select a RM:",
    options=df['added_by_name'].unique(),
    default=df['added_by_name'].unique()
)



#st.header("Average Sales per Order:")
ASV=df['value'].sum()/df['order_id'].nunique()
a1,a2,a3,a4=st.columns(4)
a1.metric("Average Sales per Order:",round(ASV,2))
a2.metric("Total No' of Orders:",df['order_id'].nunique())
a3.metric("Lines per Order:",round(df['value'].count()/df['order_id'].nunique(),2))
a4.metric("Last Updated Time:",datetime.datetime.now().strftime("%H:%M"))

Pivot=df.pivot_table(values=["value",'order_id'],index="added_by_name",aggfunc={'value':np.sum,'order_id':pd.Series.nunique})
#st.bar_chart(df["order_value"])
st.header("RM wise GMV")
Pivot
st.header("Top 5 Selling Products by Value")
Pivot2=df.pivot_table(values=["value",'suom_quantity'],index="description",aggfunc={
    "value":np.sum,'suom_quantity':np.sum
    })
Pivot2=Pivot2.reset_index()
Pivot3=Pivot2.nlargest(n=5,columns='value')
Pivot3
df1=df.query(
    'added_by_name == @RM'
)

x=df1.pivot_table(
    values=["value",'order_id'],
    index="Type",
    aggfunc={'value':np.sum,
             'order_id':pd.Series.nunique}
             )
x=x.reset_index()

#layout = Layout(
 #   paper_bgcolor='rgba(0,0,0,0)',
  #  plot_bgcolor='rgba(0,0,0,0)'
#)

plt.pie(
    x['value'],labels=x['Type'],
    autopct='%.1f%%')
my_circle=plt.Circle( (0,0), 0.7, color="white")
p=plt.gcf()
#p.set_facecolor("darkcyan")
p.gca().add_artist(my_circle)

g1,g2=st.columns(2)
g2.pyplot(plt)
g1.header("Item Type- GMV Distribution")