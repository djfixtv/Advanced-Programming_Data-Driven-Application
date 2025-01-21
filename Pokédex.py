import requests
from tkinter import ttk as ttk
from tkinter import *
from PIL import Image, ImageTk
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import os

allPokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0").json()
allNames = []
allLinks = []

for pokemon in allPokemon["results"]:
    allNames.append(pokemon["name"])
    allLinks.append(pokemon["url"])

root = Tk()
root.title("Pokédex")
root.config(bg="#ce242c", borderwidth=5, relief="ridge")

lw = 135
lh = 135

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20

def readPokemonInfo(link):
    data = requests.get(link).json()
    speciesData = requests.get(data["species"]["url"]).json()

    name = data["name"]
    height = data["height"]
    weight = data["weight"]
    baseHP = data["stats"][0]["base_stat"]
    baseATK = data["stats"][1]["base_stat"]
    baseDEF = data["stats"][2]["base_stat"]
    SpAtk = data["stats"][3]["base_stat"]
    SpDef = data["stats"][4]["base_stat"]
    Speed = data["stats"][5]["base_stat"]
    flavor = speciesData["flavor_text_entries"][0]["flavor_text"]
    pokeID = data["id"]
    spriteURL = data["sprites"]["front_default"]

    print("Types:")
    types = data["types"]
    typesOutput = ""
    for type in types:
        print("- " + type["type"]["name"])
        typesOutput += "- " + type["type"]["name"] + "\n"
    print("")
    
    print("Abilities:")
    abilities = data["abilities"]
    abilitiesOutput = ""
    for ability in abilities:
        abilityLink = ability["ability"]["url"]
        line = "- " 
        line += "\"" + ability["ability"]["name"] + "\""
        abilitiesOutput += line + "\n"
        print(line)
    abilitiesOutput = abilitiesOutput[:-1]
    typesOutput = typesOutput[:-1] 
    
    return {
            "name" : name, 
            "height" : height, 
            "weight" : weight, 
            "basehp" : baseHP,
            "baseatk" : baseATK, 
            "basedef" : baseDEF, 
            "flavortext" : flavor,
            "sp.atk" : SpAtk,
            "sp.def" : SpDef,
            "speed" : Speed,
            "spriteURL" : spriteURL,
            "pokeID" : pokeID,
            "abilities" : abilitiesOutput,
            "types" : typesOutput
            }

lastSelected = -1
updateCooldown = 0

def clearCooldown():
    global updateCooldown
    updateCooldown -= 1
    if updateCooldown != 0: return
    if lastSelected != pokelist.curselection()[0] : RunPokeUpdate()

def PokeSelect (Event):
    global updateCooldown
    updateCooldown += 1 # Increment cooldown value
    root.after(500, clearCooldown) # Load page after 0.5 seconds from last input
    
def RunPokeUpdate():
    global lastSelected
    newSelection = pokelist.curselection()[0]
    if lastSelected == newSelection: return
    lastSelected = newSelection
    pokeData = readPokemonInfo(allLinks[newSelection])
    loadPokeData(pokeData)

