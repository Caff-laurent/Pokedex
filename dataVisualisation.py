from utility.plot import plot_chain
from utility.load import load_pokemon
from utility.plot import plot_display

# Will plot (show) the image give
plot_chain("Fire",["Charizard_1","Charizard_2","Charizard_3"]);

type_folders = {    
    "Bug" : "Bug",
    "Dragon" : "Dragon",
    "Electric" : "Electric",
    "Fairy" : "Fairy",
    "Fighting" : "Fighting",
    "Fire" : "Fire",
    "Ghost" : "Ghost",
    "Grass" : "Grass",
    "Ground" : "Ground",
    "Ice" : "Ice",
    "Normal" : "Normal",
    "Poison" : "Poison",
    "Psychic" : "Psychic",
    "Rock" : "Rock",
    "Water" : "Water"
}

df = load_pokemon(type_folders)
print(df)

for i in range(1,10,1):
    plot_display(df.loc[i])