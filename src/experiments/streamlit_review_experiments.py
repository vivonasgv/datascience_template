# pylint: disable=W0105,W0201,C0303,W0611, redefined-outer-name, global-statement, line-too-long, eval-used
"""Demo streamlit app script."""

import datetime
import json
import sys

from copy import deepcopy
from glob import glob

import toniq
import pandas as pd
import streamlit as st
import numpy as np

import plotly.express as px
import plotly.figure_factory as ff



sys.path.append("../../modules")

#pylint: disable=unused-argument
@st.cache(allow_output_mutation=True)
def load_presto_df(query=""):
  """
  Load Presto Datafram (ATM we are mocking with returning a Pandas DataFrame)
  
  """
  url="https://github.com/avinashkz/income-prediction/raw/master/data/test.csv"

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
  
  #column2idx = {col:i for i, col in enumerate(df.columns)}
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
    marker_size = st.slider("Marker Size", 10,50, 20)
    df["marker_size"] = [marker_size]*len(df)


  with cols[1]:
    fig = px.scatter(df,x=x_col, y=y_col,size="marker_size", **color_args , size_max=marker_size)
    fig.update_layout(width=1000, height=800, font_size=20)
    st.plotly_chart(fig)

# Choose X, Y and Color Axis
def interactive_box_plot(df):
  """
  Interactive Box Plot
  
  params: 
    df: input data frame
    
  return:
    plots Box plot in streamlit
  
  """
    
  #column2idx = {col:i for i, col in enumerate(df.columns)}
  cols = st.beta_columns([1,3])

  df = df.sample(frac=0.1)
  with cols[0]:
    st.markdown("### Choose X Axis")
    x_col = st.selectbox("Choose Feature", df.columns, 0)

    st.markdown("### Choose Y Axis ")
    y_col = st.selectbox("Choose Feature", df.columns, 1)

    st.markdown("### Choose Color")
    color_col = st.selectbox("Choose Feature",[None] + list(df.columns), 0)
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
  
  """
  Interactive Histogram1D Plot
  
  params: 
    df: input data frame
    
  return:
    plots histogram1D plot in streamlit
  
  """
  

  #column2idx = {col:i for i, col in enumerate(df.columns)}
  
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

  #column2idx = {col:i for i, col in enumerate(df.columns)}
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

  #column2idx = {col:i for i, col in enumerate(df.columns)}
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




st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
# Load the Raw DF


PAGE_KEYS =  ["Experiment Evaluation", "Interactive Feature Analysis"]
st.sidebar.write("## Select a Page")
PAGE_KEY =  st.sidebar.selectbox("Select a Page", PAGE_KEYS, 0 )


# Initialize mlflow client
mlflow_client = toniq.MlflowClient()

# create a hash between the experiment name and experiment object
experiment_obj_list = mlflow_client.list_experiments()
experiment_name_list = list(map(lambda exp: exp.name, experiment_obj_list))
name2experiment = dict(zip(experiment_name_list, experiment_obj_list))


st.sidebar.write("## Select and Experiment")
exp_name = st.sidebar.selectbox("Select an Experiment", sorted(experiment_name_list), 2 )


experiment = mlflow_client.get_experiment_by_name(name=exp_name)

#Choose a Run ID

run_list = mlflow_client.search_runs(experiment_ids=experiment.experiment_id)

# sort out any runs with null metrics to avoid further issues when choosing an experiment
run_list = list(filter(lambda r: bool(r.data.metrics), run_list))


