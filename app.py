# -*- coding: utf-8 -*-
import streamlit as st
import traceback

st.set_page_config(page_title="Climate Portfolio", page_icon="🌍", layout="wide")

try:
    import pandas as pd
    st.success("pandas OK")
except Exception as e:
    st.error(f"pandas FAILED: {e}")
    st.stop()

try:
    import plotly.express as px
    import plotly.graph_objects as go
    st.success("plotly OK")
except Exception as e:
    st.error(f"plotly FAILED: {e}")
    st.stop()

try:
    DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    df = pd.read_csv(DATA_URL)
    st.success(f"Data OK: {df.shape}")
except Exception as e:
    st.error(f"Data load FAILED: {e}")
    st.stop()

try:
    world_df = df[df["country"] == "World"].copy()
    trend = world_df[world_df["year"]>=1900][["year","co2"]].dropna()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trend["year"], y=trend["co2"], mode="lines", fill="tozeroy",
        line=dict(color="#00c896", width=2.5)))
    fig.update_layout(template="plotly_dark", height=400, title="Global CO2 Trend")
    st.plotly_chart(fig, use_container_width=True)
    st.success("Chart OK")
except Exception as e:
    st.error(f"Chart FAILED: {e}")
    st.code(traceback.format_exc())
    st.stop()

st.title("All tests passed! App is working.")