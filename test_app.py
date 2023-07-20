import pytest
from dash import Dash, dcc, html, Input, Output, ctx
from dash._callback_context import context_value
from dash._utils import AttributeDict
from contextvars import copy_context  
import pandas as pd

# Import the names of callback functions you want to test
from data_visualizer2 import get_header_layout, get_line_graph_layout, update_line_chart_callback

# Create a Dash app instance for testing
app = Dash(__name__)

# Read the data from the CSV file for testing
test_df = pd.read_csv('required_data.csv')

# Convert the "date" column to datetime format
test_df['date'] = pd.to_datetime(test_df['date'])

# Define the test layout of the app
app.layout = html.Div([
    get_header_layout(),
    get_line_graph_layout()
])

# Test Presence of Header
def test_header_presence():
    header_layout = get_header_layout()
    assert header_layout is not None
    assert 'Pink Morsel Sales(by region) visualizer' in str(header_layout)

def test_update_line_chart_callback():
    # Test with a specific selected_region value for test_df
    selected_region = test_df['region'].unique()[0]

    # Call the update_line_chart_callback with the test_df
    output = update_line_chart_callback(selected_region)

    # Check if the output is a tuple with two elements (figure, comparison_result)
    assert isinstance(output, tuple)
    assert len(output) == 2

    # Check if figure and comparison_result are not None
    assert output[0] is not None
    assert output[1] is not None

def test_display_callback():
    # Function to run the callback
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "radio-button.n_clicks"}]}))
        return update_line_chart_callback(1)

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output is not None

# Note: Replace 'app' with the actual name of your Dash app module.
