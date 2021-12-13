# Import packages
import pip
import requests
import pandas as pd
import matplotlib.pyplot as plt
import decimal
from decimal import Decimal

# Defining
apiKey = "6XJBG28TQUI6UA1Y"
portfolio = {}
UsernameList = ["Admin"]
PasswordList = ["Python"]

def get_user_login():
    global UserName
    global Password
    UserName = input("Please enter your username: ")
    Password = input("Please enter your password: ")
    return UserName, Password

def user_login():
    print("======================================")
    print("Welcome to the Investment Game")
    print("======================================\n")
    userType = input("Do you have an account for this Investment Game? please enter y/n: ")
    if userType == 'n':
        print("Please create an account")
        User = input("Please type your username: ")
        UsernameList.append(User)
        Pass = input("Please type your password: ")
        PasswordList.append(Pass)
        print("You have created your new account with the Investment Game, please login\n")
        get_user_login()
        while True:
            if UserName in UsernameList:  # is User1 in the list?
                if Password == PasswordList[UsernameList.index(UserName)]:
                    print("Log in Success")
                    break
                else:
                    print("Incorrect Password")
                    get_user_login()
            else:
                print("Incorrect username")
                get_user_login()
    else:
        print("Please login\n")
        get_user_login()
        while True:
            if UserName in UsernameList:  # is User1 in the list?
                if Password == PasswordList[UsernameList.index(UserName)]:
                    print("Log in Success")
                    break
                else:
                    print("Incorrect username or Password")
                    get_user_login()
            else:
                print("Incorrect username or Password")
                get_user_login()

    # Full name
    fullname = input("Please enter your full name: ")
    return fullname

def default_currency():
    # Ask the user which currency he uses
    currency = (input("Stock prices are in dollars. What currency are you using? (3 letters) "))

    return currency

def get_exchange_rate():
    global currency
    # Call the API to get the stock price over 5 minutes
    response = requests.get(f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency}&to_currency=USD&apikey={apiKey}")
    # If you are not getting a response, print error message below
    # See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    if response.status_code != 200:
        raise ValueError("Could not retrieve data, code:", response.status_code)

    # The service sends JSON data, we parse that into a Python datastructure
    raw_data = response.json()

    exchange_rate = round(Decimal(raw_data['Realtime Currency Exchange Rate']['5. Exchange Rate']), 3)
    print(f"Current exchange rate {currency} to USD is {exchange_rate}")

    return exchange_rate

def wallet():
    global currency
    # Available amount of money
    wallet = round(Decimal(input(f"Please enter your budget in {currency}: ")), 3)
    return wallet

def portfolio_edit():
    portfolio_edit = input("Do you have any shares? (y/n) ")
    while True:
        if portfolio_edit == "y":
            share = input("Which share do you have? ")
            amount = int(input("How many of that share do you have? "))
            portfolio[share] = amount
            moreShares = input("Do you have any other shares? (y/n) ")
            if moreShares == "n":
                break
        else:
            break
    return portfolio

def get_stock_data():
    global exchange_rate
    # Insert which stock you want to get data for
    symbol = input("Please provide the stock name: ")
    # Call the API to get the stock price over 5 minutes
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&outputsize=full&apikey={apiKey}")
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

    # Divide the stock prices in USD by the exchange rate to get the stock prices in the correct currency
    exchange_rate = float(exchange_rate)
    for column in ['open', 'high', 'low', 'close']:
        df[column] = df[column]/exchange_rate
    return df, symbol
    # df.info()
    # print(df.head())

def buy_stocks():
    global wallet
    global symbol
    global currency
    closing_price = round(Decimal(df.tail(1)['close'][0]), 3)
    print(f"Current price is: {closing_price} {currency}")
    try:
        current_stock_amount = portfolio[symbol]
    except:
        current_stock_amount = 0
    print("Your portfolio currently holds", current_stock_amount, "stocks of", symbol)
    while True:
        stock_amount = int(input("How many stocks do you want to buy? "))
        total_buying_price = closing_price*stock_amount
        print("Please confirm if you want to spend", str(total_buying_price), currency, "on", str(stock_amount), "shares of", str(symbol))
        confirmation = input("(y/n) ")
        if confirmation == "y":
            if total_buying_price > wallet:
                print("You can not afford this")
            else:
                wallet -= total_buying_price
                try:
                    portfolio[symbol] += stock_amount
                except:
                    portfolio[symbol] = stock_amount
                break
        else:
            continue


def sell_stocks():
    global wallet
    global symbol
    global currency
    closing_price = round(Decimal(df.tail(1)['close'][0]), 3)
    print(f"Current price is: {closing_price} {currency}")
    try:
        current_stock_amount = portfolio[symbol]
    except:
        current_stock_amount = 0
    print("Your portfolio currently holds", current_stock_amount, "stocks of", symbol)
    while True:
        stock_amount = int(input("How many stocks do you want to sell? "))
        total_selling_price = closing_price*stock_amount
        print("Please confirm if you want to sell", str(total_selling_price), currency, "on", str(stock_amount), "shares of", str(symbol))
        confirmation = input("(y/n) ")
        if confirmation == "y":
            if stock_amount > current_stock_amount:
                print("You can not sell this amount of shares, because they are not available in your portfolio. Your portfolio currently holds", current_stock_amount, "stocks of", symbol)
            else:
                wallet += total_selling_price
                portfolio[symbol] -= stock_amount
                break
        else:
            continue

def portfolio_info():
    global currency
    wallet_info = print("Your current cash balance is:", wallet, currency)

    portfolio_info = print("Your current portfolio is:", portfolio)
    return wallet_info, portfolio_info

def show_chart():
    df, symbol = get_stock_data()
    df[['open', 'high', 'low', 'close']].plot()
    plt.show()

def menu():
    global wallet
    global symbol
    global df
    # Show portfolio, Display chart of a share, Buy, sell, Quit
    print("\n--------- MENU ---------")
    print("1: Show portfolio")
    print("2: Get share info")
    print("3: Buy shares")
    print("4: Sell shares")
    print("5: Quit")
    print("----------------------\n")
    choice = int(input("To which page do you want to go? Enter a number: "))
    if choice == 1:
        portfolio_info()
        return_to_menu()
    elif choice == 2:
        show_chart()
        return_to_menu()
    elif choice == 3:
        df, symbol = get_stock_data()
        buy_stocks()
        return_to_menu()
    elif choice == 4:
        df, symbol = get_stock_data()
        sell_stocks()
        return_to_menu()
    else:
        quit()

def return_to_menu():
    print("----------------------")
    return_to_menu = int(input("Do you want to return to the menu (1) or Quit (2)? "))
    print("----------------------")
    if return_to_menu == 1:
        menu()
    else:
        quit()

def quit():
    print("\n ----------------------")
    print("Thank you for using our game. Have a good day!")

if __name__ == "__main__":
    fullname = user_login()
    currency = default_currency()
    exchange_rate = get_exchange_rate()
    wallet = wallet()
    portfolio_edit = portfolio_edit()
    menu()
