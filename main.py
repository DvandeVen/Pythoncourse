# Import packages
import requests
import pandas as pd
import matplotlib.pyplot as plt

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

    # Fix column datatypes and names
    df.index = pd.DatetimeIndex(df.index)
    df.rename(columns=lambda s: s[3:], inplace=True)

    return df
    # df.info()
    # print(df.head())
def buy_stocks():
    last_record = df[0]

    return last_record

if __name__ == "__main__":
    df = get_stock_data()
    print(df)
    df[['open', 'high', 'low', 'close']].plot()
    plt.show()
    last_record = buy_stocks()
    print(last_record)