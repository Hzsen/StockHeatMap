import yfinance as yf
import pandas as pd

# Load the holdings data
file_path = 'holdings-spy.csv' # Replace with your actual file path
holdings = pd.read_csv(file_path)

# Get the tickers from the holdings DataFrame
tickers = holdings['Ticker'].tolist()

# Download data for the last two days instead of one
data = yf.download(tickers, period="2d")['Close']

# Now check if we have two days of data to calculate the percentage change
print("Data from yfinance for percentage change calculation:")
print(data)

# Calculate the percentage change only if we have at least two rows of data
percentage_changes = {ticker: (data[ticker].iloc[-1] / data[ticker].iloc[-2] - 1) * 100 for ticker in tickers if len(data[ticker]) == 2}

# Convert the dictionary to a DataFrame
percentage_changes_df = pd.DataFrame(list(percentage_changes.items()), columns=['Ticker', 'Percentage Change'])

print("Percentage Changes:")
print(percentage_changes_df)

# Calculate market value using 'Shares Held' and the closing prices
# Here, we should ensure that the 'Shares Held' and 'Close' are not NaN or zero.
holdings['Market Value'] = holdings.apply(lambda row: row['Shares Held'] * data.get(row['Ticker'], pd.Series()).iloc[-1] if pd.notna(row['Shares Held']) and pd.notna(data.get(row['Ticker'], pd.Series()).iloc[-1]) else pd.NA, axis=1)

# Check for rows with NaN 'Market Value' and remove them
holdings.dropna(subset=['Market Value'], inplace=True)

print("Holdings with calculated Market Value:")
print(holdings[['Ticker', 'Market Value']])

# Now create the percentage change DataFrame
percentage_changes = {ticker: (data[ticker].iloc[-1] / data[ticker].iloc[-2] - 1) * 100 for ticker in tickers if len(data[ticker]) > 1}

# Convert the dictionary to a DataFrame
percentage_changes_df = pd.DataFrame(list(percentage_changes.items()), columns=['Ticker', 'Percentage Change'])

print("Percentage Changes:")
print(percentage_changes_df)