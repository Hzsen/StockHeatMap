# Heat_Map.py
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from data import holdings


def performance_to_color_scale(value):
    if value > 3:
        return 'darkgreen'  # more than 3%
    elif value > 1:
        return 'green'  # more than 1%
    elif value > 0:
        return 'lightgreen'  # less than 1%
    elif value > -1:
        return 'pink'  # decline less than 1%
    elif value > -3:
        return 'red'  # decline more than 1%
    else:
        return 'darkred'  # decline more than 3%


def register_heatmap_callbacks(app):
    @app.callback(
        Output('heatmap', 'figure'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_market_cap_heatmap(n_intervals):
        # Assuming your 'holdings' DataFrame has 'Daily Performance' column
        holdings['Color'] = holdings['Daily Performance'].apply(performance_to_color_scale)
        # Make sure 'holdings' DataFrame has 'Ticker', 'Market Value', 'Daily Performance' columns
        # Calculate the text for each treemap node
        holdings['Text'] = holdings.apply(
            lambda row: f"{row['Ticker']}<br>{row['Daily Performance']:.2f}%", axis=1
        )
        fig = go.Figure(go.Treemap(
            ids=holdings['Ticker'],
            labels=holdings['Ticker'],
            parents=[""] * len(holdings),  # No parents since it's a single level treemap
            values=holdings['Market Value'],
            textinfo="text",
            text=holdings['Text'],
            marker=dict(colors=holdings['Color'], line=dict(width=1))
        ))

        fig.update_layout(
            margin=dict(t=25, l=25, r=25, b=25)  # Adjust margins to fit
        )

        return fig


# Helper function to calculate frame sizes based on sector values
def calculate_frame_sizes(sector_values):
    total_value = sector_values.sum()
    sector_sizes = {sector: value / total_value for sector, value in sector_values.items()}
    return sector_sizes


def create_sector_based_heatmap(data):
    # Create a DataFrame for sectors with aggregated market values
    sector_data = data.groupby('Sector')['Market Value'].sum().reset_index()
    sector_data['id'] = sector_data['Sector']
    sector_data['parent'] = ""

    # Prepare the DataFrame for stocks with sector as parent
    stock_data = data.copy()
    stock_data['id'] = stock_data['Ticker']
    stock_data['parent'] = stock_data['Sector']

    # Concatenate the sector and stock data
    treemap_data = pd.concat([sector_data, stock_data], sort=False)

    # Create the treemap figure
    fig = go.Figure(go.Treemap(
        ids=treemap_data['id'],
        labels=treemap_data['Ticker'].fillna(treemap_data['Sector']),
        parents=treemap_data['parent'],
        values=treemap_data['Market Value'],
        marker=dict(colors=treemap_data['Color']),
        textinfo="label+value+percent entry",
        branchvalues='total'
    ))

    # Update layout
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig


def register_sector_sorted_heatmap_callback(app):
    @app.callback(
        Output('sector-sorted-heatmap', 'figure'),  # This updates the sector-sorted heatmap
        [Input('interval-component', 'n_intervals')]  # Triggers the update
    )
    def update_sector_sorted_heatmap(n_intervals):
        # Generate the sector-sorted heatmap figure
        # Assuming 'holdings' is the DataFrame with your stock data including sector information
        sector_sorted_heatmap_fig = create_sector_based_heatmap(holdings)

        # Return the figure to update the Graph component
        return sector_sorted_heatmap_fig
