import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Climate Data Analyst Portfolio",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #0b1a14; }
  .hero-title {
    font-size: 3rem; font-weight: 800; color: #00c896;
    text-align: center; margin-bottom: 0.2rem;
  }
  .hero-sub {
    font-size: 1.15rem; color: #a0c8b0; text-align: center; margin-bottom: 2rem;
  }
  .metric-card {
    background: #112a1e; border: 1px solid #1e4d35;
    border-radius: 12px; padding: 1.2rem 1.5rem; text-align: center;
  }
  .metric-card .val { font-size: 2rem; font-weight: 700; color: #00c896; }
  .metric-card .lab { font-size: 0.82rem; color: #6fa888; margin-top: 4px; }
  .section-title {
    font-size: 1.5rem; font-weight: 700; color: #e8f5ee;
    border-left: 4px solid #00c896; padding-left: 12px; margin: 2rem 0 1rem;
  }
  .insight-box {
    background: #112a1e; border-left: 3px solid #00c896;
    border-radius: 8px; padding: 1rem 1.2rem; margin-top: 1rem;
    color: #a0c8b0; font-size: 0.92rem; line-height: 1.6;
  }
  .badge {
    display:inline-block; background:#1e4d35; color:#00c896;
    border-radius:6px; padding:2px 10px; font-size:0.78rem;
    margin:2px; font-weight:600;
  }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ───────────────────────────────────────────────────────────────
DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

df = load_data()

# Exclude aggregated regions, keep only real countries
EXCLUDE = ["World","Asia","Europe","Africa","North America","South America",
           "Oceania","European Union (27)","High-income countries",
           "Low-income countries","Middle East (GCP)","Upper-middle-income countries",
           "Lower-middle-income countries","Asia (excl. China and India)",
           "Europe (excl. EU-27)","Europe (excl. EU-28)",
           "North America (excl. USA)"]
countries_df = df[~df["country"].isin(EXCLUDE)]
world_df     = df[df["country"] == "World"]

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Navigation")
    page = st.radio("", [
        "🏠 About Me",
        "📈 Global CO₂ Trend",
        "🏆 Top Emitters",
        "🌡️ Temperature Impact",
        "⚡ Energy Source Breakdown",
        "💰 Emissions vs GDP"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 🛠️ Skills")
    skills = ["Python","Pandas","Plotly","Streamlit","Data Viz","Climate Analysis","SQL","Statistics"]
    for s in skills:
        st.markdown(f'<span class="badge">{s}</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📦 Dataset")
    st.markdown("**Our World in Data** — CO₂ & GHG Emissions")
    st.caption(f"50,411 rows · 79 columns · 1750–2024")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1 — About Me
# ═══════════════════════════════════════════════════════════════════════════
if page == "🏠 About Me":
    st.markdown('<div class="hero-title">🌍 Climate Data Analyst Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Turning climate data into actionable insights — one chart at a time</div>', unsafe_allow_html=True)

    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="val">37.4B</div><div class="lab">Tonnes CO₂ emitted in 2023</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="val">+1.45°C</div><div class="lab">Global warming above pre-industrial</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="val">254</div><div class="lab">Countries in this dataset</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="val">274 yrs</div><div class="lab">Data coverage (1750–2024)</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.markdown('<div class="section-title">👤 About This Portfolio</div>', unsafe_allow_html=True)
        st.markdown("""
        This portfolio showcases **5 deep-dive analyses** of global CO₂ and greenhouse gas emissions
        using the **Our World in Data** dataset — one of the most comprehensive open climate datasets available.

        Each project answers a real-world climate question:
        - 📈 How fast is CO₂ rising globally?
        - 🏆 Which countries are the biggest emitters?
        - 🌡️ Which nations have contributed most to warming?
        - ⚡ How is our energy mix shifting?
        - 💰 Do richer countries emit more per person?
        """)

    with col_b:
        st.markdown('<div class="section-title">🔬 Projects</div>', unsafe_allow_html=True)
        projects = [
            ("📈", "Global CO₂ Trend 1900–2024", "Time series analysis"),
            ("🏆", "Top 10 Emitters", "Comparative analysis"),
            ("🌡️", "Temperature Impact by Country", "Attribution analysis"),
            ("⚡", "Energy Source Breakdown", "Structural analysis"),
            ("💰", "Emissions vs GDP", "Correlation analysis"),
        ]
        for icon, title, tag in projects:
            st.markdown(f"**{icon} {title}** — *{tag}*")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2 — Global CO₂ Trend
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📈 Global CO₂ Trend":
    st.markdown('<div class="section-title">📈 Global CO₂ Emissions Trend (1900–2024)</div>', unsafe_allow_html=True)
    st.caption("Source: Our World in Data | Unit: Billion tonnes CO₂")

    trend = world_df[world_df["year"] >= 1900][["year","co2"]].dropna()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend["year"], y=trend["co2"],
        mode="lines", fill="tozeroy",
        line=dict(color="#00c896", width=2.5),
        fillcolor="rgba(0,200,150,0.15)",
        name="World CO₂"
    ))

    # Key events
    events = {
        1929: "Great Depression",
        1945: "WWII End",
        1973: "Oil Crisis",
        2008: "Financial Crisis",
        2020: "COVID-19"
    }
    for yr, label in events.items():
        yr_val = trend[trend["year"] == yr]["co2"]
        if not yr_val.empty:
            fig.add_vline(x=yr, line_dash="dash", line_color="rgba(255,200,100,0.5)", line_width=1)
            fig.add_annotation(x=yr, y=yr_val.values[0]+1.5,
                text=label, showarrow=False,
                font=dict(size=9, color="#ffc864"), textangle=-90)

    fig.update_layout(
        template="plotly_dark", paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e",
        height=480, margin=dict(l=10,r=10,t=30,b=10),
        xaxis_title="Year", yaxis_title="CO₂ (billion tonnes)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>Key Insight:</strong> Global CO₂ emissions have risen <strong>over 20× since 1900</strong>, from ~2 billion to ~37 billion tonnes. Notice the brief dips during economic crises — but emissions always rebounded stronger. The COVID-19 drop in 2020 was the largest single-year decline ever recorded (-5.4%), yet 2021 saw an immediate record recovery.</div>', unsafe_allow_html=True)

    # Growth rate
    st.markdown('<div class="section-title">📊 Year-on-Year CO₂ Growth Rate</div>', unsafe_allow_html=True)
    growth = world_df[world_df["year"] >= 1960][["year","co2_growth_prct"]].dropna()
    fig2 = px.bar(growth, x="year", y="co2_growth_prct",
        color="co2_growth_prct",
        color_continuous_scale=["#00c896","#ffc864","#ff6b6b"],
        labels={"co2_growth_prct":"Growth %", "year":"Year"})
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14",
        plot_bgcolor="#112a1e", height=320, margin=dict(l=10,r=10,t=10,b=10),
        coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 — Top Emitters
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🏆 Top Emitters":
    st.markdown('<div class="section-title">🏆 Top CO₂ Emitters — Country Comparison</div>', unsafe_allow_html=True)

    year_sel = st.slider("Select Year", 1990, 2023, 2023, 1)

    year_data = countries_df[countries_df["year"] == year_sel][
        ["country","co2","co2_per_capita","share_global_co2"]
    ].dropna(subset=["co2"]).sort_values("co2", ascending=False).head(15)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Total CO₂ Emissions (billion tonnes)**")
        fig = px.bar(year_data.sort_values("co2"),
            x="co2", y="country", orientation="h",
            color="co2", color_continuous_scale="Greens",
            labels={"co2":"CO₂ (bt)", "country":""})
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14",
            plot_bgcolor="#112a1e", height=480,
            margin=dict(l=0,r=10,t=10,b=10), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**CO₂ Per Capita (tonnes per person)**")
        per_cap = countries_df[countries_df["year"] == year_sel][
            ["country","co2_per_capita"]
        ].dropna().sort_values("co2_per_capita", ascending=False).head(15)
        fig2 = px.bar(per_cap.sort_values("co2_per_capita"),
            x="co2_per_capita", y="country", orientation="h",
            color="co2_per_capita", color_continuous_scale="Oranges",
            labels={"co2_per_capita":"CO₂ per capita (t)", "country":""})
        fig2.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14",
            plot_bgcolor="#112a1e", height=480,
            margin=dict(l=0,r=10,t=10,b=10), coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Global share pie
    st.markdown('<div class="section-title">🌐 Global CO₂ Share — Top 8 Countries</div>', unsafe_allow_html=True)
    top8 = year_data.head(8).copy()
    others = pd.DataFrame([{"country":"Rest of World",
                             "share_global_co2": 100 - top8["share_global_co2"].sum()}])
    pie_df = pd.concat([top8[["country","share_global_co2"]], others], ignore_index=True)

    fig3 = px.pie(pie_df, values="share_global_co2", names="country",
        color_discrete_sequence=px.colors.sequential.Greens_r,
        hole=0.45)
    fig3.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14",
        height=380, margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>Key Insight:</strong> China & USA alone account for ~40% of global emissions by total volume — yet per capita, Gulf states (Qatar, UAE, Kuwait) often rank #1. This distinction matters enormously for climate policy: a country can be a "small emitter" by total but a top polluter per person.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 4 — Temperature Impact
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🌡️ Temperature Impact":
    st.markdown('<div class="section-title">🌡️ Which Countries Contributed Most to Global Warming?</div>', unsafe_allow_html=True)
    st.caption("Metric: temperature_change_from_co2 — cumulative warming contribution in °C")

    latest_year = countries_df["year"].max()
    temp_data = countries_df[countries_df["year"] == latest_year][
        ["country","temperature_change_from_co2","temperature_change_from_ghg",
         "temperature_change_from_ch4","temperature_change_from_n2o"]
    ].dropna(subset=["temperature_change_from_co2"]).sort_values(
        "temperature_change_from_co2", ascending=False).head(20)

    fig = px.bar(temp_data.sort_values("temperature_change_from_co2"),
        x="temperature_change_from_co2", y="country", orientation="h",
        color="temperature_change_from_co2",
        color_continuous_scale=["#00c896","#ffc864","#ff4444"],
        labels={"temperature_change_from_co2":"°C warming contribution","country":""})
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14",
        plot_bgcolor="#112a1e", height=560,
        margin=dict(l=0,r=10,t=10,b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    # GHG breakdown for top 5
    st.markdown('<div class="section-title">🔬 GHG Breakdown — Top 5 Countries</div>', unsafe_allow_html=True)
    top5 = temp_data.head(5)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="CO₂", x=top5["country"], y=top5["temperature_change_from_co2"], marker_color="#00c896"))
    fig2.add_trace(go.Bar(name="CH₄ (Methane)", x=top5["country"], y=top5["temperature_change_from_ch4"], marker_color="#ffc864"))
    fig2.add_trace(go.Bar(name="N₂O", x=top5["country"], y=top5["temperature_change_from_n2o"], marker_color="#ff8c69"))
    fig2.update_layout(barmode="stack", template="plotly_dark",
        paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e",
        height=360, margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>Key Insight:</strong> The USA has contributed more to cumulative global warming than any other single country — a result of over a century of industrial emissions. China, despite being the top emitter today, has a shorter industrial history. This "historical responsibility" framing is central to climate justice debates.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 5 — Energy Source Breakdown
# ═══════════════════════════════════════════════════════════════════════════
elif page == "⚡ Energy Source Breakdown":
    st.markdown('<div class="section-title">⚡ Global CO₂ by Energy Source (1900–2023)</div>', unsafe_allow_html=True)

    energy = world_df[world_df["year"] >= 1900][
        ["year","coal_co2","oil_co2","gas_co2","cement_co2","flaring_co2"]
    ].dropna()

    fig = go.Figure()
    colors = {"coal_co2":"#ff6b6b","oil_co2":"#ffc864","gas_co2":"#69c0ff",
              "cement_co2":"#b0b0b0","flaring_co2":"#ff9f43"}
    labels = {"coal_co2":"Coal","oil_co2":"Oil","gas_co2":"Gas",
              "cement_co2":"Cement","flaring_co2":"Flaring"}

    for col, color in colors.items():
        fig.add_trace(go.Scatter(
            x=energy["year"], y=energy[col],
            mode="lines", stackgroup="one",
            name=labels[col], line=dict(color=color, width=0.5),
            fillcolor=color.replace(")", ",0.7)").replace("rgb","rgba") if "rgb" in color else color
        ))

    fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14",
        plot_bgcolor="#112a1e", height=480,
        margin=dict(l=10,r=10,t=20,b=10),
        xaxis_title="Year", yaxis_title="CO₂ (billion tonnes)",
        hovermode="x unified", legend=dict(orientation="h", y=-0.12))
    st.plotly_chart(fig, use_container_width=True)

    # Country comparison — energy mix
    st.markdown('<div class="section-title">🌏 Country Energy Mix Comparison (2022)</div>', unsafe_allow_html=True)
    compare_countries = st.multiselect(
        "Select countries to compare",
        options=sorted(countries_df["country"].unique().tolist()),
        default=["China","United States","India","Germany","Brazil"]
    )

    if compare_countries:
        mix = countries_df[
            (countries_df["year"] == 2022) &
            (countries_df["country"].isin(compare_countries))
        ][["country","coal_co2","oil_co2","gas_co2"]].dropna()

        fig2 = go.Figure()
        for source, color in [("coal_co2","#ff6b6b"),("oil_co2","#ffc864"),("gas_co2","#69c0ff")]:
            fig2.add_trace(go.Bar(
                name=source.replace("_co2","").capitalize(),
                x=mix["country"], y=mix[source], marker_color=color
            ))
        fig2.update_layout(barmode="group", template="plotly_dark",
            paper_bgcolor="#0b1a14", plot_bgcolor="#112a1e",
            height=380, margin=dict(l=10,r=10,t=20,b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>Key Insight:</strong> Coal remains the #1 source of energy-related CO₂ globally. While Europe and the USA have cut coal dramatically, Asia — particularly China and India — still relies heavily on it. The energy transition story is deeply uneven across regions.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 6 — Emissions vs GDP
# ═══════════════════════════════════════════════════════════════════════════
elif page == "💰 Emissions vs GDP":
    st.markdown('<div class="section-title">💰 CO₂ Emissions vs. Economic Output</div>', unsafe_allow_html=True)
    st.caption("Do richer countries emit more? Exploring the relationship between GDP and CO₂.")

    year_sel = st.slider("Select Year", 1990, 2022, 2022, 1)

    scatter_df = countries_df[countries_df["year"] == year_sel][
        ["country","gdp","co2","co2_per_capita","population","co2_per_gdp"]
    ].dropna()
    scatter_df = scatter_df[scatter_df["gdp"] > 0]
    scatter_df["gdp_per_capita"] = scatter_df["gdp"] / scatter_df["population"]

    fig = px.scatter(
        scatter_df,
        x="gdp_per_capita", y="co2_per_capita",
        size="population", color="co2_per_gdp",
        hover_name="country",
        size_max=60,
        color_continuous_scale="RdYlGn_r",
        labels={
            "gdp_per_capita":"GDP per Capita (USD)",
            "co2_per_capita":"CO₂ per Capita (tonnes)",
            "co2_per_gdp":"CO₂ intensity",
            "population":"Population"
        },
        log_x=True
    )
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14",
        plot_bgcolor="#112a1e", height=520,
        margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)

    # CO₂ intensity over time
    st.markdown('<div class="section-title">📉 CO₂ Intensity Declining Over Time (World)</div>', unsafe_allow_html=True)
    intensity = world_df[world_df["year"] >= 1960][["year","co2_per_gdp"]].dropna()
    fig2 = px.line(intensity, x="year", y="co2_per_gdp",
        labels={"co2_per_gdp":"CO₂ per unit GDP","year":"Year"},
        color_discrete_sequence=["#00c896"])
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0b1a14",
        plot_bgcolor="#112a1e", height=320, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>Key Insight:</strong> Richer nations tend to emit more per person — but the most carbon-<em>intensive</em> economies (CO₂ per $ of GDP) are often middle-income fossil-fuel exporters. Globally, CO₂ intensity has been falling since the 1980s — meaning the world economy is becoming more carbon-efficient, but not fast enough to offset growth.</div>', unsafe_allow_html=True)


# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#3a6b50;font-size:0.8rem;'>"
    "Built with 🐍 Python · Streamlit · Plotly &nbsp;|&nbsp; "
    "Data: Our World in Data (CC BY 4.0) &nbsp;|&nbsp; "
    "Climate Data Analyst Portfolio 2025"
    "</div>",
    unsafe_allow_html=True
)