timestamp2date = lambda ts: datetime.datetime.fromtimestamp(ts // 1000)

run_df = {}
run_df["params"] = pd.DataFrame([{"run_id": r.info.run_id,
                                   "start_time": timestamp2date(r.info.start_time),
                                   "end_time": timestamp2date(r.info.end_time)
                                  , **r.data.params} for r in run_list]).set_index("run_id")
run_df["metrics"] = pd.DataFrame([{"run_id": r.info.run_id, 
                                   "start_time": timestamp2date(r.info.start_time),
                                   "end_time": timestamp2date(r.info.end_time)
                                   
                                   , **r.data.metrics} for r in run_list]).set_index("run_id")



for rdf_type, rdf in run_df.items():
  for col in rdf.columns:
    if "time" not in col:
      run_df[rdf_type][col] = pd.to_numeric(rdf[col])

# remove columns with nans to avoid issues with plotting

for rdf_type, rdf in run_df.items():
  run_df[rdf_type] = rdf[[k for k,v in dict(rdf.isna().sum()).items() if v == 0]]

metric_options = run_df["metrics"].columns


st.sidebar.write("## Select a Metric")
chosen_metric = st.sidebar.selectbox("Choose a Metric", metric_options, 5)

st.sidebar.write("## Sort Style")
acending_sort = st.sidebar.selectbox("Ascending or Descending", ["Ascending", "Descending"] , 0)  == "Ascending"

# get the best run
show_best_runs_df = run_df["metrics"][[chosen_metric]].sort_values(by=[chosen_metric], ascending=acending_sort )


# get best run id
best_run_id = run_df["metrics"].index[0]

# get best run object
best_run = mlflow_client.get_run(run_id=best_run_id)

def interactive_feature_analysis(df):
  """
  Interactive Feature Analaysis

  params: 
    df: input data frame

  returns:

    Chosen Interactive Feature Visualizer Chosen by the User in {plot_mode}

  """
  global best_run, best_run_id

  # list all of the paths from the best run
  artifact_paths = glob(best_run.info.artifact_uri.replace("file://", "")+"/*/*")

  # get a hash between the artifact name and the path
  artifact2path = {ap.split('/')[-2] : ap for ap in artifact_paths}
  run_predictions_df = pd.read_json(artifact2path["predictions"])


  num_classes = len(run_predictions_df.loc[0, "probability"])
  class_map = {0: "low-income", 1: "high-income", 2: "Null"}
  run_predictions_df[[ f"probability_{class_map[pl]}" for pl in range(num_classes)]] = pd.DataFrame(run_predictions_df.probability.tolist(), index= run_predictions_df.index)

  st.write()
  df = pd.concat([df, run_predictions_df], axis=1)            

  # pylint: disable=unused-variable
  with open(artifact2path["config"], "r") as f:
    run_config = json.load(f)

  st.markdown("## Feature Analysis")
  st.sidebar.markdown(f"#### Best Run ID: {best_run_id}")
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
        
def interactive_experiment_analysis(df):
  """
  Interactive Feature Analaysis
  
  params: 
    df: input data frame

  returns:
    Chosen Interactive Feature Visualizer Chosen by the User in {plot_mode}
  """

  st.markdown("## Experiment Analysis")

  cols = st.beta_columns([2,2])
  with cols[0]:
    st.write("#### Performance Over Time")
    fig = px.line(run_df["metrics"], x="end_time", y=chosen_metric)
    st.plotly_chart(fig)

  with cols[1]:
    st.write("#### Histogram of Performance")
    fig = px.histogram(run_df["metrics"], x=chosen_metric)
    st.plotly_chart(fig)

  st.markdown("#### Select a Plotting Mode")
  plot_mode = st.radio("", ["Scatter Plot", "Histogram", "Histogram 2D", "Heatmap 2D", "Box Plot"], 0)

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

def evaluate_experiment():
  """
  Evaluate Experiments from MLFLOW
  """
  global run_df, run_list

  # join metrics and params on run_id key
  st.sidebar.write("## Best Runs")
  st.sidebar.write(f"#### Best Run ID : {best_run_id}")
  st.sidebar.write(f"#### Number of Runs : {len(run_df)}")

  df = pd.concat([run_df["params"], run_df["metrics"]], axis=1)

  interactive_experiment_analysis(df)
    
df = load_presto_df()

PAGE_DICT = {
    "Experiment Evaluation": {"fn": evaluate_experiment, "kwargs": {}},
    "Interactive Feature Analysis": {"fn": interactive_feature_analysis, "kwargs": {"df":df}} }

PAGE = PAGE_DICT[PAGE_KEY]
# Run the Page
PAGE["fn"](**PAGE["kwargs"])
