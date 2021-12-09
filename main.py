# Import packages
import requests
import pandas as pd

def get_stock_data():

    # Insert which stock you want to get data for
    symbol = input("What stock are you interested in? ")
    # Call the API to get the stock price over 5 minutes
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&outputsize=full&apikey=demo")

    # If you are not getting a response, print error message below
    # See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    if response.status_code != 200:
        raise ValueError("Could not retrieve data, code:", response.status_code)

    # The service sends JSON data, we parse that into a Python datastructure
    raw_data = response.json()

    # Transpose time series data into a dataframe
    data = raw_data['Time Series (5min)']
    df = pd.DataFrame(data).T.apply(pd.to_numeric)

    return df
    # df.info()
    # print(df.head())

if __name__ == "__main__":
    df = get_stock_data()
    print(df)