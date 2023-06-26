import pandas as pd                                     # Importing the pandas library for data manipulation
import numpy as np                                      # Importing the numpy library for numerical operations
import sklearn.preprocessing as preprocessing         # Importing the preprocessing module from scikit-learn for data preprocessing
from sklearn.model_selection import train_test_split    # Importing train_test_split function from scikit-learn for data splitting
from utility.load import load_pokemon                    # Importing the load_pokemon function from the utility.load module
import os                                               # Importing the os module for operating system related functions
from PIL import Image                                   # Importing the Image class from the PIL library for image processing

# We load the pokemon

type_folders = {                                        # Dictionary mapping pokemon types to their respective folders
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

df = load_pokemon(type_folders)                         # Loading the pokemon data into a DataFrame

print(df)

# Pokemon has been loaded...

# NUMPY ARRAYS

# Getting unique ID List
id_list = df["id"].unique()                              # Extracting the unique ID values from the DataFrame

# Splitting the ID list into Test IDs and Train IDs
id_train, id_test = train_test_split(id_list, test_size=0.3, random_state=42)    # Splitting the ID list into train and test IDs

# Getting our dataframes split according to those lists
df_train = df[df["id"].isin(id_train)]                   # Creating a new DataFrame for training data based on the train IDs
df_test = df[df["id"].isin(id_test)]                     # Creating a new DataFrame for testing data based on the test IDs
print(df_train.shape)



# for j in range(1, pokemon_images_number + 1):
#     sprite_filename = f"{pokemon_name}_{j}.jpg"    # Create the sprite filename based on the pokemon name and image number
#     sprite_path = os.path.join("./Pokemon/dataset/" + pokemon_type, sprite_filename)    # Construct the full path to the sprite image file
#     sprite_image = Image.open(sprite_path).convert("RGB")               # Open the image file and convert it to RGB format
#     sprite_image = sprite_image.resize((200, 200))                      # Resize the image to (200, 200)
#     arr_x[i, j-1] = np.array(sprite_image)      