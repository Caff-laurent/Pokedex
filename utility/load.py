import pandas as pd
import csv
import os
import matplotlib.image as mpimg
from matplotlib import gridspec
from skimage import color
import numpy as np
from skimage.util import dtype

def _prepare_rgba_array(arr):
    """Check the shape of the array to be RGBA and convert it to
    floating point representation.
    """
    arr = np.asanyarray(arr)

    if arr.ndim not in [3, 4] or arr.shape[-1] != 4:
        msg = ("the input array must have a shape == (.., ..,[ ..,] 4)), "
               "got {0}".format(arr.shape))
        raise ValueError(msg)

    return dtype.img_as_float(arr)


def rgba2rgb(rgba, background=(1, 1, 1)):
    """RGBA to RGB conversion.
    Parameters
    ----------
    rgba : array_like
        The image in RGBA format, in a 3-D array of shape ``(.., .., 4)``.
    background : array_like
        The color of the background to blend the image with. A tuple
        containing 3 floats between 0 to 1 - the RGB value of the background.
    Returns
    -------
    out : ndarray
        The image in RGB format, in a 3-D array of shape ``(.., .., 3)``.
    Raises
    ------
    ValueError
        If `rgba` is not a 3-D array of shape ``(.., .., 4)``.
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Alpha_compositing#Alpha_blending
    Examples
    --------
    >>> from skimage import color
    >>> from skimage import data
    >>> img_rgba = data.logo()
    >>> img_rgb = color.rgba2rgb(img_rgba)
    """
    arr = _prepare_rgba_array(rgba)
    if isinstance(background, tuple) and len(background) != 3:
        raise ValueError('the background must be a tuple with 3 items - the '
                         'RGB color of the background. Got {0} items.'
                         .format(len(background)))

    alpha = arr[..., -1]
    channels = arr[..., :-1]
    out = np.empty_like(channels)

    for ichan in range(channels.shape[-1]):
        out[..., ichan] = np.clip(
            (1 - alpha) * background[ichan] + alpha * channels[..., ichan],
            a_min=0, a_max=1)
    return out

# def load_type_dict():
#     data_path = "./dataset"  # Path to the dataset directory
#     types_file = "pokemon_types_names.csv"  # Name of the types file
#     types_path = os.path.join(data_path, types_file)  # Full path to the types file
#     type_dict = {}  # Dictionary to store type information

#     with open(types_path, "r") as f:
#         reader = csv.reader(f)  # Create a CSV reader object
#         next(reader, None)  # Skip the header row

#         # Iterate over each row in the CSV file
#         for row in reader:
#             type_dict[int(row[0])] = {
#                 "label": row[2],  # Type label (e.g., "Grass", "Fire", etc.)
#                 "color": get_text_color_from_type(row[2])  # Type color (hexadecimal value)
#             }
#     return type_dict

def get_text_color_from_type(type_name):
    type_hexa = {
        "Normal": "#A8A878",
        "Fighting": "#C03028",
        "Flying": "#A890F0",
        "Poison": "#A040A0",
        "Ground": "#E0C068",
        "Rock": "#B8A038",
        "Bug": "#A8B820",
        "Ghost": "#705898",
        "Steel": "#B8B8D0",
        "Fire": "#F08030",
        "Water": "#6890F0",
        "Grass": "#78C850",
        "Electric": "#F8D030",
        "Psychic": "#F85888",
        "Ice": "#98D8D8",
        "Dragon": "#7038F8",
        "Dark": "#705848",
        "Fairy": "#EE99AC"
    }
    return type_hexa.get(type_name.capitalize(), None)




def load_pokemon_dict():
    """Loads the Pokemon Dictionary into memory. This dictionary contains
    information of Pokemon Typing, stored as:
    
    ID: {type_01: value, type_02: value}
    
    """
    data_path = "./dataset"
    pokemon_file = "pokemon_types_names.csv"
    pokemon_path = os.path.join(data_path,pokemon_file)
    pokemon_dict = {}
    # r mean read mode, when we open with "with" -> an instance of the file is created called f, f is a copy of pokemon_types_names.csv
    with open(pokemon_path,"r") as f: 
        # To make the data from the CSV file accessible, we can store it in an array-like structure
        reader = csv.reader(f)
        next(reader,None) #Skip the header
        for row in reader:
            pkm_id = int(row[0])
            pkm_name = str(row[1])
            pkm_type1 = str(row[2])
            pkm_type2 = str(row[3])
            if pkm_id not in pokemon_dict:
                pokemon_dict[pkm_id] = {"name": None, "type_01": None, "type_02": None}
                pokemon_dict[pkm_id]["name"] = pkm_name
                pokemon_dict[pkm_id]["type_01"] = pkm_type1
            if pkm_type2 is not None:
                pokemon_dict[pkm_id]["type_02"] = pkm_type2
            else:
                raise ValueError("Unexpected type slot value")
    return pokemon_dict

# Will find the pokemon in dataset and give it here type in accordance to the csv file
def load_pokemon(pokemon_types):
    pkm_dict = load_pokemon_dict()
    df_dict = {"id" : [], "name": [], "pokemon_images_number": [], "type_01": [], "type_02": [], "text_color_type_01": [], "text_color_type_02": []}
    pokemons_folder = "./Pokemon/dataset/"
    
    for type in pokemon_types.items():
        type_folder = os.path.join(pokemons_folder,type[0])
        # Will store the pokemon in that list if he has current type in the loop
        pokemonList = [(pkm_id, pkm_dict[pkm_id]["name"]) for pkm_id in pkm_dict.keys() if pkm_dict[pkm_id]["type_01"] ==  type[0] or pkm_dict[pkm_id]["type_02"] ==  type[0]]
        print("Number of Pokemon with type", type[0], ":",  len(pokemonList))

        for pokemon_id, pokemon_name in pokemonList:
            # Will find if the pokemon in the cvs is in the dataset
            image_file = "{id}_1.jpg".format(id=pokemon_name)
            image_path = os.path.join(type_folder,image_file)
            if not os.path.exists(image_path):
                continue
            pokemon_images_number = count_pokemon_file_name(type[0], pokemon_name)
            df_dict["id"].append(pokemon_id)
            df_dict["name"].append(pokemon_name)
            df_dict["pokemon_images_number"].append(pokemon_images_number)
            df_dict["type_01"].append(pkm_dict[pokemon_id]["type_01"])
            df_dict["type_02"].append(pkm_dict[pokemon_id]["type_02"])
            df_dict["text_color_type_01"].append(get_text_color_from_type(pkm_dict[pokemon_id]["type_01"]) )
            df_dict["text_color_type_02"].append(get_text_color_from_type(pkm_dict[pokemon_id]["type_02"]) )
    return pd.DataFrame.from_dict(df_dict)



def count_pokemon_file_name(pokemon_type, pokemon_name):
    pokemons_folder = "./Pokemon/dataset/"
    type_folder = os.path.join(pokemons_folder, pokemon_type)
    file_count = 0
    digit = 1
    
    while True:
        file_name = pokemon_name + '_' + str(digit) + '.jpg'
        
        if file_name in os.listdir(type_folder):
            file_count += 1
            digit += 1
        else:
            break
    
    print('Number of files for the pokemon called ' + pokemon_name + ' : ' + str(file_count))
    return file_count
