# Import packages
import pip
import requests
import pandas as pd
import matplotlib.pyplot as plt
import decimal
from decimal import Decimal

# Create portfolio dictionary
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
    userType = input("Do you have an account for this Investment Game? please enter y/n:")
    if userType == 'n':
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

def wallet():
    # Available amount of money
    wallet = round(Decimal(input("Please enter your budget: ")), 3)
    # Currencies to be added later
    # Limits to be added later
    # More user variables?
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

    return df, symbol
    # df.info()
    # print(df.head())

def buy_stocks():
    global wallet
    global symbol
    closing_price = round(Decimal(df.tail(1)['close'][0]), 3)
    print("Current price is: ", closing_price, " euros")
    while True:
        stock_amount = int(input("How many stocks do you want to buy? "))
        total_buying_price = closing_price*stock_amount
        print("Please confirm if you want to spend", str(total_buying_price), "euros on", str(stock_amount), "shares of", str(symbol))
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
    closing_price = round(Decimal(df.tail(1)['close'][0]), 3)
    print("Current price is: ", closing_price, " euros")
    while True:
        stock_amount = int(input("How many stocks do you want to sell? "))
        total_selling_price = closing_price*stock_amount
        print("Please confirm if you want to sell", str(total_selling_price), "euros on", str(stock_amount), "shares of", str(symbol))
        confirmation = input("(y/n)")
        if confirmation == "y":
            if stock_amount > portfolio[symbol]:
                print("You can not sell this amount of shares, because they are not available in your portfolio")
            else:
                wallet += total_selling_price
                portfolio[symbol] -= stock_amount
                break
        else:
            continue

def portfolio_info():
    wallet_info = print("Your current cash balance is:", wallet, "euros")
    value_of_shares =

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
    print("--------- MENU ---------")
    print("1: Show portfolio")
    print("2: Get share info")
    print("3: Buy shares")
    print("4: Sell shares")
    print("5: Quit")
    print("---------------------- \n")
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
    return_to_menu = int(input("Do you want to return to the menu (1) or Quit (2)?"))
    print("----------------------")
    if return_to_menu == 1:
        menu()
    else:
        quit()

def quit():
    print("----------------------")
    print("Thank you for using our game. Have a good day!")

if __name__ == "__main__":
    fullname = user_login()
    wallet = wallet()
    portfolio_edit = portfolio_edit()
    menu()



















    # print('So your full name is ', fullname, ' and your budget is ', wallet)
    #df, symbol = get_stock_data()
    # print(df)

    # Display chart
    #df[['open', 'high', 'low', 'close']].plot()
    #plt.show()

    #if len(portfolio) == 0:
    #    buyTransaction = buy_stocks()
    #else:
    #    typeOfTransaction = input("Do you want to buy or sell stocks? (b/s) ")
    #    if typeOfTransaction == "b":
    #        buyTransaction = buy_stocks()
    #    else:
     #       sellTransaction = sell_stocks()




