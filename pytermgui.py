import tkinter as tk
from tkinter import messagebox

#
# window = tkinter.Tk()
# greeting = tkinter.Label(text="Hello, Tkinter")
# greeting.pack()
# window.mainloop()

# window = tk.Tk()
# greeting = tk.Label(text="Hello, Tkinter",foreground="yellow",background="purple", width=10,height=10)
# greeting.pack()
# window.mainloop()


def display1():
    messagebox.showinfo("Investment game", "You clicked Show Portfolio")

def display2():
    messagebox.showinfo("Investment game", "You clicked Get Share Info")

def display3():
    messagebox.showinfo("Investment game", "You clicked Buy Shares")

def display4():
    messagebox.showinfo("Investment game", "You clicked Sell Shares")

def display5():
    messagebox.showinfo("Investment game", "You clicked Quit. Have a nice day!")


window = tk.Tk()
window.title('Investment Game')
greeting = tk.Label(text="MENU\n Please choose one of the following options:",
                    anchor='n', foreground="yellow",background="purple", width=100,height=10, pady = 100)
greeting.pack()
b1 = tk.Button(window, bg = 'yellow', text="Show portfolio", command=display1, 	wraplength = 70).place(x=100, y=200)
b2 = tk.Button(window, bg = 'yellow', text="Get share info", command=display2, wraplength = 70).place(x=200, y=200)
b3 = tk.Button(window, bg = 'yellow', text="Buy shares", command=display3, height = 2).place(x=300, y=200)
b4 = tk.Button(window, bg = 'yellow', text="Sell shares", command=display4, height = 2).place(x=400, y=200)
b5 = tk.Button(window, bg = 'yellow', text="Quit", command=display5, height = 2).place(x=500, y=200)
window.mainloop()