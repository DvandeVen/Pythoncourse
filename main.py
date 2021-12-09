UsernameList = ["jacob"]
PasswordList = ["pass1"]

print("Welcome to the Investment Game")
userType = input("Do you have an account for this Investment Game? please enter y/n:")

#maybe add account info here

if userType == 'n':
    User = input("Please type your username: ")
    UsernameList.append(User)
    Pass = input("Please type your password: ")
    PasswordList.append(Pass)
    print("You have created your new account with the Investment Game, please login\n")
    UserName = input("Please enter your username: ")
    Password = input("Please enter your password: ")
    if UserName in UsernameList:  # is User1 in the list?
        if Password == PasswordList[UsernameList.index(UserName)]:
            print("Log in Success")
    else:
        print("Incorrect username or Password")
else:
    print("Please login\n")
    UserName = input("Please enter your username: ")
    Password = input("Please enter your password: ")
    if UserName in UsernameList:  # is User1 in the list?
        if Password == PasswordList[UsernameList.index(UserName)]:
            print("Log in Success")
        else:
            print("Incorrect username or Password")
    else:
        print("Incorrect username or Password")

# Full name
fullname = input("Please enter your full name: ")
# Available amount of money
wallet = input("Please enter your budget: ")
# Currencies to be added later
# Limits to be added later
# More user variables?

print('So your full name is ', fullname, ' and your budget is ', wallet)






