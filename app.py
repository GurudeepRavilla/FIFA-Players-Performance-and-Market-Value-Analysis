# ==========================================================
# FIFA PLAYER ANALYTICS DASHBOARD
# Master's Data Visualization Project
# Part 1 - Project Setup
# ==========================================================

# -------------------------
# IMPORT LIBRARIES
# -------------------------

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -------------------------
# PAGE CONFIGURATION
# -------------------------
st.markdown("""
<style>

.stApp{
  <style>

.stApp {
    <style>

.stApp {
    <style>

.stApp {
    background-image:
        linear-gradient(rgba(0,0,0,.82), rgba(0,0,0,.82)),
        url("https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a?auto=format&fit=crop&w=1920&q=80");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

</style>""", unsafe_allow_html=True)

st.set_page_config(
    page_title="FIFA Player Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CUSTOM CSS
# -------------------------

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.block-container{
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

h1,h2,h3,h4{
    color:white;
}

div[data-testid="metric-container"]{
    background:#1E1E1E;
    border-radius:12px;
    padding:15px;
    border:1px solid #333333;
}

div[data-testid="metric-container"]:hover{
    border:1px solid #00CC66;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------

st.title("⚽ FIFA Player Analytics Dashboard")

st.markdown(
"""
Interactive Data Visualization using **Streamlit** and **Plotly**

Master's Data Visualization Project
"""
)

st.markdown("---")

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_data():
   df = pd.read_csv("fifa_players.csv")
   return df
df = load_data()

# -------------------------
# CLEAN COLUMN NAMES
# -------------------------

df.columns = df.columns.str.strip()

# -------------------------
# REMOVE DUPLICATES
# -------------------------

df = df.drop_duplicates()

# -------------------------
# CONVERT NUMERIC COLUMNS
# -------------------------

numeric_columns = [

    "age",
    "height_cm",
    "weight_kgs",
    "overall_rating",
    "potential",
    "value_euro",
    "wage_euro"

]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# -------------------------
# HANDLE MISSING VALUES
# -------------------------

for col in numeric_columns:

    if col in df.columns:

        df[col] = df[col].fillna(df[col].median())

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("Dashboard Filters")

# Player Search

search_player = st.sidebar.text_input(
    "Search Player"
)

# Age Filter

min_age = int(df["age"].min())
max_age = int(df["age"].max())

age_range = st.sidebar.slider(

    "Age",

    min_age,
    max_age,

    (min_age, max_age)

)

# Rating Filter

min_rating = int(df["overall_rating"].min())
max_rating = int(df["overall_rating"].max())

rating_range = st.sidebar.slider(

    "Overall Rating",

    min_rating,
    max_rating,

    (min_rating, max_rating)

)

# Nationality

countries = sorted(df["nationality"].dropna().unique())

selected_country = st.sidebar.multiselect(

    "Nationality",

    countries

)

# Position

positions = sorted(df["positions"].dropna().unique())

selected_position = st.sidebar.multiselect(

    "Position",

    positions

)

# -------------------------
# APPLY FILTERS
# -------------------------

filtered_df = df.copy()

filtered_df = filtered_df[

    (filtered_df["age"] >= age_range[0]) &
    (filtered_df["age"] <= age_range[1])

]

filtered_df = filtered_df[

    (filtered_df["overall_rating"] >= rating_range[0]) &
    (filtered_df["overall_rating"] <= rating_range[1])

]

if search_player != "":

    filtered_df = filtered_df[

        filtered_df["name"].str.contains(
            search_player,
            case=False,
            na=False
        )

    ]

if len(selected_country) > 0:

    filtered_df = filtered_df[

        filtered_df["nationality"].isin(selected_country)

    ]

if len(selected_position) > 0:

    filtered_df = filtered_df[

        filtered_df["positions"].isin(selected_position)

    ]

st.sidebar.markdown("---")

st.sidebar.success(

    f"Players Selected : {len(filtered_df):,}"

)

# -------------------------
# DATA PREVIEW
# -------------------------

st.subheader("Dataset Preview")

st.dataframe(

    filtered_df,

    use_container_width=True,

    height=500

)

st.info(
    f"Dataset contains **{len(filtered_df):,}** players after applying the selected filters."
)

# ==========================================================
# END OF PART 1
# ==========================================================
# ==========================================================
# PART 2 - KPI DASHBOARD & DATA OVERVIEW
# ==========================================================

st.markdown("---")
st.header("📊 Dashboard Overview")

# -------------------------
# KPI CALCULATIONS
# -------------------------

total_players = len(filtered_df)

avg_rating = round(filtered_df["overall_rating"].mean(), 2)

avg_age = round(filtered_df["age"].mean(), 1)

avg_value = round(filtered_df["value_euro"].mean() / 1_000_000, 2)

avg_wage = round(filtered_df["wage_euro"].mean() / 1000, 2)

highest_rating = int(filtered_df["overall_rating"].max())

highest_value = filtered_df["value_euro"].max()

# -------------------------
# KPI CARDS
# -------------------------

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "👥 Players",
        f"{total_players:,}"
    )

with c2:
    st.metric(
        "⭐ Avg Rating",
        avg_rating
    )

with c3:
    st.metric(
        "🎂 Avg Age",
        avg_age
    )

with c4:
    st.metric(
        "💰 Avg Value (€M)",
        avg_value
    )

with c5:
    st.metric(
        "💵 Avg Wage (€K)",
        avg_wage
    )

st.markdown("---")

# -------------------------
# DATASET INFORMATION
# -------------------------

left, right = st.columns([2, 1])

with left:

    st.subheader("📋 Dataset Information")

    info_df = pd.DataFrame({

        "Property": [

            "Rows",
            "Columns",
            "Highest Rating",
            "Highest Value (€)",
            "Average Rating",
            "Average Age"

        ],

        "Value": [

            len(filtered_df),
            len(filtered_df.columns),
            highest_rating,
            f"{highest_value:,.0f}",
            avg_rating,
            avg_age

        ]

    })

    st.dataframe(
        info_df,
        use_container_width=True,
        hide_index=True
    )

with right:

    st.subheader("📊 Missing Values")

    missing = filtered_df.isnull().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:

        st.success("✅ No missing values")

    else:

        st.dataframe(

            missing.reset_index().rename(

                columns={
                    "index": "Column",
                    0: "Missing Values"
                }

            ),

            hide_index=True,

            use_container_width=True

        )

st.markdown("---")

# -------------------------
# NUMERICAL SUMMARY
# -------------------------

st.subheader("📈 Statistical Summary")

numeric_cols = [

    "age",
    "height_cm",
    "weight_kgs",
    "overall_rating",
    "potential",
    "value_euro",
    "wage_euro"

]

available_numeric = [

    col for col in numeric_cols

    if col in filtered_df.columns

]

st.dataframe(

    filtered_df[available_numeric].describe().round(2),

    use_container_width=True

)

st.markdown("---")

# -------------------------
# DOWNLOAD FILTERED DATA
# -------------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="📥 Download Filtered Dataset",

    data=csv,

    file_name="Filtered_FIFA_Players.csv",

    mime="text/csv"

)

st.markdown("---")

st.success(
"""
### ✅ Dashboard Summary

- Interactive filtering by player, nationality, position, age and rating.
- Live KPI cards update automatically.
- Statistical summary of the filtered dataset.
- Download the filtered dataset as a CSV file.
"""
)

# ==========================================================
# END OF PART 2
# ==========================================================
# ==========================================================
# PART 3 - PLAYER ANALYTICS
# ==========================================================

st.header("🏆 Player Analytics")

# ----------------------------------------------------------
# TOP 10 HIGHEST RATED PLAYERS
# ----------------------------------------------------------

st.subheader("⭐ Top 10 Highest Rated Players")

top_rating = (
    filtered_df
    .sort_values("overall_rating", ascending=False)
    .head(10)
)

fig = px.bar(
    top_rating,
    x="name",
    y="overall_rating",
    color="overall_rating",
    text="overall_rating",
    hover_data=[
        "age",
        "nationality",
        "positions"
    ],
    color_continuous_scale="Viridis"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Player",
    yaxis_title="Overall Rating",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# TOP 10 MOST VALUABLE PLAYERS
# ----------------------------------------------------------

st.subheader("💰 Top 10 Most Valuable Players")

top_value = (
    filtered_df
    .sort_values("value_euro", ascending=False)
    .head(10)
)

fig = px.bar(
    top_value,
    x="name",
    y="value_euro",
    color="overall_rating",
    text="value_euro",
    hover_data=[
        "age",
        "nationality",
        "positions"
    ],
    color_continuous_scale="Turbo"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Player",
    yaxis_title="Market Value (€)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# TOP 10 HIGHEST WAGE PLAYERS
# ----------------------------------------------------------

st.subheader("💵 Top 10 Highest Wage Players")

top_wage = (
    filtered_df
    .sort_values("wage_euro", ascending=False)
    .head(10)
)

fig = px.bar(
    top_wage,
    x="name",
    y="wage_euro",
    color="wage_euro",
    text="wage_euro",
    color_continuous_scale="Plasma"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Player",
    yaxis_title="Weekly Wage (€)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# VALUE VS RATING
# ----------------------------------------------------------

st.subheader("📈 Market Value vs Overall Rating")

scatter_df = filtered_df[
    [
        "name",
        "overall_rating",
        "value_euro",
        "potential",
        "age",
        "nationality",
        "positions"
    ]
].copy()

scatter_df = scatter_df.dropna()

fig = px.scatter(

    scatter_df,

    x="overall_rating",

    y="value_euro",

    color="potential",

    size="potential",

    hover_name="name",

    hover_data=[
        "age",
        "nationality",
        "positions"
    ],

    color_continuous_scale="Viridis"

)

fig.update_layout(
    template="plotly_dark",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# AGE VS RATING
# ----------------------------------------------------------

st.subheader("🎯 Age vs Overall Rating")

age_df = filtered_df[
    [
        "name",
        "age",
        "overall_rating",
        "potential",
        "positions"
    ]
].dropna()

fig = px.scatter(

    age_df,

    x="age",

    y="overall_rating",

    color="potential",

    size="overall_rating",

    hover_name="name",

    hover_data=["positions"],

    color_continuous_scale="Cividis"

)

fig.update_layout(
    template="plotly_dark",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# PLAYER TABLE
# ----------------------------------------------------------

st.subheader("📋 Top Players Overview")

table = filtered_df[
    [
        "name",
        "age",
        "nationality",
        "positions",
        "overall_rating",
        "potential",
        "value_euro",
        "wage_euro"
    ]
].sort_values(
    "overall_rating",
    ascending=False
)

st.dataframe(
    table,
    use_container_width=True,
    height=450
)

st.success("""

### 📌 Insights

• Identify the highest-rated players.

• Compare market value with player rating.

• Observe how age influences player ratings.

• Explore wage distribution among elite footballers.

• Review detailed player information interactively.

""")

# ==========================================================
# END OF PART 3
# ==========================================================
# ==========================================================
# PART 4 - NATIONALITY ANALYTICS
# ==========================================================

st.header("🌍 Nationality Analytics")

# ----------------------------------------------------------
# COUNTRY PLAYER COUNT
# ----------------------------------------------------------

country_count = (
    filtered_df.groupby("nationality")
    .size()
    .reset_index(name="Players")
    .sort_values("Players", ascending=False)
)

top15 = country_count.head(15)

st.subheader("🏆 Top 15 Countries by Number of Players")

fig = px.bar(
    top15,
    x="nationality",
    y="Players",
    color="Players",
    text="Players",
    color_continuous_scale="Blues"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Country",
    yaxis_title="Players",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# PIE CHART
# ----------------------------------------------------------

st.subheader("🥧 Top 10 Nationalities")

fig = px.pie(
    top15.head(10),
    names="nationality",
    values="Players",
    hole=0.45
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# AVERAGE RATING
# ----------------------------------------------------------

avg_rating_country = (
    filtered_df.groupby("nationality")["overall_rating"]
    .mean()
    .reset_index()
)

avg_rating_country = (
    avg_rating_country
    .merge(country_count, on="nationality")
)

# Ignore countries with very few players
avg_rating_country = avg_rating_country[
    avg_rating_country["Players"] >= 5
]

avg_rating_country = (
    avg_rating_country
    .sort_values("overall_rating", ascending=False)
    .head(15)
)

st.subheader("⭐ Top Countries by Average Rating")

fig = px.bar(
    avg_rating_country,
    x="nationality",
    y="overall_rating",
    color="overall_rating",
    text=avg_rating_country["overall_rating"].round(1),
    color_continuous_scale="Viridis"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Country",
    yaxis_title="Average Rating",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# TREEMAP
# ----------------------------------------------------------

st.subheader("🌳 Nationality Treemap")

tree = country_count.merge(
    avg_rating_country[["nationality", "overall_rating"]],
    on="nationality",
    how="left"
)

tree["overall_rating"] = tree["overall_rating"].fillna(
    tree["overall_rating"].mean()
)

fig = px.treemap(
    tree,
    path=["nationality"],
    values="Players",
    color="overall_rating",
    color_continuous_scale="RdYlGn"
)

fig.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# SUMMARY TABLE
# ----------------------------------------------------------

st.subheader("📋 Nationality Summary")

summary = (
    filtered_df.groupby("nationality")
    .agg(
        Players=("name", "count"),
        Average_Rating=("overall_rating", "mean"),
        Average_Age=("age", "mean"),
        Average_Value=("value_euro", "mean"),
        Average_Wage=("wage_euro", "mean")
    )
    .sort_values("Players", ascending=False)
)

summary["Average_Rating"] = summary["Average_Rating"].round(2)
summary["Average_Age"] = summary["Average_Age"].round(1)
summary["Average_Value"] = summary["Average_Value"].round(0)
summary["Average_Wage"] = summary["Average_Wage"].round(0)

st.dataframe(
    summary,
    use_container_width=True,
    height=450
)

st.markdown("---")

# ----------------------------------------------------------
# INSIGHTS
# ----------------------------------------------------------

most_players = summary.index[0]
num_players = int(summary.iloc[0]["Players"])

best_rating = (
    summary.sort_values(
        "Average_Rating",
        ascending=False
    ).index[0]
)

highest_value = (
    summary.sort_values(
        "Average_Value",
        ascending=False
    ).index[0]
)

st.success(f"""

### 📌 Nationality Insights

- 🌍 **{most_players}** has the largest number of players (**{num_players}**).

- ⭐ **{best_rating}** has the highest average player rating.

- 💰 **{highest_value}** has the highest average market value.

- 📊 These visualizations reveal the strongest football-producing nations and compare player quality, value, and representation across countries.

""")

# ==========================================================
# END OF PART 4
# ==========================================================
# ==========================================================
# PART 5 - ADVANCED DASHBOARD
# ==========================================================

st.header("📊 Advanced Player Insights")

tab1, tab2, tab3 = st.tabs([
    "🔥 Correlation",
    "⚽ Positions",
    "⭐ Player Comparison"
])

# ---------------- CORRELATION ----------------

with tab1:

    st.subheader("Correlation Heatmap")

    numeric = filtered_df.select_dtypes(include="number")

    corr = numeric.corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )

    fig.update_layout(
        template="plotly_dark",
        height=650
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- POSITIONS ----------------

with tab2:

    temp = filtered_df.copy()

    temp["Primary Position"] = (
        temp["positions"]
        .str.split(",")
        .str[0]
    )

    position = (
        temp.groupby("Primary Position")
        .size()
        .reset_index(name="Players")
        .sort_values("Players", ascending=False)
    )

    fig = px.treemap(
        position,
        path=["Primary Position"],
        values="Players",
        color="Players",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        template="plotly_dark",
        height=650
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- PLAYER COMPARISON ----------------

with tab3:

    players = sorted(filtered_df["name"].unique())

    p1 = st.selectbox("Player 1", players)

    p2 = st.selectbox("Player 2", players, index=1)

    compare = filtered_df[
        filtered_df["name"].isin([p1, p2])
    ]

    radar = go.Figure()

    metrics = [
        "overall_rating",
        "potential",
        "age"
    ]

    for _, row in compare.iterrows():

        radar.add_trace(go.Scatterpolar(
            r=[row[m] for m in metrics],
            theta=["Rating","Potential","Age"],
            fill="toself",
            name=row["name"]
        ))

    radar.update_layout(
        template="plotly_dark",
        polar=dict(radialaxis=dict(visible=True)),
        height=650
    )

    st.plotly_chart(radar, use_container_width=True)

# ==========================================================
# ==========================================================
# CONCLUSION & KEY INSIGHTS
# ==========================================================

st.markdown("---")

st.header("📌 Conclusion & Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.success("""
### 📊 Major Findings

- ⭐ Players with higher overall ratings generally have higher market values.
- 💰 Market value and wages show a positive relationship.
- 🌍 A few countries contribute a large share of professional football players.
- ⚽ Different playing positions have distinct rating and value distributions.
- 🎯 Younger players often possess higher growth potential.
""")

with col2:
    st.info("""
### 🎓 Project Summary

This dashboard demonstrates how interactive data visualization can help explore football player performance, market value, wages, and nationality trends.

By combining Streamlit and Plotly, users can filter players, compare statistics, and gain meaningful insights from the FIFA dataset through an intuitive and interactive interface.
""")

st.markdown("---")

st.markdown(
"""
<div style="text-align:center; padding:20px; border-radius:10px; background-color:#1f2937;">
    <h2>⚽ FIFA Player Analytics Dashboard</h2>
    <h4>Master's Data Visualization Project</h4>
    <p>Developed using <b>Python • Streamlit • Plotly • Pandas</b></p>
    <p>Thank you for exploring the dashboard!</p>
</div>
""",
unsafe_allow_html=True)