def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.
    '''
    # Load font into the system
    if isinstance(fontpath, str):
        pathbuf = create_string_buffer(fontpath.encode('utf-8'))  # Encode as bytes
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):  # Python 3: str handles unicode as well
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str')

    # Determine the flags based on the private and enumerable options
    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)

    # Add the font resource and return True if successful, False otherwise
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

# Ensure the font is loaded correctly
fontpath = r"pokemon_pixel_font.ttf"
loadfont(fontpath)

pil_image = Image.open("missingno.png")
resized_image = pil_image.resize((lw, lh), Image.Resampling.LANCZOS)
image = ImageTk.PhotoImage(resized_image)

#Pokemon list frame
listframe = Frame(root, bg="#ce242c", borderwidth=5, relief="ridge")
listframe.grid(row=0, column=0)

pokelist = Listbox(listframe, width=27, height=15, font=("Pokemon Pixel Font", 20, "bold"), bg="#8e1a21", fg="light gray", selectbackground="#f78c8d")
pokelist.grid(row=0, column=0)
pokelist.bind("<<ListboxSelect>>", PokeSelect)

sbar = Scrollbar(listframe, width=15, orient="vertical", borderwidth=5, relief="ridge", activebackground="#610b0f", troughcolor="#610b0f")
sbar.grid(row=0, column=1, sticky="ns")

pokelist.config(yscrollcommand=sbar.set)
sbar.config(command=pokelist.yview)

# Pokemon information frame
dataframe = Frame(root, bg='#40a9d8', borderwidth=5, relief="ridge")
dataframe.grid(row=0, column=2)

name = Message(dataframe, text="", width=200, justify="center", font=("Pokemon Pixel Font", 30, "bold"), bg='#40a9d8', fg="#1c1c1c")
name.grid(row=0, column=0, columnspan=2, sticky="n", padx=2, pady=2, )

height = Message(dataframe, text="Height: ", width=200, justify="left",font=("Pokemon Pixel Font", 20, "bold"), bg='#40a9d8', fg="#1c1c1c")
height.grid(row=1, column=0, sticky="w", padx=2, pady=2)

weight = Message(dataframe, text="Weight: ", width=200, justify="left",font=("Pokemon Pixel Font", 20, "bold"), bg='#40a9d8', fg="#1c1c1c")
weight.grid(row=1, column=1, sticky="w", padx=2, pady=2)

abilities = Message(dataframe, text="Abilities: ", width=200, justify="left",font=("Pokemon Pixel Font", 20, "bold"), bg='#40a9d8', fg="#1c1c1c")
abilities.grid(row=2, column=0, sticky="w", padx=2, pady=2)

types = Message(dataframe, text="Types: ", width=200, justify="left",font=("Pokemon Pixel Font", 20, "bold"), bg='#40a9d8', fg="#1c1c1c")
types.grid(row=2, column=1, sticky="w", padx=2, pady=2)

flavor = Message(dataframe, text="",font=("Pokemon Pixel Font", 20, "bold"), bg='#40a9d8', fg="#1c1c1c")
flavor.grid(row=3, column=0, columnspan=2)

# Pokemon stats Frame
statframe = Frame(root, bg="#4caf50", borderwidth=5, relief="ridge")
statframe.grid(row=0, column=3)

imageLabel = Label(statframe, image=image, width=lw, height=lh, bg="#4caf50", borderwidth=2, relief="ridge")
imageLabel.grid(row=1, column=0)

basehp = Message(statframe, bg="#4caf50", text="HP:", justify="left", font=("Pokemon Pixel Font", 20, "bold"), width=100, padx=20, fg="#1c1c1c")
basehp.grid(row=2, column=0, columnspan=3, sticky="w")

baseatk = Message(statframe, bg="#4caf50", text="ATK:", justify="left", font=("Pokemon Pixel Font", 20, "bold"), width=100, padx=20, fg="#1c1c1c")
baseatk.grid(row=3, column=0, columnspan=3, sticky="w")

basedef = Message(statframe, bg="#4caf50", text="DEF:", justify="left", font=("Pokemon Pixel Font", 20, "bold"), width=100, padx=20, fg="#1c1c1c")
basedef.grid(row=4, column=0, columnspan=3, sticky="w")

spatk = Message(statframe, bg="#4caf50", text="Sp.Atk:", justify="left", font=("Pokemon Pixel Font", 20, "bold"), width=100, padx=20, fg="#1c1c1c")
spatk.grid(row=5, column=0, columnspan=3, sticky="w")

spdef = Message(statframe, bg="#4caf50", text="Sp.Def:", justify="left", font=("Pokemon Pixel Font", 20, "bold"), width=100, padx=20, fg="#1c1c1c")
spdef.grid(row=6, column=0, columnspan=3, sticky="w")

speed = Message(statframe, bg="#4caf50", text="Speed:", justify="left", font=("Pokemon Pixel Font", 20, "bold"), width=100, padx=20, fg="#1c1c1c")
speed.grid(row=7, column=0, columnspan=3, sticky="w")

def loadPokeData(pokeData):
    print(pokeData)
    name.config(text=pokeData["name"]) 
    flavor.config(text=pokeData["flavortext"])
    height.config(text="Height: " + str(pokeData["height"]))
    weight.config(text="Weight: " + str(pokeData["weight"]))
    basehp.config(text="HP: " + str(pokeData["basehp"]))
    baseatk.config(text="ATK: " + str(pokeData["baseatk"]))
    basedef.config(text="DEF: " + str(pokeData["basedef"]))
    spatk.config(text="Sp.ATK: " + str(pokeData["sp.atk"]))
    spdef.config(text="Sp.DEF: " + str(pokeData["sp.def"]))
    speed.config(text="Speed: " + str(pokeData["speed"]))
    abilities.config(text="Abilities: \n" + pokeData["abilities"])
    types.config(text="Types: \n" + pokeData["types"])
    loadPokeSprite(pokeData["spriteURL"], pokeData["pokeID"])

def checkforfolder():
    # Create the Sprites folder if it doesn't already exist - (from: https://www.geeksforgeeks.org/create-a-directory-in-python/)
    directory_name = "sprites"
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def loadPokeSprite(spriteURL, pokeID):
    checkforfolder()
    spritePath = os.path.join(os.path.abspath("sprites"), str(pokeID) + ".png")
    print("Sprite Path: " + spritePath)
    if(os.path.exists(spritePath)):
        loadImage(spritePath)
    else:
        if spriteURL == None:
            loadImage("missingno.png")
        else:
            imageResponse = requests.get(spriteURL)
            try:
                imageFile = open(spritePath, "wb")
                imageFile.write(imageResponse.content)
                imageFile.close()
                loadImage(spritePath)
            except:
                print("Uh oh")
                loadImage("missingno.png")

def loadImage(path):
    loaded_image = Image.open(path)
    loaded_resized = loaded_image.resize((lw, lh), Image.Resampling.LANCZOS)
    loaded_final = ImageTk.PhotoImage(loaded_resized)
    imageLabel.config(image=loaded_final)
    imageLabel.image = loaded_final

for line in range(len(allNames)):
    pokelist.insert(line, "  " + allNames[line])
loadPokeData(readPokemonInfo(allLinks[0])) 
root.mainloop()