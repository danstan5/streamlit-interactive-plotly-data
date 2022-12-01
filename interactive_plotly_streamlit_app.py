from typing import List

import plotly.express as px
from plotly.graph_objects import Figure

import streamlit as st
from streamlit_plotly_events import plotly_events


def selected_indexes(
    selected_points: List[dict],
    ploty_figure: Figure
) -> List[int]:
    """Selected datapoints indexes to filter dataframe.
    
    Args:
        selected_points: list of dictonaries containing point details.
            Point data comes from the javascript [event data components]
            (https://plotly.com/javascript/plotlyjs-events/#event-data).
            This is accessed via the [streamlit-plotly-events]
            (https://pypi.org/project/streamlit-plotly-events/) package.
        ploty_figure: 
            The plotly figure the data is referenced to.
            Note: this is currently only tested for scatter plot types.

    Returns:
        List of dataframe indexes that have been selected on the plot.
        These can then be filtered against on the dataframe using `.loc` method.

    """
    plotly_data = [(s['curveNumber'], s['pointIndex']) for s in selected_points]
    return [ploty_figure.data[g]['customdata'][i][0] for g, i in plotly_data]


df = px.data.iris()  # loads the demonstrate iris dataset as a dataframe

st.markdown('#### Plotly graph 📊')
fig = px.scatter(
    df, x="sepal_width", y="sepal_length", color="species", size='petal_length',
    hover_data=[df.index.values]
)

selected_points = plotly_events(fig, key='plot', select_event=True)
df_indexes = selected_indexes(selected_points, fig)

if df_indexes:
    st.markdown('#### Selected datapoints 👉')
    selected_df = df.loc[df_indexes]
    st.dataframe(selected_df)
