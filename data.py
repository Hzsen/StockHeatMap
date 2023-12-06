import yfinance as yf
import pandas as pd
import numpy as np

# Load the holdings data
file_path = 'holdings-spy.csv'  # Replace with your actual file path
holdings = pd.read_csv(file_path)

# Get the tickers from the holdings DataFrame
tickers = holdings['Ticker'].tolist()


# Fetch sector information for each ticker using yfinance
# We use the 'info' attribute to fetch various metadata including the sector
def fetch_sector(ticker):
    stock = yf.Ticker(ticker)
    return stock.info.get('sector')


# This way, we're not querying Yahoo Finance one ticker at a time in a loop
holdings['Sector'] = holdings['Ticker'].apply(fetch_sector)

# Download data for the last two days
data = yf.download(tickers, period="2d")['Close']

# Calculate the percentage change only if we have at least two rows of data
percentage_changes = {
    ticker: (data[ticker].iloc[-1] / data[ticker].iloc[-2] - 1) * 100
    for ticker in tickers if len(data[ticker]) == 2
}
# Check if we have at least two rows of data to calculate the percentage change
if len(data.index) > 1:
    # Calculate the percentage change for the last available day
    daily_performance = data.pct_change().iloc[-1] * 100
    # Add the 'Daily Performance' to the 'holdings' DataFrame
    holdings['Daily Performance'] = holdings['Ticker'].map(daily_performance)
else:
    print("Not enough data to calculate daily performance.")
# Convert the dictionary to a DataFrame
percentage_changes_df = pd.DataFrame(list(percentage_changes.items()), columns=['Ticker', 'Percentage Change'])

# Calculate market value using 'Shares Held' and the closing prices
# Ensure that 'Shares Held' and 'Close' are not NaN or zero
holdings['Market Value'] = holdings.apply(
    lambda row: row['Shares Held'] * data.get(row['Ticker'], pd.Series()).iloc[-1]
    if pd.notna(row['Shares Held']) and pd.notna(data.get(row['Ticker'], pd.Series()).iloc[-1])
    else pd.NA,
    axis=1
)

# Check for rows with NaN 'Market Value' and remove them
holdings.dropna(subset=['Market Value'], inplace=True)

# Calculate total market value
total_market_value = holdings['Market Value'].sum()

# Normalize the widths to a scale of 1 for simplicity
holdings['Normalized Width'] = holdings['Market Value'] / total_market_value

# The 'holdings' DataFrame now contains the market values and the normalized widths
# Save this DataFrame to a CSV file for the next step
normalized_file_path = 'normalized_holdings.csv'  # Replace with your desired file path
holdings.to_csv(normalized_file_path, index=False)

# Output the data to the console
# print("Normalized Holdings Data:")
# print(holdings[['Ticker', 'Shares Held', 'Market Value', 'Normalized Width']])


# This function will be used to create a heatmap data structure
def get_heatmap_data(num_days=60):
    # Start date is 'num_days' ago from the most recent data point in 'data'
    start_date = data.index.max() - pd.Timedelta(days=num_days - 1)

    # Filter the holdings DataFrame for the required date range
    date_range = pd.date_range(start=start_date, periods=num_days, freq='D')
    heatmap_data = pd.DataFrame(index=date_range, columns=tickers)

    # Fill the DataFrame with the percentage change data
    for ticker in tickers:
        # Fetch historical data for each ticker without printing progress
        ticker_data = yf.download(ticker, start=start_date, end=data.index.max(), progress=False)['Close']
        # Calculate daily percentage changes
        ticker_changes = ticker_data.pct_change().iloc[1:] * 100  # Exclude the first NaN value
        # Assign the data to the corresponding column in the heatmap DataFrame
        heatmap_data[ticker] = ticker_changes

    # Multiply each column by its normalized width to reflect market cap size in the heatmap
    for ticker in tickers:
        normalized_width = holdings.loc[holdings['Ticker'] == ticker, 'Normalized Width'].values[0]
        heatmap_data[ticker] *= normalized_width

    # Drop any NaN values to clean up the DataFrame
    heatmap_data.dropna(axis=1, how='all', inplace=True)

    return heatmap_data


# Generate the heatmap data
heatmap_data = get_heatmap_data()
