from tkinter import ttk as ttk
import tkinter as tk
import requests
# URL = "https://solaris0.hopto.org/Out1.txt"
# URL2 = "https://solaris0.hopto.org/Out2.txt"
# URL3 = "https://solaris0.hopto.org/Out3.txt"
# URL4 = "https://solaris0.hopto.org/Out4.txt"
URLs = [ "https://solaris0.hopto.org/Out1.txt", "https://solaris0.hopto.org/Out2.txt", "https://solaris0.hopto.org/Out3.txt", "https://solaris0.hopto.org/Out4.txt", "https://solaris0.hopto.org/test.txt" ]
Labels = [ "Output 1", "Output 2", "Output 3", "Output 4", "TEST" ]

# try:
#     print(response.text)
# except requests.exceptions.JSONDecodeError:
#     print("JSON Decoding Error")
# Out1 = requests.get(URL)
# Out2 = requests.get(URL2)
# Out3 = requests.get(URL3)
# Out4 = requests.get(URL4)

# def getrequest():
#     print(Out1.text)

# def getrequest2():
#     print(Out2.text)

# def getrequest3():
#     print(Out3.text)

# def getrequest4():
#     print(Out4.text)

menu = tk.Tk()
"""
b1 = tk.Button(text="Out1", command=getrequest)
b1.pack()
b2 = tk.Button(text="Out2", command=getrequest2)
b2.pack()
b3 = tk.Button(text="Out3", command=getrequest3)
b3.pack()
b4 = tk.Button(text="Out4", command=getrequest4)
b4.pack()
"""
def selectItem(event):
    clicked_item = combobox.get()
    index = Labels.index(clicked_item)
    URL = URLs[index]
    response = requests.get(URL)
    print(response.text)
combobox = ttk.Combobox(menu, values=Labels)
combobox.pack()
combobox.bind("<<ComboboxSelected>>", selectItem) # Why. Why the ACTUAL fuck?


menu.mainloop()