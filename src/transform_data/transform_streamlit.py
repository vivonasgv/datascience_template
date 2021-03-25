"""Demo streamlit app script."""

import pandas as pd
import streamlit as st
import sys
from copy import deepcopy
import numpy as np


import plotly.express as px
import plotly.figure_factory as ff
import plotly.express as px

from app_utils import *

sys.path.append("../modules")



st.markdown(
f"""
<style>
  .reportview-container .main .block-container{{
      max-width: {1800}px;
      padding-top: {5}rem;
      padding-right: {1}rem;
      padding-left: {0}rem;
      padding-bottom: {10}rem;
  }}
</style>
""",
unsafe_allow_html=True,
)


df = load_presto_df()
st.markdown("## Feature Analysis")

feature_columns = list(df.columns)


st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
plot_mode = st.sidebar.radio("", ["Scatter Plot", "Histogram", "Histogram 2D", "Heatmap 2D", "Map"], 0)



if plot_mode == "Scatter Plot":
    interactive_scatter_plot(df)
      
if plot_mode == "Histogram":
    interactive_histogram1D(df)
    

if plot_mode == "Histogram 2D" :
    interactive_histogram2D(df)

if  plot_mode == "Heatmap 2D":
    interactive_heatmap2D(df)

