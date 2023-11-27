import requests
import pandas as pd

# Replace these with your Alpaca API key and secret
API_KEY = 'CKGQTS1OSUY1N2AEIRDH'
SECRET_KEY = '0hVJVkpHNk06hD2LU9MUfkKh9scdL2M3xfLNQM9k'

# Alpaca's endpoint URL for market data
URL = "https://data.alpaca.markets/v1/bars/day"

# The stock symbols you are interested in
symbols = ['AAPL', 'MSFT', 'GOOG']  # example symbols

# Set up headers with the API credentials
headers = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': SECRET_KEY
}

# Prepare the parameters for the API request
params = {
    'symbols': ','.join(symbols),
    'start': '2022-01-01',  # example start date
    'end': '2022-12-31'     # example end date
}

# Make the request
response = requests.get(URL, headers=headers, params=params)

# Convert the response to a pandas DataFrame
data = pd.read_json(response.content)
