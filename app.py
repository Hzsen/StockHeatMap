# This file will serve as the entry point to your Dash application, bringing together the components from other files
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from data import tickers, holdings
from Line_Graph import register_line_graph_callbacks
from Heat_Map import register_heatmap_callbacks, register_sector_sorted_heatmap_callback


# This function should be defined in your data.py file
def scale_market_cap_to_size(market_caps, min_size=100, max_size=500):
    # Scale market cap values to a size value for visualization
    min_cap, max_cap = min(market_caps), max(market_caps)
    cap_range = max_cap - min_cap
    size_range = max_size - min_size
    scaled_sizes = min_size + (market_caps - min_cap) / cap_range * size_range
    return scaled_sizes


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Heatmap to display the data in a two-dimensional grid
    html.H1('Stock Data Heatmap'),
    dcc.Graph(id='heatmap'),  # Make sure this ID matches the one in your callback
    dcc.Graph(id='sector-sorted-heatmap'),  # This will display the sector-sorted heatmap
    # Interval component for updating the graph regularly
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # in milliseconds (1 minute)
        n_intervals=0
    ),


    html.H2('Real-Time Stock Data Visualization'),

    # Dropdown to select the ticker, now getting options from data.py
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        value=tickers[0]  # Default value is the first ticker in the list
    ),

    # Graph to display the stock data
    dcc.Graph(id='stock-graph')
])

# Register callbacks for line graph and heatmap components
register_heatmap_callbacks(app)
register_line_graph_callbacks(app)
# Register the new sector-sorted heatmap callback
register_sector_sorted_heatmap_callback(app)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
