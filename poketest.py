# import pokebase as pkb # fuckin' useless, cracker
import requests
import tkinter as tk
from tkinter import ttk as ttk

allPokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0").json()
allNames = []
allLinks = []
for pokemon in allPokemon["results"]:
    allNames.append(pokemon["name"])
    allLinks.append(pokemon["url"])

root = tk.Tk()
root.title("PokeBase Test")

def selectEvent(event): # "event" is actually useless here. Necessary to avoid crashes though.
    clicked_item = combobox.get()
    print("Selected item: " + clicked_item)
    clicked_link = allLinks[allNames.index(clicked_item)]
    print("Required link: " + clicked_link)

tk.Label(text="Mirror mirror on the wall, who's the gayest of them all?").pack()
combobox = ttk.Combobox(root, values=allNames)
combobox.pack(pady=5)
combobox.set("you")
combobox.bind("<<ComboboxSelected>>", selectEvent) # Why. Why the ACTUAL fuck?

root.mainloop()