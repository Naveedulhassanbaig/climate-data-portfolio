# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Climate Data Analyst Portfolio", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #0b1a14; }
  .hero-title { font-size:3rem; font-weight:800; color:#00c896; text-align:center; margin-bottom:0.2rem; }
  .hero-sub   { font-size:1.15rem; color:#a0c8b0; text-align:center; margin-bottom:2rem; }
  .metric-card{ background:#112a1e; border:1px solid #1e4d35; border-radius:12px; padding:1.2rem 1.5rem; text-align:center; }
  .metric-card .val{ font-size:2rem; font-weight:700; color:#00c896; }
  .metric-card .lab{ font-size:0.82rem; color:#6fa888; margin-top:4px; }
  .section-title{ font-size:1.5rem; font-weight:700; color:#e8f5ee; border-left:4px solid #00c896; padding-left:12px; margin:2rem 0 1rem; }
  .insight-box{ background:#112a1e; border-left:3px solid #00c896; border-radius:8px; padding:1rem 1.2rem; margin-top:1rem; color:#a0c8b0; font-size:0.92rem; line-height:1.6; }
  .badge{ display:inline-block; background:#1e4d35; color:#00c896; border-radius:6px; padding:2px 10px; font-size:0.78rem; margin:2px; font-weight:600; }
  footer{ visibility:hidden; }
</style>
""", unsafe_allow_html=True)

DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

EXCLUDE = ["World","Asia","Europe","Africa","North America","South America",
           "Oceania","European Union (27)","High-income countries","Low-income countries",
           "Middle East (GCP)","Upper-middle-income countries","Lower-middle-income countries",
           "Asia (excl. China and India)","Europe (excl. EU-27)","Europe (excl. EU-28)",
           "North America (excl. USA)"]
countries_df = df[~df["country"].isin(EXCLUDE)].copy()
world_df     = df[df["country"] == "World"].copy()

with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio("Navigation", [
        "About Me","Global CO2 Trend","Top Emitters",
        "Temperature Impact","Energy Sources","Emissions vs GDP"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### Skills")
    for s in ["Python","Pandas","Plotly","Streamlit","Data Viz","Climate Analysis","SQL","Statistics"]:
        st.markdown(f'<span class="badge">{s}</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Dataset:** Our World in Data")
    st.caption("50,411 rows x 79 columns x 1750-2024")

if page == "About Me":
    st.markdown('<div class="hero-title">Climate Data Analyst Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Turning climate data into actionable insights</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown('<div class="metric-card"><div class="val">37.4B</div><div class="lab">Tonnes CO2 in 2023</div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="val">+1.45C</div><div class="lab">Global warming</div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="val">254</div><div class="lab">Countries</div></div>', unsafe_allow_html=True)
    c4.markdown('<div class="metric-card"><div class="val">274 yrs</div><div class="lab">Data coverage</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 5 Projects Inside")
    for p in [("Global CO2 Trend","Time series 1900-2024"),("Top Emitters","Total vs per capita"),
              ("Temperature Impact","Historical warming by country"),("Energy Sources","Coal/Oil/Gas over time"),
              ("Emissions vs GDP","Wealth vs pollution")]:
        st.markdown(f"**{p[0]}** - *{p[1]}*")

elif page == "Global CO2 Trend":
    st.markdown('<div class="section-title">Global CO2 Emissions Trend (1900-2024)</div>', unsafe_allow_html=True)
    trend = world_df[world_df["year"]>=1900][["year","co2"]].dropna()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trend["year"], y=trend["co2"], mode="lines", fill="tozeroy",
        line=dict(color="#00c896", width=2.5), fillcolor="rgba(0,200,150,0.15)", name="World CO2"))
    events = {1929:"Great Depression",1945:"WWII End",1973:"Oil Crisis",2008:"Financial Crisis",2020:"COVID-19"}
    for yr, label in events.items():
        val = trend[trend["year"]==yr]["co2"]
        if not val.empty:
            fig.add_vline(x=yr, line_dash="dash", line_color="rgba(255,200,100,0.6)", line_width=1.5)
            fig.add_annotation(x=yr, y=float(val.values[0])+2.5, text=label, showarrow=False,
                font=dict(size=9, color="#ffc864"), textangle=-90)
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e",
        height=480, xaxis_title="Year", yaxis_title="CO2 (billion tonnes)", hovermode="x unified",
        title="Global CO2 Emissions (1900-2024)")
    st.plotly_chart(fig, use_container_width=True)
    growth = world_df[world_df["year"]>=1960][["year","co2_growth_prct"]].dropna()
    fig2 = px.bar(growth, x="year", y="co2_growth_prct", color="co2_growth_prct",
        color_continuous_scale=["#00c896","#ffc864","#ff4444"],
        title="Year-on-Year CO2 Growth Rate (%)", labels={"co2_growth_prct":"Growth %","year":"Year"})
    fig2.add_hline(y=0, line_color="white", line_width=0.8)
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e",
        height=340, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="insight-box">Key Insight: Global CO2 rose 20x since 1900. COVID-19 caused the largest single-year drop (-5.4%) in 2020, yet 2021 saw an immediate record rebound.</div>', unsafe_allow_html=True)

elif page == "Top Emitters":
    st.markdown('<div class="section-title">Top CO2 Emitters</div>', unsafe_allow_html=True)
    year_sel = st.slider("Select Year", 1990, 2023, 2023, 1)
    top_total  = countries_df[countries_df["year"]==year_sel][["country","co2","share_global_co2"]]\
        .dropna().sort_values("co2", ascending=False).head(15)
    top_percap = countries_df[countries_df["year"]==year_sel][["country","co2_per_capita"]]\
        .dropna().sort_values("co2_per_capita", ascending=False).head(15)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("**Total CO2 (billion tonnes)**")
        fig = px.bar(top_total.sort_values("co2"), x="co2", y="country", orientation="h",
            color="co2", color_continuous_scale="Greens", labels={"co2":"CO2","country":""})
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e",
            height=480, coloraxis_showscale=False, margin=dict(l=0,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("**CO2 Per Capita (tonnes/person)**")
        fig2 = px.bar(top_percap.sort_values("co2_per_capita"), x="co2_per_capita", y="country",
            orientation="h", color="co2_per_capita", color_continuous_scale="Oranges",
            labels={"co2_per_capita":"Per Capita","country":""})
        fig2.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e",
            height=480, coloraxis_showscale=False, margin=dict(l=0,r=10,t=10,b=10))
        st.plotly_chart(fig2, use_container_width=True)
    top8  = top_total.head(8).copy()
    rest  = pd.DataFrame([{"country":"Rest of World","share_global_co2":100-top8["share_global_co2"].sum()}])
    pie_df = pd.concat([top8[["country","share_global_co2"]], rest], ignore_index=True)
    fig3 = px.pie(pie_df, values="share_global_co2", names="country",
        title="Global CO2 Share - Top 8 Countries",
        color_discrete_sequence=px.colors.sequential.Greens_r, hole=0.45)
    fig3.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14", height=380)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="insight-box">Key Insight: China and USA account for ~40% of global CO2. Gulf states lead per-capita rankings.</div>', unsafe_allow_html=True)

elif page == "Temperature Impact":
    st.markdown('<div class="section-title">Which Countries Contributed Most to Global Warming?</div>', unsafe_allow_html=True)
    latest = int(countries_df["year"].max())
    temp = countries_df[countries_df["year"]==latest][
        ["country","temperature_change_from_co2","temperature_change_from_ch4","temperature_change_from_n2o"]
    ].dropna(subset=["temperature_change_from_co2"]).sort_values("temperature_change_from_co2", ascending=False).head(20)
    fig = px.bar(temp.sort_values("temperature_change_from_co2"), x="temperature_change_from_co2", y="country",
        orientation="h", color="temperature_change_from_co2",
        color_continuous_scale=["#00c896","#ffc864","#ff4444"],
        title="Cumulative Temperature Contribution by Country (C)",
        labels={"temperature_change_from_co2":"C warming","country":""})
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e",
        height=560, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    top5 = temp.head(5)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="CO2",     x=top5["country"].tolist(), y=top5["temperature_change_from_co2"].tolist(), marker_color="#00c896"))
    fig2.add_trace(go.Bar(name="Methane", x=top5["country"].tolist(), y=top5["temperature_change_from_ch4"].tolist(), marker_color="#ffc864"))
    fig2.add_trace(go.Bar(name="N2O",     x=top5["country"].tolist(), y=top5["temperature_change_from_n2o"].tolist(), marker_color="#ff8c69"))
    fig2.update_layout(barmode="stack", title="Warming by Gas Type - Top 5 Countries",
        template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e", height=400)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="insight-box">Key Insight: The USA leads in cumulative warming contribution due to 100+ years of heavy industrial emissions.</div>', unsafe_allow_html=True)

elif page == "Energy Sources":
    st.markdown('<div class="section-title">CO2 by Energy Source (1900-2023)</div>', unsafe_allow_html=True)
    energy = world_df[world_df["year"]>=1900][["year","coal_co2","oil_co2","gas_co2","cement_co2","flaring_co2"]].dropna()
    fig = go.Figure()
    for col, label, color in [("coal_co2","Coal","#ff6b6b"),("oil_co2","Oil","#ffc864"),
                                ("gas_co2","Gas","#69c0ff"),("cement_co2","Cement","#b0b0b0"),
                                ("flaring_co2","Flaring","#ff9f43")]:
        fig.add_trace(go.Scatter(x=energy["year"].tolist(), y=energy[col].tolist(), mode="lines",
            stackgroup="one", name=label, line=dict(width=0.5, color=color), fillcolor=color))
    fig.update_layout(title="Global CO2 by Energy Source", template="plotly_dark",
        paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e", height=480,
        xaxis_title="Year", yaxis_title="CO2 (billion tonnes)", hovermode="x unified",
        legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig, use_container_width=True)
    options = sorted(countries_df["country"].unique().tolist())
    selected = st.multiselect("Compare countries", options, default=["China","United States","India","Germany","Brazil"])
    if selected:
        mix = countries_df[(countries_df["year"]==2022) & (countries_df["country"].isin(selected))]\
            [["country","coal_co2","oil_co2","gas_co2"]].dropna()
        fig2 = go.Figure()
        for src, color in [("coal_co2","#ff6b6b"),("oil_co2","#ffc864"),("gas_co2","#69c0ff")]:
            fig2.add_trace(go.Bar(name=src.replace("_co2","").capitalize(),
                x=mix["country"].tolist(), y=mix[src].tolist(), marker_color=color))
        fig2.update_layout(barmode="group", title="Coal / Oil / Gas Comparison (2022)",
            template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e", height=380)
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="insight-box">Key Insight: Coal remains the #1 source globally. The energy transition is deeply uneven across regions.</div>', unsafe_allow_html=True)

elif page == "Emissions vs GDP":
    st.markdown('<div class="section-title">CO2 Emissions vs Economic Output</div>', unsafe_allow_html=True)
    year_sel = st.slider("Select Year", 1990, 2022, 2022, 1)
    sc = countries_df[countries_df["year"]==year_sel][["country","gdp","co2","co2_per_capita","population","co2_per_gdp"]].dropna()
    sc = sc[sc["gdp"]>0].copy()
    sc["gdp_per_capita"] = sc["gdp"] / sc["population"]
    fig = px.scatter(sc, x="gdp_per_capita", y="co2_per_capita", size="population",
        color="co2_per_gdp", hover_name="country", size_max=60, log_x=True,
        color_continuous_scale="RdYlGn_r",
        title="CO2 Per Capita vs GDP Per Capita",
        labels={"gdp_per_capita":"GDP per Capita (USD)","co2_per_capita":"CO2 per Capita (t)","co2_per_gdp":"CO2 Intensity"})
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e", height=520)
    st.plotly_chart(fig, use_container_width=True)
    intensity = world_df[world_df["year"]>=1960][["year","co2_per_gdp"]].dropna()
    fig2 = px.line(intensity, x="year", y="co2_per_gdp",
        title="Global CO2 Intensity Declining Since 1980s",
        labels={"co2_per_gdp":"CO2 per unit GDP","year":"Year"},
        color_discrete_sequence=["#00c896"])
    fig2.update_traces(line_width=2.5)
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e", height=360)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="insight-box">Key Insight: Richer nations emit more per person. But globally CO2 intensity has been falling since the 1980s.</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#3a6b50;font-size:0.8rem;'>Built with Python | Streamlit | Plotly | Data: Our World in Data (CC BY 4.0) | 2025</div>", unsafe_allow_html=True)