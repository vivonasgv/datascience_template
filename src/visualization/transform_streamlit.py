"""Demo streamlit app script."""

import pandas as pd
import streamlit as st


import plotly.express as px
import plotly.figure_factory as ff
import plotly.express as px

sys.path.append("../modules")
from module import ToniqEnvManager

# set up the Toniq Env Manger
tem = ToniqEnvManger(provider='gcp')


@st.cache(allow_output_mutation=True)
def load_presto_df(query):
    global tem
    return pd.read_sql_query(query, tem.conn)



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


st.markdown("## Feature Analysis")

feature_columns = list(feature_store.columns)

plot_mode = st.radio("", ["Scatter Plot", "Histogram", "Histogram 2D", "Heatmap 2D", "Map"], 0)

sampled_feature_store = load_presto_df(q)



if plot_mode == "Scatter Plot":
    # Choose X, Y and Color Axis

    cols = st.beta_columns([1,3])
    with cols[0]:
      st.markdown("### Choose X Axis")
      x_col = st.selectbox("Choose Feature", feature_store.columns, 0)

      st.markdown("### Choose Y Axis ")
      y_col = st.selectbox("Choose Feature", feature_store.columns, 1)

      st.markdown("### Choose Color")
      color_col = st.selectbox("Choose Feature",[None] + list(feature_store.columns), 0)
      color_args = {"color": color_col} if color_col else {}

    with cols[1]:
      fig = px.scatter(sampled_feature_store,x=x_col, y=y_col, **color_args )
      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)
    
if plot_mode == "Histogram":
    # Choose X, Y and Color Axis

    cols = st.beta_columns([1,3])
    with cols[0]:
      st.markdown("### Choose Feature")
      x_col = st.selectbox("Choose Feature", feature_store.columns, 0)

      st.markdown("### Choose Color")
      color_col = st.selectbox("Choose Feature",[None] + list(feature_store.columns), 0)
      color_args = {"color": color_col} if color_col else {}

    with cols[1]:

      fig = px.histogram(sampled_feature_store,x=x_col, **color_args )
      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)


if plot_mode == "Histogram 2D" :
    # Choose X, Y and Color Axis

    cols = st.beta_columns([1,3])
    with cols[0]:
      st.markdown("### X-axis")
      x_col = st.selectbox("Choose X-Axis Feature", feature_store.columns, 0)
      nbinsx = st.slider("Number of Bins", 10,100, 10)

      st.markdown("### Y-axis")
      y_col = st.selectbox("Choose Y-Axis Feature", feature_store.columns, 0)
      nbinsy = st.slider("Number of Bins (Y-Axis)", 10,100, 10)


      if "3D" in plot_mode:
        st.markdown("### Z-axis")
        x_col = st.selectbox("Choose Z-Axis Feature", feature_store.columns, 0)
        nbinsx = st.selectbox("Aggregation Function", 10, 100, 10)


    with cols[1]:

      fig = px.density_heatmap(sampled_feature_store,
                               x=x_col,
                               y=y_col,
                               marginal_x="histogram",
                               marginal_y="histogram",
                               nbinsx=nbinsx,
                               nbinsy=nbinsy)

      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)

if  plot_mode == "Heatmap 2D":
    # Choose X, Y and Color Axis

    cols = st.beta_columns([1, 3])
    with cols[0]:
      st.markdown("### X-axis")
      x_col = st.selectbox("Choose X-Axis Feature", feature_store.columns, 0)
      nbinsx = st.slider("Number of Bins", 10, 100, 10)

      st.markdown("### Y-axis")
      y_col = st.selectbox("Choose Y-Axis Feature", feature_store.columns, 0)
      nbinsy = st.slider("Number of Bins (Y-Axis)", 10, 100, 10)

      st.markdown("### Z-axis")
      z_col = st.selectbox("Choose Z-Axis Feature", feature_store.columns, 0)
      agg_func = st.selectbox("Aggregation Function", ["avg", "sum", "min", "sum", "count"], 0)

    with cols[1]:

      fig = px.density_heatmap(sampled_feature_store,
                               x=x_col,
                               y=y_col,
                               z=z_col,
                               nbinsx=nbinsx,
                               nbinsy=nbinsy,
                               histfunc=agg_func)
      fig.update_layout(width=1000, height=800, font_size=20)
      st.plotly_chart(fig)


if plot_mode == "Map":

    cols = st.beta_columns([1, 3])
    with cols[0]:
      st.markdown("### Z-axis")
      color_col = st.selectbox("Choose Color Feature", [None]+list(feature_store.columns), 0)
      nx_hexagon = st.slider("Number of Hexagons (Horizontal)", 5, 20, 10)
      #agg_func = st.selectbox("Aggregation Function", ["avg", "sum", "min", "sum", "count"], 0)

    with cols[1]:
      tmp_feature_store = deepcopy(feature_store)
      tmp_feature_store["date"] = tmp_feature_store["date"].dt.strftime("%Y/%m/%d")
      fig = ff.create_hexbin_mapbox(tmp_feature_store,
                      lat="lat", lon="long",
                      color= color_col,
                      agg_func= np.mean,
                      nx_hexagon=nx_hexagon,
                      animation_frame="date",
                      color_continuous_scale="Cividis", labels={"frame": "date"},
                      opacity=0.5,
                      show_original_data=False, original_data_marker=dict(opacity=0.6, size=4, color="deeppink")
      )

      fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))
      fig.layout.sliders[0].pad.t = 20
      fig.layout.updatemenus[0].pad.t = 40
      fig.update_layout(mapbox_style="open-street-map")

      st.plotly_chart(fig)


