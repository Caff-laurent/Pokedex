from utility.load import load_dataframe

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

# Load the images aspect and specific data 
df = load_dataframe(type_folders)

from utility.plot import plot_record

for i in range(1,3500,400):
    print(df)
    plot_record(df.loc[i])