"""Demo streamlit app script."""

import pandas as pd
import streamlit as st
import sys
from copy import deepcopy
import numpy as np


import plotly.express as px
import plotly.figure_factory as ff
import plotly.express as px



@st.cache(allow_output_mutation=True)
def load_presto_df(query=""):
    url=f"https://github.com/avinashkz/income-prediction/raw/master/data/test.csv"
    
    columns = ["age",
    "workclass", 
    "fnlwgt", 
    "education", 
    "education_num", 
    "marital_status",
    "occupation",
    "relationship",
    "race", 
    "sex",
    "capital_gain",
    "capital_loss", 
    "hours_per_week", 
    "native_country",
    "income"]
    df = pd.read_csv(url)
    
    df.columns = columns
    
    df["income"] = df["income"].apply(lambda x: "gt 50k" if ">" in x else "lt 50k" )
    df = df.reset_index()

    
    return df

    
# Choose X, Y and Color Axis
def interactive_scatter_plot(df):
    global column2idx
    cols = st.beta_columns([1,3])
    with cols[0]:
      st.markdown("### Choose X Axis")
      x_col = st.selectbox("Choose Feature", df.columns, column2idx["age"])

      st.markdown("### Choose Y Axis ")
      y_col = st.selectbox("Choose Feature", df.columns, column2idx["fnlwgt"])

      st.markdown("### Choose Color")
      color_col = st.selectbox("Choose Feature",list(df.columns) + [None], column2idx["sex"])
      color_args = {"color": color_col} if color_col else {}
    
      st.markdown("### Select a Marker Size")
      marker_size = st.slider("Marker Size", 5,30, 15)
      df["marker_size"] = [marker_size]*len(df)
      

    with cols[1]:
      fig = px.scatter(df,x=x_col, y=y_col,size="marker_size", **color_args , size_max=marker_size)
      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)
    
# Choose X, Y and Color Axis
def interactive_box_plot(df):
    global column2idx
    cols = st.beta_columns([1,3])
    
    df = df.sample(frac=0.1)
    with cols[0]:
      st.markdown("### Choose X Axis")
      x_col = st.selectbox("Choose Feature", df.columns, column2idx["workclass"])

      st.markdown("### Choose Y Axis ")
      y_col = st.selectbox("Choose Feature", df.columns, column2idx["age"])

      st.markdown("### Choose Color")
      color_col = st.selectbox("Choose Feature",list(df.columns) + [None], column2idx["sex"])
      color_args = {"color": color_col} if color_col else {}
    
      if color_col:
        color_args = {"color": color_col}
        st.markdown("### Choose a Box Mode")
        boxmode = st.selectbox("Choose a Box Mode", ['group', 'overlay'], 0)
        boxmode_args = {"boxmode": boxmode}
      else:
        color_args = {}
        boxmode_args = {}
    

    with cols[1]:
      fig = px.box(df,x=x_col, y=y_col, **color_args , **boxmode_args )
      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)
    
    

def interactive_histogram1D(df):
    global column2idx
    cols = st.beta_columns([1,3])
    with cols[0]:
      st.markdown("### Choose Feature")
      x_col = st.selectbox("Choose Feature", df.columns, column2idx["age"])

      st.markdown("### Choose Color")
      color_col = st.selectbox("Choose Feature", list(df.columns) + [None], column2idx["sex"])
        
      if color_col:
        color_args = {"color": color_col}
        st.markdown("### Choose a Bar Mode")
        barmode = st.selectbox("Choose a Bar Mode", ['group', 'overlay','relative'], 1)
        barmode_args = {"barmode": barmode}
      else:
        color_args = {}
        barmode_args = {}
        
      st.markdown("### Enter a Tranformation")
      transform_string = st.text_input("Enter a Tranformation","x")
      transform_fn = eval(f"lambda x: {transform_string}")
      
      
    
      show_df = deepcopy(df)
      show_df[x_col] = show_df[x_col].apply(transform_fn)

    with cols[1]:

      fig = px.histogram(show_df, x=x_col, **color_args, **barmode_args )
      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)


def interactive_histogram2D(df):
    global column2idx
    # Choose X, Y and Color Axis

    cols = st.beta_columns([1,3])
    with cols[0]:
      st.markdown("### X-axis")
      x_col = st.selectbox("Choose X-Axis Feature", df.columns, column2idx["age"])
      nbinsx = st.slider("Number of Bins", 10,100, 10)

      st.markdown("### Y-axis")
      y_col = st.selectbox("Choose Y-Axis Feature", df.columns, column2idx["hours_per_week"])
      nbinsy = st.slider("Number of Bins (Y-Axis)", 10,100, 10)


    with cols[1]:

      fig = px.density_heatmap(df,
                               x=x_col,
                               y=y_col,
                               marginal_x="histogram",
                               marginal_y="histogram",
                               nbinsx=nbinsx,
                               nbinsy=nbinsy)

      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)

    
def interactive_heatmap2D(df):
    global column2idx
    # Choose X, Y and Color Axis
    cols = st.beta_columns([1, 3])
    with cols[0]:
      st.markdown("### X-axis")
      x_col = st.selectbox("Choose X-Axis Feature", df.columns, column2idx["age"])
      nbinsx = st.slider("Number of Bins", 10, 100, 20)

      st.markdown("### Y-axis")
      y_col = st.selectbox("Choose Y-Axis Feature", df.columns, column2idx["fnlwgt"])
      nbinsy = st.slider("Number of Bins (Y-Axis)", 10, 100, 20)

      st.markdown("### Z-axis")
      z_col = st.selectbox("Choose Z-Axis Feature", df.columns, column2idx["hours_per_week"])
      agg_func = st.selectbox("Aggregation Function", ["avg", "sum", "min", "sum", "count"], 0)

    with cols[1]:

      fig = px.density_heatmap(df,
                               x=x_col,
                               y=y_col,
                               z=z_col,
                               nbinsx=nbinsx,
                               nbinsy=nbinsy,
                               histfunc=agg_func)
      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)





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
column2idx = {col:i for i,col in enumerate(df.columns)}
st.markdown("# Feature Analysis")

feature_columns = list(df.columns)


st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.markdown("### Select a Plotting Mode")
plot_mode = st.radio("", ["Box Plot", "Scatter Plot", "Histogram", "Histogram 2D", "Heatmap 2D"], 0)


if plot_mode == "Box Plot":
    interactive_box_plot(df)

if plot_mode == "Scatter Plot":
    interactive_scatter_plot(df)

if plot_mode == "Histogram":
    interactive_histogram1D(df)


if plot_mode == "Histogram 2D" :
    interactive_histogram2D(df)

if  plot_mode == "Heatmap 2D":
    interactive_heatmap2D(df)
        