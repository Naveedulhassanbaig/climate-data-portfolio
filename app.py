# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Climate Portfolio", page_icon="🌍", layout="wide")

st.title("Climate Data Analyst Portfolio")
st.markdown("Loading data...")

DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_URL)
        return df
    except Exception as e:
        st.error(f"Data load error: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Could not load data.")
    st.stop()

st.success(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
st.write(df.head(3))