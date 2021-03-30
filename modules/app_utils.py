"""Demo streamlit app script."""

# pylint: disable=W0105,W0201,C0303,W0611
from copy import deepcopy
import pandas as pd
import streamlit as st
import numpy as np


import plotly.express as px
import plotly.figure_factory as ff

#pylint: disable=W0613
@st.cache(allow_output_mutation=True)
def load_presto_df(query=""):
  """
  Load Presto Datafram (ATM we are mocking with returning a Pandas DataFrame)
  
  """
  
  url="https://github.com/avinashkz/income-prediction/raw/master/data/train.csv"

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
  """
  Interactive Scatter Plot
  
  params: 
    df: input data frame
    
  return:
    plots scatter plot in streamlit
  
  """
  
  cols = st.beta_columns([1,3])
  with cols[0]:
    st.markdown("### Choose X Axis")
    x_col = st.selectbox("Choose Feature", df.columns, 0)

    st.markdown("### Choose Y Axis ")
    y_col = st.selectbox("Choose Feature", df.columns, 1)

    st.markdown("### Choose Color")
    color_col = st.selectbox("Choose Feature",[None] + list(df.columns), 0)
    color_args = {"color": color_col} if color_col else {}

    st.markdown("### Select a Marker Size")
    marker_size = st.slider("Marker Size", 10,50, 2)
    df["marker_size"] = [marker_size]*len(df)


  with cols[1]:
    fig = px.scatter(df,x=x_col, y=y_col,size="marker_size", **color_args , size_max=marker_size)
    fig.update_layout(width=1000, height=800, font_size=20)
    st.plotly_chart(fig)
    
def interactive_histogram1D(df):
  """
  Interactive Histogram1D Plot
  
  params: 
    df: input data frame
    
  return:
    plots histogram plot in streamlit
  
  """
  
  cols = st.beta_columns([1,3])
  with cols[0]:
    st.markdown("### Choose Feature")
    x_col = st.selectbox("Choose Feature", df.columns, 0)

    st.markdown("### Choose Color")
    color_col = st.selectbox("Choose Feature",[None] + list(df.columns), 0)

    if color_col:
      color_args = {"color": color_col}
      st.markdown("### Choose a Bar Mode")
      barmode = st.selectbox("Choose a Bar Mode", ['group', 'overlay','relative'], 0)
      barmode_args = {"barmode": barmode}
    else:
      color_args = {}
      barmode_args = {}

    st.markdown("### Enter a Tranformation")
    transform_string = st.text_input("Enter a Tranformation","lambda x: x")
    
    #pylint: disable=W0123
    transform_fn = eval(transform_string)

    show_df = deepcopy(df)
    show_df[x_col] = show_df[x_col].apply(transform_fn)

  with cols[1]:

    fig = px.histogram(show_df, x=x_col, **color_args, **barmode_args )
    fig.update_layout(width=1000, height=800, font_size=20)
    st.plotly_chart(fig)


def interactive_histogram2D(df):
  
  """
  Interactive Histogram2D Plot
  
  params: 
    df: input data frame
    
  return:
    plots histogram2D plot in streamlit
  
  """
  
  # Choose X, Y and Color Axis

  cols = st.beta_columns([1,3])
  with cols[0]:
    st.markdown("### X-axis")
    x_col = st.selectbox("Choose X-Axis Feature", df.columns, 0)
    nbinsx = st.slider("Number of Bins", 10,100, 10)

    st.markdown("### Y-axis")
    y_col = st.selectbox("Choose Y-Axis Feature", df.columns, 0)
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
  
  """
  Interactive heatmap2D Plot
  
  params: 
    df: input data frame
    
  return:
    plots heatmap2D plot in streamlit
  """
  
  # Choose X, Y and Color Axis

  cols = st.beta_columns([1, 3])
  with cols[0]:
    st.markdown("### X-axis")
    x_col = st.selectbox("Choose X-Axis Feature", df.columns, 0)
    nbinsx = st.slider("Number of Bins", 10, 100, 10)

    st.markdown("### Y-axis")
    y_col = st.selectbox("Choose Y-Axis Feature", df.columns, 0)
    nbinsy = st.slider("Number of Bins (Y-Axis)", 10, 100, 10)

    st.markdown("### Z-axis")
    z_col = st.selectbox("Choose Z-Axis Feature", df.columns, 0)
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

def interactive_feature_analysis(df):
  
  """
  Interactive Feature Analaysis
  
  params: 
    df: input data frame
    
  returns:
  
    Chosen Interactive Feature Visualizer Chosen by the User in {plot_mode}
    
  """
  
  st.markdown("## Feature Analysis")

  st.sidebar.markdown("### Select a Plotting Mode")
  plot_mode = st.sidebar.radio("", ["Scatter Plot", "Histogram", "Histogram 2D", "Heatmap 2D"], 0)

  if plot_mode == "Scatter Plot":
    interactive_scatter_plot(df)

  if plot_mode == "Histogram":
    interactive_histogram1D(df)


  if plot_mode == "Histogram 2D" :
    interactive_histogram2D(df)

  if  plot_mode == "Heatmap 2D":
    interactive_heatmap2D(df)

def interactive_experiment_analysis(df):
  
  """
  Interactive Feature Analaysis
  
  params: 
    df: input data frame
    
  returns:
    Chosen Interactive Feature Visualizer Chosen by the User in {plot_mode}
  """
  st.markdown("## Experiment Analysis Ass")
  st.markdown("## Select a Plotting Mode")
  
  plot_mode = st.radio("", ["Scatter Plot", "Histogram", "Histogram 2D", "Heatmap 2D"], 0)

  if plot_mode == "Scatter Plot":
    interactive_scatter_plot(df)

  if plot_mode == "Histogram":
    interactive_histogram1D(df)
    
  if plot_mode == "Histogram 2D" :
    interactive_histogram2D(df)

  if  plot_mode == "Heatmap 2D":
    interactive_heatmap2D(df)
