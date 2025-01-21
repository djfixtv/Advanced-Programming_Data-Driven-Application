import requests
import pokebase as pkb
import os

allPokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0").json()
allNames = []
allLinks = []
allIDs = []
for pokemon in allPokemon["results"]:
    allNames.append(pokemon["name"])
    url = pokemon["url"]
    allLinks.append(url)
    allIDs.append(url[url[0:-1].rindex("/")+1:-1])

def readPokemonInfo(link):
    data = requests.get(link).json()
    speciesData = requests.get(data["species"]["url"]).json()

    print("Name: " + data["name"])

    print("Height: " + str(data["height"]))
    print("Weight: " + str(data["weight"]))
    print("")

    print("Base HP: " + str(data["stats"][0]["base_stat"]))
    print("Base ATK: " + str(data["stats"][1]["base_stat"]))
    print("Base DEF: " + str(data["stats"][2]["base_stat"]))
    print("")

    print("Types:")
    types = data["types"]
    for type in types:
        print("- " + type["type"]["name"])
    print("")
    
    print("Abilities:")
    abilities = data["abilities"]
    for ability in abilities:
        isHidden = ability["is_hidden"]
        abilityLink = ability["ability"]["url"]
        line = "- " + abilityLink[abilityLink[0:-1].rindex("/")+1:-1] + " : "
        if isHidden: line += "[HIDDEN] "
        line += "\"" + ability["ability"]["name"] + "\""
        print(line)
    print("")

    print("Flavor Text:")
    print("- " + speciesData["flavor_text_entries"][0]["flavor_text"])

    print("Pokemon info from - " + link)
    print("")

def readPokeInfo():
    ExitPanel = False
    while ExitPanel == False:
        print("Pokemon information panel")
        print("")
        print("1) Show pokemon list")
        print("2) Show pokemon data by name")
        print("3) Show pokemon data by ID")
        print("4) Exit")
        print("")
        validInput = False
        while validInput == False:
            userinput = input("> ")

            if(userinput == "quit"): exit(0)
            numinput = int(userinput)
            print("Option: " + str(numinput))

            if(numinput > 4 or numinput < 1):
                print("That option isn't valid, please try again.")
                continue

            validInput = True

            match(numinput):
                case 1:
                    for name in allNames:
                        print(name)
                case 2:
                    os.system("cls")
                    print("What's the name of the pokemon would you like to view? (Type \"cancel\" to return)")
                    print("")
                    validInput2 = False
                    pokeIndex = 0
                    while validInput2 == False:
                        pokeID = input("> ")
                        if pokeID == "cancel":
                            validInput2 = True
                            os.system("cls")
                            break

                        try:
                            pokeIndex = allNames.index(pokeID)
                            if pokeIndex == -1:
                                print("Invalid pokemon name. Try again or enter \"cancel\" to exit")
                                continue
                        except ValueError:
                            print("Invalid pokemon name. Try again or enter \"cancel\" to exit")
                            continue

                        validInput2 = True
                    
                    pokeDataLink = allLinks[pokeIndex]
                    os.system("cls")
                    readPokemonInfo(pokeDataLink)
                case 3:
                    os.system("cls")
                    print("readPokeInfo Loop 2")
                    print("Which pokemon would you like to view? (Type \"cancel\" to return)")
                    print("")
                    validInput2 = False
                    while validInput2 == False:
                        pokeID = input("> ")
                        if pokeID == "cancel":
                            validInput2 = True
                            os.system("cls")
                            break

                        try:
                            pokeIndex = allIDs.index(pokeID)
                            if pokeIndex == -1:
                                print("Invalid pokemon ID. Try again or enter \"cancel\" to exit")
                                continue
                        except ValueError:
                            print("Invalid pokemon ID. Try again or enter \"cancel\" to exit")
                            continue

                        validInput2 = True

                        pokeDataLink = allLinks[pokeIndex]
                        os.system("cls")
                        readPokemonInfo(pokeDataLink)
                case 4:
                    ExitPanel = True
                case _:
                    print("Invalid input. Please try again.")

def quit():
    print("Goodbye")
    exit(0)

mainPanels = [ readPokeInfo, quit ]

# Main Loop
while True:
    os.system("cls")
    print("Terminal")
    print("")
    print("Please choose one of the following, or type \"quit\" to quit.")
    print("1) Read pokemon info")
    print("2) Quit")
    print("")
    validInput = False
    userinput = ""
    while(validInput == False):
        try:
            userinput = input("> ")
            if(userinput == "quit"): exit(0)
            numinput = int(userinput)
            print("Option: " + str(numinput))

            if(numinput > 2 or numinput < 1):
                print("That option isn't valid, please try again.")
                continue

            validInput = True
            os.system("cls")
            mainPanels[numinput - 1]()
        except ValueError:
            print("Could not interpret that response. Please try again.")
