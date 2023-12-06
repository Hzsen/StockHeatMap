# This file will contain functions related to the line graph visualization
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go


def register_line_graph_callbacks(app):
    @app.callback(
        Output('stock-graph', 'figure'),
        [Input('ticker-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_line_graph(selected_ticker, n_intervals):
        # Here you would call your data fetching function
        # For illustration, we're generating dummy data
        end_date = pd.to_datetime('today').normalize()
        start_date = end_date - pd.Timedelta(days=59)

        df = pd.DataFrame({
            'Time': pd.date_range(start=start_date, end=end_date, freq='D'),
            'Price': np.random.randn(60).cumsum()  # Replace with actual data
        })

        figure = {
            'data': [{
                'x': df['Time'],
                'y': df['Price'],
                'type': 'line',
                'name': selected_ticker
            }],
            'layout': {
                'title': f'Stock Data for {selected_ticker}',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Price'}
            }
        }

        return figure
