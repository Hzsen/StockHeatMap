import yfinance as yf
import pandas as pd

# Example sector data with market capitalization (this would be obtained from your data source)
# Note: Replace 'FB' with 'META' for Meta Platforms.
sector_data = {
    'Technology': {'AAPL': 2250000, 'MSFT': 1800000, 'GOOGL': 1500000, 'META': 1000000, 'INTC': 500000},
    'Healthcare': {'JNJ': 2000000, 'PFE': 1500000, 'UNH': 1200000, 'MRK': 1000000, 'ABT': 800000},
    # ... additional sectors and companies
}

# A list to store each company's data
top_companies_list = []

for sector, companies in sector_data.items():
    top_companies = sorted(companies, key=companies.get, reverse=True)[:10]

    for symbol in top_companies:
        stock_data = yf.Ticker(symbol)

        # Try to get the most recent data for this stock
        try:
            hist_data = stock_data.history(period="1d")
            if not hist_data.empty:
                latest_close_price = hist_data['Close'].iloc[-1]

                # Create a DataFrame for this company's data
                company_data = pd.DataFrame({
                    'Symbol': [symbol],
                    'Sector': [sector],
                    'Market Cap': [companies[symbol]],
                    'Latest Close Price': [latest_close_price]
                })

                # Add the DataFrame to the list
                top_companies_list.append(company_data)
            else:
                print(f"No data found for {symbol}. The symbol may be delisted or incorrect.")
        except Exception as e:
            print(f"An error occurred for {symbol}: {e}")

# Concatenate all the company DataFrames into a single DataFrame
top_companies_data = pd.concat(top_companies_list, ignore_index=True)

# Now `top_companies_data` is ready for visualization
print(top_companies_data)
