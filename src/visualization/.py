"""Demo streamlit app script."""

import pandas as pd
import streamlit as st

df = pd.read_csv("./data/raw/county.csv", index_col="COUNTY")

st.write("""
# Demo Module
Showcases a demo using streamlit and patients dataset
""")
st.bar_chart(df)
