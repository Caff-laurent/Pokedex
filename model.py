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

def get_xy(df):
    rows = df.values.shape[0]                            # Get the number of rows in the DataFrame
    arr_x = np.zeros((rows, 200, 200, 3))                 # Create a numpy array of zeros with dimensions (rows, 200, 200, 3) for storing images (width, height, number of colors)
    arr_y = df["type_01"].values.reshape(-1, 1)           # Extract the values of the "type_01" column as the y-labels
    
    for i, (pokemon_images_number, pokemon_name, type) in enumerate(zip(df["pokemon_images_number"], df["name"], df["type_01"])):
        for j in range(1, pokemon_images_number + 1):
            sprite_filename = f"{pokemon_name}_{j}.jpg"    # Create the sprite filename based on the pokemon name and image number
            sprite_path = os.path.join("./Pokemon/dataset/" + type, sprite_filename)    # Construct the full path to the sprite image file
            sprite_image = Image.open(sprite_path).convert("RGB")               # Open the image file and convert it to RGB format
            sprite_image = sprite_image.resize((200, 200))                      # Resize the image to (200, 200)
            arr_x[i] = np.array(sprite_image)                                   # Convert the image to a numpy array and store it in the arr_x array
    
    y_domain = np.array(range(1, 19)).reshape(-1, 1)       # Create an array with values from 1 to 18 and reshape it to (-1, 1)
    oh_encoder = preprocessing.OneHotEncoder()             # Create a one-hot encoder object from scikit-learn
    oh_encoder.fit(y_domain)                               # Fit the one-hot encoder to the y-domain
    arr_y = oh_encoder.transform(arr_y).toarray()          # Apply one-hot encoding to the arr_y array
    arr_x = oh_encoder.transform(arr_x).toarray()          # Apply one-hot encoding to the arr_x array
    
    return arr_x, arr_y

x_train, y_train = get_xy(df_train)                       # Get the features (x_train) and labels (y_train) for training data
x_test, y_test = get_xy(df_test)                          # Get the features (x_test) and labels (y_test) for testing data
   
