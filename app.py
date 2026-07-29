
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FIFA Dashboard",layout="wide")

@st.cache_data
def load():
    return pd.read_csv("data/fifa_players.csv")

df=load()

st.title("⚽ FIFA Players Data Visualization Dashboard")

st.sidebar.header("Filters")

if "nationality" in df.columns:
    nations=sorted(df["nationality"].dropna().unique())
    selected=st.sidebar.multiselect("Nationality",nations)
    if selected:
        df=df[df["nationality"].isin(selected)]

if "age" in df.columns:
    mn,mx=int(df["age"].min()),int(df["age"].max())
    ages=st.sidebar.slider("Age",mn,mx,(mn,mx))
    df=df[(df["age"]>=ages[0])&(df["age"]<=ages[1])]

c1,c2,c3,c4=st.columns(4)
c1.metric("Players",len(df))
if "overall_rating" in df.columns:
    c2.metric("Avg Rating",round(df["overall_rating"].mean(),1))
if "value_euro" in df.columns:
    c3.metric("Avg Value (€)",f"{df['value_euro'].mean():,.0f}")
if "wage_euro" in df.columns:
    c4.metric("Avg Wage (€)",f"{df['wage_euro'].mean():,.0f}")

st.subheader("Dataset")
st.dataframe(df.head(100),use_container_width=True)

left,right=st.columns(2)

if "overall_rating" in df.columns and "value_euro" in df.columns:
    fig=px.scatter(df,x="value_euro",y="overall_rating",color="age" if "age" in df.columns else None,
                   hover_name="short_name" if "short_name" in df.columns else None,
                   title="Player Value vs Overall Rating")
    left.plotly_chart(fig,use_container_width=True)

if "nationality" in df.columns:
    top=df["nationality"].value_counts().head(10).reset_index()
    top.columns=["Nationality","Players"]
    fig=px.bar(top,x="Nationality",y="Players",title="Top Nationalities")
    right.plotly_chart(fig,use_container_width=True)

left,right=st.columns(2)

if "overall_rating" in df.columns:
    fig=px.histogram(df,x="overall_rating",nbins=20,title="Overall Rating Distribution")
    left.plotly_chart(fig,use_container_width=True)

num=df.select_dtypes(include="number")
if not num.empty:
    corr=num.corr(numeric_only=True)
    fig=px.imshow(corr,text_auto=".2f",title="Correlation Heatmap")
    right.plotly_chart(fig,use_container_width=True)

if "positions" in df.columns:
    st.subheader("Top Positions")
    p=df["positions"].astype(str).str.split(",").str[0].value_counts().head(10).reset_index()
    p.columns=["Position","Players"]
    st.plotly_chart(px.bar(p,x="Position",y="Players"),use_container_width=True)

csv=df.to_csv(index=False).encode("utf-8")
st.download_button("Download Filtered CSV",csv,"filtered_fifa_players.csv","text/csv")

st.markdown("---")
st.markdown("**Data Visualization Project | Streamlit Dashboard**")
